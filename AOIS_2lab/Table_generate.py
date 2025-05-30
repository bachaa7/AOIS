import itertools
from Validator import LogicalExpressionChecker
from rpn_converter import ReversePolishNotationConverter
from Logic_solver import LogicSolver


class TruthTableGenerator:
    def __init__(self, expression):
        self.expression = expression
        LogicalExpressionChecker.is_valid(expression)

        self.variables = sorted(set(c for c in expression if c in LogicalExpressionChecker._ALLOWED_VARS))
        self.rpn_converter = ReversePolishNotationConverter(
            allowed_vars=LogicalExpressionChecker._ALLOWED_VARS,
            operator_precedence={'!': 4, '~': 4, '&': 3, '|': 2, '->': 1}
        )
        self.subexpressions = []
        self.subexpression_strings = []
        self._parse_subexpressions()

    def _parse_subexpressions(self):
        """Разбирает выражение на подвыражения"""
        stack = []
        rpn_expr = self.rpn_converter.transform(self.expression)

        for token in rpn_expr:
            if token in self.variables:
                stack.append([token])
            elif token == '!':
                operand = stack.pop()
                new_expr = operand + [token]
                stack.append(new_expr)
                self.subexpressions.append(new_expr)
            else:
                right = stack.pop()
                left = stack.pop()
                new_expr = left + right + [token]
                stack.append(new_expr)
                self.subexpressions.append(new_expr)

        # Создаем строковые представления подвыражений
        self.subexpression_strings = [self._rpn_to_str(expr) for expr in self.subexpressions]

    def _rpn_to_str(self, rpn):
        """Конвертирует ОПН в инфиксную запись"""
        stack = []
        for token in rpn:
            if token in self.variables:
                stack.append(token)
            elif token == '!':
                stack.append(f"!{stack.pop()}")
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(f"({left} {token} {right})")
        return stack[0]

    def generate_truth_table(self):
        """Генерирует полную таблицу истинности"""
        table = []
        rpn_expr = self.rpn_converter.transform(self.expression)

        for values in itertools.product([False, True], repeat=len(self.variables)):
            var_values = dict(zip(self.variables, values))

            sub_results = []
            for sub_expr in self.subexpressions:
                solver = LogicSolver(sub_expr)
                sub_results.append(solver.compute(var_values))

            solver = LogicSolver(rpn_expr)
            final_result = solver.compute(var_values)

            table.append((var_values, sub_results, final_result))

        return table

    def compute_index_form(self):
        """Вычисляет индексную форму"""
        truth_table = self.generate_truth_table()
        binary = ''.join(str(int(row[2])) for row in truth_table)
        return {
            "binary": binary,
            "decimal": int(binary, 2)
        }

    def display_table(self):
        """Выводит форматированную таблицу истинности"""
        table = self.generate_truth_table()

        # Определяем ширину колонок
        headers = self.variables + self.subexpression_strings + ["Result"]
        col_width = max(len(h) for h in headers) + 2

        # Шапка таблицы
        header = " | ".join(h.center(col_width) for h in headers)
        print("\nТаблица истинности:")
        print(header)
        print("-" * len(header))

        # Строки данных
        for row in table:
            values = [str(int(row[0][var])) for var in self.variables]
            sub_results = [str(int(res)) for res in row[1]]
            line = " | ".join(v.center(col_width) for v in values + sub_results + [str(int(row[2]))])
            print(line)