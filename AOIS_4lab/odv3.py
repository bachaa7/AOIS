from itertools import product

def odv3_table():
    table = []
    for a, b, bin in product([0, 1], repeat=3):
        d = a ^ b ^ bin
        bout = (not a and b) or (not a and bin) or (b and bin)
        table.append([a, b, bin, int(d), int(bout)])
    return table

def build_sdnf_for_column(table, column_index):
    terms = []
    var_names = ['a', 'b', 'bin']
    for row in table:
        if row[column_index] == 1:
            term = []
            for i, val in enumerate(row[:3]):
                term.append(var_names[i] if val == 1 else f"!{var_names[i]}")
            terms.append("(" + " & ".join(term) + ")")
    return " | ".join(terms)


