from karnaugh_template import KarnaughMapProcessor, TruthTableData


ODS_3_truth_table = \
    [
        [0, 0, 0, 0, 1, 1, 1, 1],  # P_i perenos from previous
        [0, 0, 1, 1, 0, 0, 1, 1],  # A
        [0, 1, 0, 1, 0, 1, 0, 1],  # B
        [0, 1, 1, 0, 1, 0, 0, 1],  # S sum
        [0, 0, 0, 1, 0, 1, 1, 1],  # P_i+1 perenos to the next
    ]

D8421_plus_5_truth_table = [
    [0, 0, 0, 0, 0, 1, 0, 1],  # 0 +5=5  → 0101
    [0, 0, 0, 1, 0, 1, 1, 0],  # 1 +5=6 → 0110
    [0, 0, 1, 0, 0, 1, 1, 1],  # 2 +5=7 → 0111
    [0, 0, 1, 1, 1, 0, 0, 0],  # 3 +5=8 → 1000
    [0, 1, 0, 0, 1, 0, 0, 1],  # 4 +5=9 →
    [0, 1, 0, 1, 0, 0, 0, 0],  # 5 +5=0 →
    [0, 1, 1, 0, 0, 0, 0, 1],  # 6 +5=1 →
    [0, 1, 1, 1, 0, 0, 1, 0],  # 7 +5=2 →
    [1, 0, 0, 0, 0, 0, 1, 1],  # 8 +5=3 →
    [1, 0, 0, 1, 0, 1, 0, 0],  # 9 +5=14 →

    [1, 0, 1, 0, 0, 0, 0, 0],  # 10 +5=15 →
    [1, 0, 1, 1, 0, 0, 0, 0],  # 11 +5=16 →
    [1, 1, 0, 0, 0, 0, 0, 0],  # 12 +5=17 →
    [1, 1, 0, 1, 0, 0, 0, 0],  # 13 +5=18 →
    [1, 1, 1, 0, 0, 0, 0, 0],  # 14 +5=19 →  (mod16)
    [1, 1, 1, 1, 0, 0, 0, 0],  # 15 +5=20 →
]

def print_ODS_3_truth_table():
    print('Таблица истинности ОДС3:')
    bits = ['P_i:  ', 'A:    ', 'B:    ', 'S_sum:', 'P_i+1:']
    for i in range(5):
        line_to_print = ''
        for j in range(len(ODS_3_truth_table[i])):
            line_to_print += str(ODS_3_truth_table[i][j]) + ' '
        print(bits[i] + line_to_print)

def print_D8421_plus5_truth_table():
    print('Таблица истинности Д8421+5:')
    print('A  B  C  D  A\' B\' C\' D\'')
    for row in D8421_plus_5_truth_table:
        print('  '.join(map(str, row[:4])) + '  ' + '  '.join(map(str, row[4:])))
    print("=======================")


def process_minimization(output_index, output_name):
    variables = ['A', 'B', 'C', 'D']
    table_content = []
    for row in D8421_plus_5_truth_table:
        input_vars = row[:4]
        output = row[4 + output_index]
        table_row = input_vars + [output]
        table_content.append(table_row)

    truth_table = TruthTableData(variables, table_content)
    processor_dnf = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=table_content,
        is_conjunctive_form=False
    )
    processor_cnf = KarnaughMapProcessor(
        variables=variables,
        truth_table_rows=table_content,
        is_conjunctive_form=True
    )
    print(f'\nМинимизация для {output_name}:')
    print('СДНФ:', processor_dnf.compute_minimized_form())
    #print('СКНФ:', processor_cnf.compute_minimized_form())

# print_D8421_plus5_truth_table()
# print_ODS_3_truth_table()
# process_minimization(0, "A'")
# process_minimization(1, "B'")
# process_minimization(2, "C'")
# process_minimization(3, "D'")


