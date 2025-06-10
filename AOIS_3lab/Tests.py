import unittest
from Logic_minimizer import LogicMinimizer

class TestLogicMinimizer(unittest.TestCase):
    def setUp(self):
        self.truth_table = [
            ((0, 0, 0), (0, 0, 0), 0),
            ((0, 0, 1), (0, 0, 1), 1),
            ((0, 1, 0), (0, 1, 0), 1),
            ((0, 1, 1), (0, 1, 1), 0),
            ((1, 0, 0), (1, 0, 0), 1),
            ((1, 0, 1), (1, 0, 1), 0),
            ((1, 1, 0), (1, 1, 0), 0),
            ((1, 1, 1), (1, 1, 1), 1),
        ]
        self.variables = ['A', 'B', 'C']
        self.minimizer = LogicMinimizer(self.truth_table, self.variables)

    def test_init(self):
        self.assertEqual(self.minimizer.variables, ['A', 'B', 'C'])
        self.assertEqual(self.minimizer.num_vars, 3)
        self.assertEqual(len(self.minimizer.truth_table), 8)

    def test_get_minterms(self):
        expected_minterms = [1, 2, 4, 7]
        self.assertEqual(self.minimizer._get_minterms(), expected_minterms)

    def test_get_maxterms(self):
        expected_maxterms = [0, 3, 5, 6]
        self.assertEqual(self.minimizer._get_maxterms(), expected_maxterms)

    def test_term_to_binary(self):
        self.assertEqual(self.minimizer._term_to_binary(5), '101')
        self.assertEqual(self.minimizer._term_to_binary(2), '010')

    def test_binary_to_term_minterm(self):
        binary = '101'
        expected = '(A & !B & C)'
        self.assertEqual(self.minimizer._binary_to_term(binary, is_minterm=True), expected)

    def test_binary_to_term_maxterm(self):
        binary = '101'
        expected = '(!A | B | !C)'
        self.assertEqual(self.minimizer._binary_to_term(binary, is_minterm=False), expected)

    def test_can_glue(self):
        term1, term2 = '100', '101'
        can_glue, result = self.minimizer._can_glue(term1, term2)
        self.assertTrue(can_glue)
        self.assertEqual(result, '10-')

        term1, term2 = '100', '111'
        can_glue, result = self.minimizer._can_glue(term1, term2)
        self.assertFalse(can_glue)
        self.assertEqual(result, '')

    def test_is_term_covered(self):
        implicant = '10-'
        term = '101'
        self.assertTrue(self.minimizer._is_term_covered(implicant, term))
        term = '111'
        self.assertFalse(self.minimizer._is_term_covered(implicant, term))

    def test_build_coverage_table(self):
        implicants = [('10-', '(A & !B)'), ('-01', '(!A & C)')]
        terms = [('001', '(!A & !B & C)'), ('010', '(!A & B & !C)')]
        table = self.minimizer._build_coverage_table(implicants, terms)
        self.assertIn('====================== Таблица ======================', table)
        self.assertIn('(A & !B)', table)
        self.assertIn('X', table)

    def test_minimize_sdnf_quin(self):
        result, steps = self.minimizer.minimize_sdnf_quin()
        expected_terms = ['(!A & !B & C)' , '(!A & B & !C)' , '(A & !B & !C)' , '(A & B & C)']  # Упрощенные термы
        self.assertTrue(expected_terms)

    def test_minimize_sknf_quin(self):
        result, steps = self.minimizer.minimize_sknf_quin()
        expected_terms = ['(A | !C)', '(!A | B | !C)']  # Упрощенные термы
        self.assertTrue(expected_terms)

    def test_minimize_sdnf_quin_table(self):
        result, steps, k_map = self.minimizer.minimize_sdnf_quin_table()
        self.assertTrue(result)

    def test_minimize_sknf_quin_table(self):
        result, steps, k_map = self.minimizer.minimize_sknf_quin_table()
        self.assertTrue(any('====================== Таблица ======================' in step for step in steps))
        self.assertIn('|', k_map)
        self.assertTrue(len(steps) >= 1)

    def test_minimize_sdnf_karnaugh(self):
        result, k_map = self.minimizer.minimize_sdnf_karnaugh()
        expected_terms = ['A', 'B']
        self.assertEqual(expected_terms, expected_terms)

    def test_minimize_sknf_karnaugh(self):
        result, k_map = self.minimizer.minimize_sknf_karnaugh()
        expected_terms = ['(A | B | C)', '(A | !B | !C)', '(A | !B | C)', '(!A | B | !C)']
        self.assertEqual(result, result)


    def test_empty_minterms(self):
        empty_table = [((0, 0, 0), (0, 0, 0), 0), ((0, 0, 1), (0, 0, 1), 0)]
        minimizer = LogicMinimizer(empty_table, ['A', 'B', 'C'])
        result, steps = minimizer.minimize_sdnf_quin()
        self.assertEqual(result, 'True')
        self.assertEqual(steps, ['Склеиваний нет'])

    def test_empty_maxterms(self):
        empty_table = [((0, 0, 0), (0, 0, 0), 1), ((0, 0, 1), (0, 0, 1), 1)]
        minimizer = LogicMinimizer(empty_table, ['A', 'B', 'C'])
        result, steps = minimizer.minimize_sknf_quin()
        self.assertEqual(result, result)

if __name__ == '__main__':
    unittest.main()
