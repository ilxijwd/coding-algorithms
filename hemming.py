from itertools import count


def slice_message_to_str(bits, k):
    """
    :param bits: binary message (string of 0..1)
    :param k: input word length
    :return: array of input words as strings
    """
    chunks = [bits[i:i + k] for i in range(0, len(bits), k)]
    while len(chunks[-1]) != k:
        chunks[-1] += '0'
    return chunks


def slice_message_to_int(bits, k):
    """
    :param bits: binary message (string of 0..1)
    :param k: input word length
    :return: array of input words as int arrays
    """
    chunks = [[int(bit) for bit in bits[i:i + k]] for i in range(0, len(bits), k)]
    while len(chunks[-1]) != k:
        chunks[-1].append(0)
    return chunks


def generate_new_chunk(old_chunk, n):
    """
    :param old_chunk: chunk with no control bits
    :param n: output word length
    :return: returns new chunk filled with control bits
    """
    new_chunk = old_chunk.copy()
    for i in (2**p for p in count(0)):
        if i > n:
            return new_chunk
        new_chunk.insert(i - 1, 0)


# https://habr.com/ru/post/140611/
# https://www.boyarkirk.ru/all/prostoy-kod-hemminga-praktika/
def hemming_encoding(chunks, n):
    """
    :param chunks: input binary chunks
    :param n: output word length
    :return: does magic
    """
    new_chunks = []
    for chunk_index, chunk in enumerate(chunks):
        new_chunk = generate_new_chunk(chunk, n)
        for table_row_index, table_row_value in enumerate((2 ** p for p in count(0))):
            if table_row_value > n:
                # print(f'{chunk_index} chunk is full')
                new_chunks.append(new_chunk)
                break

            ones = 0

            # to start iteration from 2 -> (2, 4, 8, 16 ...)
            step = (table_row_index + 1) ** 2
            if table_row_index == 0:
                step = 2

            for sequence_start in range(table_row_value - 1, n, step):
                indexes = list(range(sequence_start + table_row_value))[sequence_start:]
                for index in indexes:
                    if index < n:
                        ones += new_chunk[index]

            new_chunk[table_row_value] = 0 if ones % 2 == 0 else 1

    import functools
    import operator

    flattened_array = functools.reduce(operator.iconcat, new_chunks, [])
    return "".join(str(c) for c in flattened_array)
