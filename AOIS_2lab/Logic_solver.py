from Validator import LogicalExpressionChecker  # Новый импорт

class LogicSolver:
    def __init__(self, rpn_expr):
        self.rpn_expr = rpn_expr
        self._allowed_vars = LogicalExpressionChecker._ALLOWED_VARS  # Используем новую константу

    def compute(self, values):
        stack = []
        for token in self.rpn_expr:
            if token in self._allowed_vars:  # Используем сохранённый набор переменных
                stack.append(values[token])
            elif token == '!':
                stack.append(not stack.pop())
            elif token == '&':
                right, left = stack.pop(), stack.pop()
                stack.append(left and right)
            elif token == '|':
                right, left = stack.pop(), stack.pop()
                stack.append(left or right)
            elif token == '->':
                right, left = stack.pop(), stack.pop()
                stack.append((not left) or right)
            elif token == '~':
                right, left = stack.pop(), stack.pop()
                stack.append(left == right)
        return stack[0] if stack else None