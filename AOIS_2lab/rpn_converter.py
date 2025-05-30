class ReversePolishNotationConverter:
    """Конвертер логических выражений в обратную польскую нотацию"""

    def __init__(self, allowed_vars=None, operator_precedence=None):
        self.variables = allowed_vars or {'a', 'b', 'c', 'd', 'e'}
        self.precedence = operator_precedence or {
            '!': 4,
            '~': 4,
            '&': 3,
            '|': 2,
            '->': 1
        }

    def transform(self, logic_expression: str) -> list:
        """Основной метод преобразования выражения"""
        cleaned_expr = self._clean_expression(logic_expression)
        self._validate_expression(cleaned_expr)

        result = []
        operator_stack = []
        token_generator = self._tokenize(cleaned_expr)

        for token in token_generator:
            if self._is_variable(token):
                result.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                self._process_closing_parenthesis(operator_stack, result)
            else:
                self._process_operator(token, operator_stack, result)

        self._empty_operator_stack(operator_stack, result)
        return result

    def _clean_expression(self, expr: str) -> str:
        """Удаление пробелов и проверка на пустоту"""
        expr = expr.replace(' ', '')
        if not expr:
            raise ValueError("Пустое логическое выражение")
        return expr

    def _validate_expression(self, expr: str):
        """Проверка допустимости выражения по токенам, включая многосимвольные операторы"""
        allowed_tokens = self.variables | {'(', ')', '!', '&', '|', '~', '->'}
        for token in self._tokenize(expr):
            if token not in allowed_tokens:
                raise ValueError(f"Выражение содержит недопустимый токен: '{token}'")

    def _tokenize(self, expr: str):
        """Генератор токенов с обработкой многосимвольных операторов"""
        i = 0
        n = len(expr)
        while i < n:
            if expr[i] == '-' and i + 1 < n and expr[i + 1] == '>':
                yield '->'
                i += 2
            else:
                yield expr[i]
                i += 1

    def _is_variable(self, token: str) -> bool:
        """Проверка является ли токен переменной"""
        return token in self.variables

    def _process_closing_parenthesis(self, stack: list, output: list):
        """Обработка закрывающей скобки"""
        while stack and stack[-1] != '(':
            output.append(stack.pop())
        if not stack:
            raise ValueError("Несбалансированные скобки")
        stack.pop()  # Удаляем открывающую скобку

    def _process_operator(self, operator: str, stack: list, output: list):
        """Обработка операторов с учетом приоритетов"""
        while (stack and stack[-1] != '(' and
               self.precedence.get(stack[-1], 0) >= self.precedence.get(operator, 0)):
            output.append(stack.pop())
        stack.append(operator)

    def _empty_operator_stack(self, stack: list, output: list):
        """Перенос оставшихся операторов в выходную очередь"""
        while stack:
            op = stack.pop()
            if op == '(':
                raise ValueError("Несбалансированные скобки")
            output.append(op)