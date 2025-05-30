from itertools import product


def binary_to_decimal(binary_str):
    decimal = 0
    for i, bit in enumerate(reversed(binary_str)):
        decimal += int(bit) * (2 ** i)
    return decimal



def to_postfix(formula):
    precedence = {
        '!': 4,
        '*': 3,
        '+': 2,
        '>': 1,
        '~': 0,
    }

    stack = []
    output = []

    for char in formula:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif char in precedence:
            while (stack and stack[-1] != '(' and
                   precedence.get(char, -1) <= precedence.get(stack[-1], -1)):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


def negation(x):
    return 1 if x == 0 else 0


def conjunction(x, y):
    return 1 if x == 1 and y == 1 else 0


def disjunction(x, y):
    return 1 if x == 1 or y == 1 else 0


def implication(x, y):
    return 1 if x == 0 or y == 1 else 0


def equivalence(x, y):
    return 1 if x == y else 0


def evaluate_postfix(postfix_formula, var_values):
    stack = []
    operations = []

    for char in postfix_formula:
        if char.isalnum():
            stack.append(var_values[char])
        elif char == '!':
            x = stack.pop()
            result = negation(x)
            stack.append(result)
            operations.append(('!', result))
        elif char == '*':
            y = stack.pop()
            x = stack.pop()
            result = conjunction(x, y)
            stack.append(result)
            operations.append(('*', result))
        elif char == '+':
            y = stack.pop()
            x = stack.pop()
            result = disjunction(x, y)
            stack.append(result)
            operations.append(('+', result))
        elif char == '>':
            y = stack.pop()
            x = stack.pop()
            result = implication(x, y)
            stack.append(result)
            operations.append(('>', result))
        elif char == '~':
            y = stack.pop()
            x = stack.pop()
            result = equivalence(x, y)
            stack.append(result)
            operations.append(('~', result))

    return operations


def generate_truth_table(variables):
    return list(product([0, 1], repeat=len(variables)))


def print_table(variables, truth_table, postfix_formula):
    for values in truth_table:
        var_values = dict(zip(variables, values))
        operations_result = evaluate_postfix(postfix_formula, var_values)

        row = list(values) + [op[1] for op in operations_result]
        print("\t".join(map(str, row)))


def get_sdnf_sknf(variables, truth_table, postfix_formula):
    sdnf_terms = []
    sknf_terms = []

    for values in truth_table:
        var_values = dict(zip(variables, values))
        operations_result = evaluate_postfix(postfix_formula, var_values)
        result = operations_result[-1][1]

        term_sdnf = []
        term_sknf = []

        for var, val in var_values.items():
            term_sdnf.append(var if val == 1 else f"!{var}")
            term_sknf.append(var if val == 0 else f"!{var}")

        if result == 1:
            sdnf_terms.append('(' + '*'.join(term_sdnf) + ')')
        else:
            sknf_terms.append('(' + '+'.join(term_sknf) + ')')

    return '+'.join(sdnf_terms), '*'.join(sknf_terms)


def get_numeric_forms(truth_table, postfix_formula, variables):
    sdnf_indices = []
    sknf_indices = []

    for idx, values in enumerate(truth_table):
        var_values = dict(zip(variables, values))
        operations_result = evaluate_postfix(postfix_formula, var_values)
        result = operations_result[-1][1]

        if result == 1:
            sdnf_indices.append(idx)
        else:
            sknf_indices.append(idx)

    return sdnf_indices, sknf_indices


def get_index_form(truth_table, postfix_formula, variables):
    index_form = []
    for values in truth_table:
        var_values = dict(zip(variables, values))
        operations_result = evaluate_postfix(postfix_formula, var_values)
        result = operations_result[-1][1]
        index_form.append('1' if result == 1 else '0')
    return binary_to_decimal(''.join(index_form))