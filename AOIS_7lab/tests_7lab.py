import unittest
from matrix import DiagonalMatrix
from io import StringIO
import sys

class TestDiagonalMatrix(unittest.TestCase):

    def setUp(self):
        self.dm = DiagonalMatrix()

    def test_write_and_read_word(self):
        word = [1 if i % 2 == 0 else 0 for i in range(16)]
        self.dm.write_word(3, word)
        result = self.dm.read_word(3)
        self.assertEqual(result, word)

    def test_read_column(self):
        matrix = [[i for _ in range(16)] for i in range(16)]
        self.dm.set_matrix(matrix)
        col = self.dm.read_column(5)
        expected = list(range(16))
        self.assertEqual(col, expected)

    def test_read_address_column(self):
        for i in range(16):
            word = [0]*16
            word[i] = 1
            self.dm.write_word(i, word)

        col = self.dm.read_address_column(0)
        expected = [1 if i == 0 else 0 for i in range(16)]
        self.assertEqual(col, expected)

    def test_logical_function_f7(self):
        col1 = [1]*16
        col2 = [0]*16
        self.dm.write_word(0, col1)
        self.dm.write_word(1, col2)
        self.dm.logical_function(0, 1, 7, 2)
        result = self.dm.read_word(2)
        self.assertEqual(result, [1]*16)

    def test_compare_words(self):
        w1 = [0, 1, 0, 0]
        w2 = [0, 1, 0, 0]
        self.assertEqual(self.dm.compare_words(w1, w2), 0)
        self.assertEqual(self.dm.compare_words([1, 0, 0, 0], w2), 1)
        self.assertEqual(self.dm.compare_words([0, 0, 0, 0], w2), -1)

    def test_compute_g_l_flags(self):
        word = [0]*16
        self.dm.write_word(0, word)
        g, l = self.dm.compute_g_l_flags([0]*16)
        self.assertEqual(g[0], 0)
        self.assertEqual(l[0], 0)

    def test_add_fields(self):
        # Формируем слово: V=110, A=1100, B=0111, S=00000
        word = [1,1,0, 1,1,0,0, 0,1,1,1, 0,0,0,0,0]
        self.dm.write_word(2, word)
        self.dm.add_fields([1,1,0])
        new_word = self.dm.read_word(2)
        expected = [1,1,0, 1,1,0,0, 0,1,1,1, 1,0,0,1,1]
        self.assertEqual(new_word, expected)

        base_word = [0] * 16
        self.dm.write_word(0, base_word)  # слово из всех нулей
        max_word = [1] * 16
        self.dm.write_word(1, max_word)  # слово из всех единиц

        mid_word = [0, 1] * 8
        for i in range(2, 16):
            self.dm.write_word(i, mid_word)



    def test_search_in_range_by_gl(self):
        low_key = [0] * 16
        high_key = [1] * 16

        # Записываем тестовые слова с разным содержимым
        self.dm.write_word(0, [0]*16)
        self.dm.write_word(1, [1]*16)
        self.dm.write_word(2, [0,1]*8)

        captured_output = StringIO()
        original_stdout = sys.stdout
        try:
            sys.stdout = captured_output  # Перенаправляем stdout в буфер
            self.dm.search_in_range_by_gl(low_key, high_key)
        finally:
            sys.stdout = original_stdout  # Восстанавливаем стандартный вывод

        output = captured_output.getvalue()

        # Проверяем, что в выводе есть ожидаемые слова
        self.assertIn("Слово 0: 0000000000000000", output)
        self.assertIn("Слово 1: 1111111111111111", output)
        self.assertIn("Слово 2: 0101010101010101", output)
        self.assertTrue(output.startswith("Слова в интервале:"))

if __name__ == '__main__':
    unittest.main()
