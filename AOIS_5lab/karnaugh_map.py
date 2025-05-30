from logic_solver import *


def is_power_of_two(n):
    return (n & (n - 1)) == 0 and n != 0


def get_rectangle_cells(matrix, start_row, start_col, end_row, end_col):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    cells = set()

    if start_row <= end_row:
        row_range = range(start_row, end_row + 1)
    else:
        row_range = list(range(start_row, rows)) + list(range(0, end_row + 1))

    if start_col <= end_col:
        col_range = range(start_col, end_col + 1)
    else:
        col_range = list(range(start_col, cols)) + list(range(0, end_col + 1))

    for i in row_range:
        for j in col_range:
            cells.add((i, j))

    return cells


def find_all_rectangles(matrix, mode="sdnf"):
    rows = len(matrix)
    if rows == 0:
        return []
    cols = len(matrix[0])
    rectangles = []
    target = 1 if mode == "sdnf" else 0

    for start_row in range(rows):
        for start_col in range(cols):
            if matrix[start_row][start_col] != target:
                continue

            for height in range(1, rows + 1):
                for width in range(1, cols + 1):
                    for dr in [0, -rows]:
                        for dc in [0, -cols]:
                            end_row = (start_row + height - 1 + dr) % rows
                            end_col = (start_col + width - 1 + dc) % cols
                            cells = get_rectangle_cells(matrix, start_row, start_col, end_row, end_col)

                            valid = True
                            for i, j in cells:
                                if matrix[i][j] != target:
                                    valid = False
                                    break

                            if valid and is_power_of_two(len(cells)):
                                rectangles.append((cells, len(cells)))
    return rectangles


def filter_unique_rectangles(rectangles):
    sorted_rects = sorted(rectangles, key=lambda x: (-x[1], min(x[0])))
    unique = []
    covered_cells = set()

    for cells, area in sorted_rects:
        new_cells = cells - covered_cells
        if new_cells:
            unique.append((cells, area))
            covered_cells.update(cells)
    return unique


def select_non_overlapping_rectangles(matrix, rectangles, mode="sdnf"):
    target = 1 if mode == "sdnf" else 0
    covered = set()
    selected = []
    sorted_rects = sorted(rectangles, key=lambda x: (-x[1], min(x[0])))

    for cells, area in sorted_rects:
        has_new = False
        for cell in cells:
            i, j = cell
            if matrix[i][j] == target and cell not in covered:
                has_new = True
                break

        if has_new:
            selected.append((cells, area))
            covered.update(cells)
    return remove_redundant_rectangles(matrix, selected, mode)


def remove_redundant_rectangles(matrix, selected_rectangles, mode="sdnf"):
    if not selected_rectangles:
        return selected_rectangles

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    target = 1 if mode == "sdnf" else 0

    def is_redundant(rect_idx):
        covered = [[False for _ in range(cols)] for _ in range(rows)]
        for i, rect in enumerate(selected_rectangles):
            if i == rect_idx:
                continue
            cells, _ = rect
            for x, y in cells:
                if matrix[x][y] == target:
                    covered[x][y] = True

        cells, _ = selected_rectangles[rect_idx]
        for x, y in cells:
            if matrix[x][y] == target and not covered[x][y]:
                return False
        return True

    to_remove = set()
    for i in reversed(range(len(selected_rectangles))):
        if is_redundant(i):
            to_remove.add(i)

    return [rect for idx, rect in enumerate(selected_rectangles) if idx not in to_remove]


def find_islands_torus(matrix, mode="sdnf"):
    rectangles = find_all_rectangles(matrix, mode)
    unique_rectangles = filter_unique_rectangles(rectangles)
    selected_rectangles = select_non_overlapping_rectangles(matrix, unique_rectangles, mode)

    return selected_rectangles


def split_matrix_two_parts(matrix):
    left = [row[:4] for row in matrix]
    right = [row[4:] for row in matrix]
    return left, right


def mirror_matrix_vertically(matrix):
    return [row[::-1] for row in matrix]


def find_matching_matrix(matrix, mode="sdnf"):
    left = [row[:4] for row in matrix]
    right = [row[4:] for row in matrix]
    mirrored_right = mirror_matrix_vertically(right)

    matching = []
    for i in range(4):
        row_match = []
        for j in range(4):
            if mode == "sdnf":
                if left[i][j] == 1 and mirrored_right[i][j] == 1:
                    row_match.append(1)
                else:
                    row_match.append(0)
            else:
                if left[i][j] == 0 and mirrored_right[i][j] == 0:
                    row_match.append(0)
                else:
                    row_match.append(1)
        matching.append(row_match)
    return matching


def transform_coords(groups, col_offset):
    transformed = []
    for cells, area in groups:
        new_cells = set()
        for i, j in cells:
            new_cells.add((i, j + col_offset))
        transformed.append((new_cells, area))
    return transformed


def add_mirrored_coordinates_to_groups(groups):
    extended_groups = []
    for cells, area in groups:
        mirrored_cells = set()
        for i, j in cells:
            mirrored_j = 7 - j
            mirrored_cells.add((i, mirrored_j))
        combined_cells = cells.union(mirrored_cells)
        extended_groups.append((combined_cells, area * 2))
    return extended_groups


