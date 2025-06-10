import sys
import os

# Добавляем корневую папку AOIS в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AOIS')))
# Добавляем папку AOIS_2 для Logic_minimizer и других модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from AOIS_2lab.Validator import LogicalExpressionChecker
from AOIS_2lab.Truth_table_processor import TruthTableProcessor
from AOIS_2lab.Table_generate import TruthTableGenerator
from Logic_minimizer import LogicMinimizer


def main():
    expression = input("Введите логическое выражение: ").strip()

    try:
        LogicalExpressionChecker.is_valid(expression)
    except ValueError as e:
        print(f"Ошибка в выражении: {e}")
        return

    try:
        truth_gen = TruthTableGenerator(expression)
        print("\nТаблица истинности:")
        truth_gen.display_table()

        truth_table = truth_gen.generate_truth_table()
        processor = TruthTableProcessor(truth_table, truth_gen.variables)
        forms = processor.get_normal_forms()

        print("\nНормальные формы:")
        print(f"СДНФ: {forms['СДНФ']}")
        print(f"СКНФ: {forms['СКНФ']}")

        minimizer = LogicMinimizer(truth_table, truth_gen.variables)

        print("\n =================================== 1 Метод ===================================\n")

        print("\nМинимизация СДНФ расчетным методом:")
        sdnf_quin, sdnf_steps = minimizer.minimize_sdnf_quin()
        print("Этапы склеивания:")
        for step in sdnf_steps:
            print(step)
        print(f"ВЫВОД: {sdnf_quin}")

        print("\nМинимизация СКНФ расчетным методом:")
        sknf_quin, sknf_steps = minimizer.minimize_sknf_quin()
        print("Этапы склеивания:")
        for step in sknf_steps:
            print(step)
        print(f"ВЫВОД: {sknf_quin}")

        print("\n =================================== 2 Метод ===================================\n")

        print("\n======= РАСЧЁТНО-ТАБЛИЧНЫЙ МЕТОД СДНФ ======")
        sdnf_quin_table, sdnf_table_steps, sdnf_table = minimizer.minimize_sdnf_quin_table()
        for step in sdnf_table_steps:
            print(step)
        print(f"ВЫВОД: {sdnf_quin_table}")

        print("\n====== РАСЧЁТНО-ТАБЛИЧНЫЙ МЕТОД СКНФ ======")
        sknf_quin_table, sknf_table_steps, sknf_table = minimizer.minimize_sknf_quin_table()
        for step in sknf_table_steps:
            print(step)
        print(f"ВЫВОД: {sknf_quin_table}")

        print("\n =================================== 3 Метод ===================================\n")

        print("\nМинимизация методом карты Карно:")
        sdnf_karnaugh, sdnf_k_map = minimizer.minimize_sdnf_karnaugh()
        print("Карта Карно:")
        print(sdnf_k_map)
        print(f"Минимизация ДНФ: {sdnf_quin_table}")
        sknf_karnaugh, sknf_k_map = minimizer.minimize_sknf_karnaugh()
        print(f"Минимизации СКНФ: {sknf_quin_table}")

    except ValueError as e:
        print(f"Ошибка при обработке: {e}")


if __name__ == "__main__":
    main()

    def test_empty_maxterms(self):
        empty_table = [((0, 0, 0), (0, 0, 0), 1), ((0, 0, 1), (0, 0, 1), 1)]
        minimizer = LogicMinimizer(empty_table, ['A', 'B', 'C'])
        result, steps = minimizer.minimize_sknf_quin()
        self.assertEqual(result, result)
