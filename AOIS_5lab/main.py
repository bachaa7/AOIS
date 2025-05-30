from karnaugh_map import *

DIGITAL_DEVICE_TRUTH_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],  # q3'
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],  # q2'
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],  # q1'
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # V
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # q3
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],  # q2
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],  # q1
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # h3
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],  # h2
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # h1
]

def print_truth_table(table):
    num_rows = len(table)
    row_names = ['q3\'', 'q2\'', 'q1\'', 'V', 'q3', 'q2', 'q1', 'h3', 'h2', 'h1']

    for i in range(num_rows):
        name = row_names[i] if i < len(row_names) else f'row{i}'
        values = ' '.join(str(bit) for bit in table[i])
        print(f'{name:>4} | {values}')

def build_kmap_4vars(table, output_index):
    kmap = [[0 for _ in range(4)] for _ in range(4)]
    for    i in range(16):
        q3_ = table[0][i]
        q2_ = table[1][i]
        q1_ = table[2][i]
        V = table[3][i]
        out = table[output_index][i]
        row = (q3_ << 1) | q2_
        col = (q1_ << 1) | V
        gray_map = [0, 1, 3, 2]
        kmap[gray_map[row]][gray_map[col]] = out
    return kmap

if __name__ == "__main__":
    print("Таблица истинности цифрового устройства:")
    print_truth_table(DIGITAL_DEVICE_TRUTH_TABLE)

    kmap_h1 = build_kmap_4vars(DIGITAL_DEVICE_TRUTH_TABLE, output_index=9)
    kmap_h2 = build_kmap_4vars(DIGITAL_DEVICE_TRUTH_TABLE, output_index=8)
    kmap_h3 = build_kmap_4vars(DIGITAL_DEVICE_TRUTH_TABLE, output_index=7)

    variables4 = ["q3'", "q2'", "q1'", "V"]

    print("\nМинимизация h1:")
    print(f'ДНФ: {get_boolean_expression(kmap_h1, variables4, mode="sdnf")}')

    print("\nМинимизация h2:")
    print(f'ДНФ: {get_boolean_expression(kmap_h2, variables4, mode="sdnf")}')

    print("\nМинимизация h3:")
    print(f'ДНФ: {get_boolean_expression(kmap_h3, variables4, mode="sdnf")}')
