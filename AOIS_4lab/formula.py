import re
from itertools import product


class Formula:
    MAX_BITS = 7

    def __init__(self, formula):
        self.operators = {
            "!": {"priority": 4, "unary": True},
            "&": {"priority": 3, "unary": False},
            "|": {"priority": 2, "unary": False},
            "->": {"priority": 1, "unary": False},
            "~": {"priority": 0, "unary": False},
        }
        self.expression = formula.replace('∨', '|').replace(
            '∧', '&').replace('→', '->').replace('↔', '~')


    @staticmethod
    def binary_to_decimal_number(binary):
        decimal = 0
        length = len(binary)
        for i in range(length):
            if binary[i] == '1':
                decimal += 2 ** (length - i - 1)
        return decimal

    def get_variables(self):
        return sorted(set(re.findall(r'\b[a-zA-Z]+\b', self.expression)))

    def combinations(self):
        variables = self.get_variables()
        for combination in product([False, True], repeat=len(variables)):
            yield dict(zip(variables, combination))

    def tokenize(self):
        tokens = []
        i = 0
        while i < len(self.expression):
            if self.expression[i] == '-' and i + 1 < len(self.expression) and self.expression[i + 1] == '>':
                tokens.append('->')
                i += 2
            elif self.expression[i] in "()!&|~":
                tokens.append(self.expression[i])
                i += 1
            elif self.expression[i].isalpha():
                var = []
                while i < len(self.expression) and (self.expression[i].isalpha() or self.expression[i].isdigit()):
                    var.append(self.expression[i])
                    i += 1
                tokens.append(''.join(var))
            else:
                i += 1
        return tokens

    def to_postfix(self, tokens):
        output = []
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            elif token in self.operators:
                while stack and stack[-1] != '(' and self.operators[token]["priority"] <= self.operators.get(stack[-1], {"priority": -1})["priority"]:
                    output.append(stack.pop())
                stack.append(token)
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate_postfix(self, postfix, variables):
        stack = []
        for token in postfix:
            if token in self.operators:
                op = self.operators[token]
                if op["unary"]:
                    a = stack.pop()
                    result = not a
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == '&':
                        result = a and b
                    elif token == '|':
                        result = a or b
                    elif token == '->':
                        result = (not a) or b
                    elif token == '~':
                        result = a == b
                stack.append(result)
            else:
                stack.append(variables[token])
        return stack[0]

    def evaluate_of_expr(self, **variables):
        tokens = self.tokenize()
        missing = set(t for t in tokens if t.isalpha()) - set(variables.keys())
        if missing:
            raise ValueError(f"Не указаны переменные: {missing}")
        postfix = self.to_postfix(tokens)
        return self.evaluate_postfix(postfix, variables)

    def create_table_of_truth(self):
        variables = self.get_variables()
        combinations = list(self.combinations())
        result_of_expr = []
        table = []
        for combo in combinations:
            result = self.evaluate_of_expr(**combo)
            result_of_expr.append(result)
            row = [combo[var] for var in variables] + [result]
            table.append(row)
        return table, variables + ["Result"], result_of_expr

    def to_cnf(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        cnf = []
        for row in table:
            if not row[-1]:
                clause = []
                for i, var in enumerate(variables):
                    clause.append(f'¬{var}' if row[i] else var)
                cnf.append(f'({" ∨ ".join(clause)})')
        return " ∧ ".join(cnf) if cnf else "True"

    def to_dnf(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        dnf = []
        for row in table:
            if row[-1]:
                clause = []
                for i, var in enumerate(variables):
                    clause.append(var if row[i] else f'¬{var}')
                dnf.append(f'({" ∧ ".join(clause)})')
        return " ∨ ".join(dnf) if dnf else "False"

    def get_number_forms(self):
        table, headers, result_of_expr = self.create_table_of_truth()
        variables = headers[:-1]
        disjunction = []
        conjunction = []
        for row in table:
            binary = ''.join(str(int(v)) for v in row[:-1])
            decimal = self.binary_to_decimal_number(binary)
            if row[-1]:
                disjunction.append(decimal)
            else:
                conjunction.append(decimal)
        return (f"({','.join(map(str, disjunction))}) ∨\n"
                f"({','.join(map(str, conjunction))}) ∧")
