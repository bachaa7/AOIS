from Validator import LogicalExpressionChecker
from rpn_converter import ReversePolishNotationConverter  # Используем новый конвертер
from Truth_table_processor import TruthTableProcessor
from Table_generate import TruthTableGenerator


def main():
    # Получаем выражение от пользователя
    expression = input("Введите логическое выражение: ").strip()

    # Первичная валидация выражения
    try:
        LogicalExpressionChecker.is_valid(expression)
    except ValueError as e:
        print(f"Ошибка в выражении: {e}")
        return

    try:
        # Дополнительная проверка (можно убрать дублирование)
        LogicalExpressionChecker.is_valid(expression)

        # Создаем генератор таблицы истинности
        truth_gen = TruthTableGenerator(expression)

        # Выводим таблицу истинности
        print("\nТаблица истинности:")
        truth_gen.display_table()

        # Конвертируем в обратную польскую запись
        rpn_converter = ReversePolishNotationConverter()
        rpn_expression = rpn_converter.transform(expression)  # Используем новый метод
        print(f"\nОбратная польская нотация: {' '.join(rpn_expression)}")

        # Генерируем полную таблицу истинности для анализа
        truth_table = truth_gen.generate_truth_table()

        # Анализируем нормальные формы
        processor = TruthTableProcessor(truth_table, truth_gen.variables)
        forms = processor.get_normal_forms()

        # Выводим результаты
        print("\nНормальные формы:")
        print(f"СДНФ: {forms['СДНФ']}")
        print(f"СКНФ: {forms['СКНФ']}")
        print(f"Индексы СДНФ: {forms['СДНФ Индексы']} |")
        print(f"Индексы СКНФ: {forms['СКНФ Индексы']} &")

        # Выводим индексную форму
        index_data = truth_gen.compute_index_form()
        print("\nИндексная форма:")
        print(f"Бинарная: {index_data['binary']}")
        print(f"Десятичная: {index_data['decimal']}")

    except ValueError as e:
        print(f"Ошибка при обработке: {e}")


if __name__ == "__main__":
    main()