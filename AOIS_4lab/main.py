from odv3 import odv3_table, build_sdnf_for_column
from KaMain import  *

def print_odv3_truth_and_sdnf():
    table = odv3_table()
    print("a b Bin | D Bout")
    print("--------------")
    for row in table:
        print(f"{row[0]} {row[1]} {row[2]}   | {row[3]}  {row[4]}")

    d_sdnf = build_sdnf_for_column(table, 3)
    bout_sdnf = build_sdnf_for_column(table, 4)

    print("\nСДНФ для D (Разность):")
    print(d_sdnf)

    print("\nСДНФ для Bout (Заём):")
    print(bout_sdnf)

if __name__ == "__main__":
    print_odv3_truth_and_sdnf()

    print_D8421_plus5_truth_table()
    # print_ODS_3_truth_table()
    for i, out_name in enumerate(["A'", "B'", "C'", "D'"]):
        process_minimization(i, out_name)