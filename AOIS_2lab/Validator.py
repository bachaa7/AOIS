class LogicalExpressionChecker:
    """Проверяет корректность логических выражений с поддержкой скобок и операторов"""

    _ALLOWED_VARS = {'a', 'b', 'c', 'd', 'e'}
    _OPERATORS = {'!', '&', '|', '->', '~'}
    _VALID_CHARS = _ALLOWED_VARS | {'(', ')', ' ','-','>'} | set('!&|~')

    @classmethod
    def is_valid(cls, expression: str) -> bool:
        """Проверяет выражение на корректность"""
        expr = cls._prepare_expression(expression)
        cls._check_chars(expr)
        cls._check_parentheses(expr)
        cls._check_operators(expr)
        return True

    @classmethod
    def _prepare_expression(cls, expr: str) -> str:
        """Удаляет пробелы и проверяет пустоту"""
        expr = expr.replace(' ', '')
        if not expr:
            raise ValueError("Пустое выражение")
        return expr

    @classmethod
    def _check_chars(cls, expr: str):
        """Проверяет допустимость символов и корректность операторов (включая многосимвольные)"""
        i = 0
        while i < len(expr):
            if expr[i] in cls._ALLOWED_VARS or expr[i] in '()':
                i += 1
            elif expr[i] == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                i += 2  # это '->'
            elif expr[i] in '!&|~':
                i += 1
            else:
                raise ValueError(f"Недопустимый символ: '{expr[i]}'")

    @classmethod
    def _check_parentheses(cls, expr: str):
        """Проверяет баланс скобок"""
        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    break
        if balance != 0:
            raise ValueError("Несбалансированные скобки")

    @classmethod
    def _check_operators(cls, expr: str):
        """Проверяет корректность операторов"""
        i = 0
        n = len(expr)
        while i < n:
            if expr[i] == '-':
                if i + 1 >= n or expr[i + 1] != '>':
                    raise ValueError("Некорректный оператор '->'")
                i += 2
            elif expr[i] in cls._OPERATORS:
                i += 1
            elif expr[i] in cls._ALLOWED_VARS or expr[i] in '()':
                i += 1
            else:
                i += 1  # Уже проверено в _check_chars