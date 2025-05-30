import Tests
from Validator import ExpressionValidator
from rpn_converter import RPNConverter
from Logic_solver import LogicSolver
from Table_generate import TruthTableGenerator
from Truth_table_processor import TruthTableProcessor


class TestPipeline(unittest.TestCase):

    def test_rpn_conversion(self):
        # Тест на корректность преобразования в обратную польскую нотацию (RPN)
        expr = "!a | (b -> c)"
        converter = RPNConverter(expr)
        rpn = converter.convert_to_rpn()
        self.assertEqual(rpn, ['a', '!', 'b', 'c', '->', '|'])

    def test_logic_solver(self):
        # Тест на решение логического выражения в RPN
        rpn = ['a', 'b', '&']
        solver = LogicSolver(rpn)
        values = {'a': True, 'b': False}
        self.assertFalse(solver.compute(values))  # a & b = False

        rpn = ['a', '!', 'b', 'c', '&', '|']
        solver = LogicSolver(rpn)
        values = {'a': False, 'b': True, 'c': True}
        self.assertTrue(solver.compute(values))  # !a | (b & c) = True

    def test_truth_table_generation(self):
        # Тест на генерацию таблицы истинности
        expr = "a -> b"
        generator = TruthTableGenerator(expr)
        table = generator.generate_truth_table()
        self.assertEqual(len(table), 4)  # 2 переменные => 4 комбинации

        # Проверим хотя бы одну строку результата
        for row in table:
            self.assertIn('a', row[0])  # Проверим, что переменная 'a' есть
            self.assertIn('b', row[0])  # Проверим, что переменная 'b' есть
            self.assertIsInstance(row[2], bool)  # Проверим, что результат - булевое значение

    def test_normal_forms(self):
        # Тест на получение СДНФ и СКНФ
        expr = "a & b"
        generator = TruthTableGenerator(expr)
        table = generator.generate_truth_table()
        processor = TruthTableProcessor(table, generator.variables)
        forms = processor.get_normal_forms()

        self.assertIn("СДНФ", forms)  # Проверяем наличие СДНФ
        self.assertIn("СКНФ", forms)  # Проверяем наличие СКНФ
        self.assertTrue(forms["СДНФ"].startswith("("))  # СДНФ должно начинаться с '('
        self.assertTrue(forms["СКНФ"].startswith("("))  # СКНФ должно начинаться с '('

    def test_index_form(self):
        # Тест на получение бинарной и десятичной формы
        expr = "!a | b"
        generator = TruthTableGenerator(expr)
        result = generator.compute_index_form()
        self.assertIn("binary", result)  # Проверяем, что есть бинарное представление
        self.assertIn("decimal", result)  # Проверяем, что есть десятичное представление
        self.assertTrue(result["binary"].isdigit())  # Проверяем, что бинарная форма состоит из цифр
        self.assertTrue(isinstance(result["decimal"], int))  # Проверяем, что десятичная форма - целое число

    def test_invalid_expression(self):
        # Тест на валидацию некорректного выражения
        invalid_expr = "a & b |"
        with self.assertRaises(ValueError):
            ExpressionValidator.validate(invalid_expr)  # Выражение не может заканчиваться оператором

        invalid_expr2 = "a & & b"
        with self.assertRaises(ValueError):
            ExpressionValidator.validate(invalid_expr2)  # Ожидается оператор между переменными

        invalid_expr3 = "(a & b"
        with self.assertRaises(ValueError):
            ExpressionValidator.validate(invalid_expr3)  # Несбалансированные скобки


if __name__ == "__main__":
    unittest.main()
