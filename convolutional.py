def message_to_int_array(message):
    return list(map(int, message))


def generate_polynoms(n, k):
    # перевернутые двоичные n и k
    bin_n = str(bin(n))[2:][::-1]
    bin_k = str(bin(k))[2:][::-1]

    # удаление лишних 0 спереди
    while bin_n[0] == '0' and bin_k[0] == '0':
        bin_n = bin_n[1:]
        bin_k = bin_k[1:]

    # удаление лишних 0 сзади
    while bin_n[-1] == '0' and bin_k[-1] == '0':
        bin_n = bin_n[:-1]
        bin_k = bin_k[:-1]

    # задание одинаковой длины кодам
    while len(bin_n) != len(bin_k):
        if len(bin_n) > len(bin_k):
            bin_k += '0'
        else:
            bin_n += '0'

    return list(map(int, bin_n)), list(map(int, bin_k))


def convolutional_code(top_conn, bottom_conn, binary_message):
    coded_message = ''
    registers = [0] * len(top_conn)

    for bit in binary_message:
        # Сдвинуть элементы регистров, поместить следующий на позицию 1
        registers.pop()
        registers.insert(0, bit)

        top_bit = 0
        bottom_bit = 0
        for bit_in_register, top_has_connection, bottom_has_connection in zip(registers, top_conn, bottom_conn):
            if top_has_connection:
                top_bit ^= bit_in_register
            if bottom_has_connection:
                bottom_bit ^= bit_in_register

        coded_message += f'{top_bit}{bottom_bit}'

    return coded_message