def find_islands_torus_5vars(matrix, mode="sdnf"):
    left, right = split_matrix_two_parts(matrix)

    left_groups_raw = find_islands_torus(left, mode)
    left_groups = transform_coords(left_groups_raw, 0)

    right_groups_raw = find_islands_torus(right, mode)
    right_groups = transform_coords(right_groups_raw, 4)

    matching = find_matching_matrix(matrix, mode)

    matching_groups = find_islands_torus(matching, mode)

    matching_sym = add_mirrored_coordinates_to_groups(matching_groups)

    all_groups = left_groups + right_groups + matching_sym

    unique_groups = filter_unique_rectangles(all_groups)
    selected_groups = select_non_overlapping_rectangles(matrix, unique_groups, mode)

    return selected_groups


def generate_gray_code(bits):
    if bits == 0:
        return [0]
    gray = generate_gray_code(bits - 1)
    return gray + [(1 << (bits - 1)) | x for x in reversed(gray)]


def get_variable_sequences(length):
    bits = max(1, (length - 1).bit_length())
    gray = generate_gray_code(bits)
    sequences = []
    for i in range(bits):
        seq = []
        for num in gray[:length]:
            bit = (num >> (bits - 1 - i)) & 1
            seq.append(bit)
        sequences.append(seq)
    return sequences


def get_literals_for_cell_group(cells, row_seqs, col_seqs, var_names, mode="sdnf"):
    if not cells:
        return None

    rows = {i for i, j in cells}
    cols = {j for i, j in cells}

    literals = []

    for i, seq in enumerate(row_seqs):
        first_val = seq[next(iter(rows))]
        uniform = all(seq[r] == first_val for r in rows)
        if uniform:
            if mode == "scnf":
                first_val = 1 - first_val

            literal = f"!{var_names[i]}" if first_val == 0 else var_names[i]
            literals.append(literal)

    for i, seq in enumerate(col_seqs):
        col_var_index = len(row_seqs) + i
        first_val = seq[next(iter(cols))]
        uniform = all(seq[c] == first_val for c in cols)
        if uniform:
            if mode == "scnf":
                first_val = 1 - first_val

            literal = f"!{var_names[col_var_index]}" if first_val == 0 else var_names[col_var_index]
            literals.append(literal)

    return literals


def get_expression_for_rectangles(variables, rectangles, rows, cols, mode="sdnf"):
    if not rectangles:
        return "0" if mode == "sdnf" else "1"

    row_seqs = get_variable_sequences(rows)
    col_seqs = get_variable_sequences(cols)

    var_names = variables[:len(row_seqs) + len(col_seqs)]

    terms = []
    for group in rectangles:
        cells, area = group
        term = get_literals_for_cell_group(cells, row_seqs, col_seqs, var_names, mode)
        if term:
            if mode == "sdnf":
                term = "*".join(term)
            else:
                term = "+".join(term)
            terms.append(term)

    unique_terms = []
    seen = set()
    for term in terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)

    if mode == "sdnf":

        return " + ".join(f"({term})" for term in unique_terms) if unique_terms else "0"
    else:

        return " * ".join(f"({term})" for term in unique_terms) if unique_terms else "1"


def get_boolean_expression(matrix, variables, mode="sdnf"):
    if not matrix:
        return "0" if mode == "sdnf" else "1"

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    if rows == 4 and cols == 8:
        rectangles = find_islands_torus_5vars(matrix, mode)
    else:
        rectangles = find_islands_torus(matrix, mode)

    expression = get_expression_for_rectangles(variables, rectangles, rows, cols, mode)
    return expression


def build_karnaugh_map(index_form, variables, truth_table):
    n = len(variables)
    if n < 2 or n > 5:
        raise ValueError("Поддерживаются только от 2 до 5 переменных")

    if n == 2:
        row_vars, col_vars = [variables[0]], [variables[1]]
    elif n == 3:
        row_vars, col_vars = [variables[0]], variables[1:]
    elif n == 4:
        row_vars, col_vars = variables[:2], variables[2:]
    else:
        row_vars, col_vars = variables[:2], variables[2:]

    row_gray = gray_code(len(row_vars))
    col_gray = gray_code(len(col_vars))

    int_index_form = [int(val) if isinstance(val, str) else val for val in index_form]
    table_index = {tuple(vals): val for vals, val in zip(truth_table, int_index_form)}

    print("     ", end="")
    for col in col_gray:
        print(col, end=" ")
    print()

    kmap_matrix = []
    for row in row_gray:
        print(row, end=" ")
        row_values = []
        for col in col_gray:
            full = row + col
            key = tuple(int(x) for x in full)
            val = table_index.get(key, 0)
            print(f"  {val}", end="")
            row_values.append(val)
        kmap_matrix.append(row_values)
        print()

    return kmap_matrix


def gray_code(n):
    if n == 0:
        return ['']
    prev = gray_code(n - 1)
    return ['0' + x for x in prev] + ['1' + x for x in reversed(prev)]


def process_formula(formula):
    postfix_formula = to_postfix(formula)
    variables = sorted(set(c for c in formula if c.isalnum()))
    truth_table = generate_truth_table(variables)

    index_form = []
    for values in truth_table:
        var_values = dict(zip(variables, values))
        operations_result = evaluate_postfix(postfix_formula, var_values)
        result = operations_result[-1][1] if operations_result else 0
        index_form.append('1' if result == 1 else '0')

    matrix = build_karnaugh_map(index_form, variables, truth_table)

    print("\nМинимальная ДНФ:")
    sdnf = get_boolean_expression(matrix, variables, mode="sdnf")
    print(sdnf)
    print("===================================================================")
    print("\nМинимальная КНФ:")
    scnf = get_boolean_expression(matrix, variables, mode="scnf")
    print(scnf)