def divide_table(table):
    optimal_difference = sum(table.values())
    optimal_index = 0

    for i in range(len(table)):
        current_difference = abs(sum(list(table.values())[:i]) - sum(list(table.values())[i:]))

        if current_difference < optimal_difference:
            optimal_difference = current_difference
            optimal_index = i
    return dict({item for i, item in enumerate(table.items()) if i < optimal_index}), \
            dict({item for i, item in enumerate(table.items()) if i >= optimal_index})


def shennon_code(table, value='', codes={}):
    if len(table) != 1:
        a, b = divide_table(table)
        shennon_code(a, value + '0', codes)
        shennon_code(b, value + '1', codes)
    else:
        codes[table.popitem()[0]] = value
    return codes
