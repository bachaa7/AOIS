from matrix import DiagonalMatrix

def main():
    dm = DiagonalMatrix()

    print("Изначально пустая матрица:")
    dm.display()

    # Примеры слов
    s0 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    s1 = [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    s2 = [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    s3 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    # Записываем слова и отображаем матрицу после каждой записи
    print("Добавление слов в матрицу:")
    for i, word in enumerate([s0, s1, s2, s3]):
        dm.write_word(i, word)
        print(f"\nСлово {i+1} записано: {''.join(map(str, word))}\n")
    dm.display()


    print("Чтение слова:")
    word_index = 1
    word = dm.read_word(word_index)
    print(f"Слово {word_index}: {''.join(map(str, word))}")


    print("\nЧтение столбца:")
    col_index = 1
    column = dm.read_column(col_index)
    print(f"Столбец {col_index}: {''.join(map(str, column))}")

    bit_index = 3
    address_column = dm.read_address_column(bit_index)
    print(f"\nАдресный столбец {bit_index}: {''.join(map(str, address_column))}")


    # Демонстрация логических функций по обновленной логике
    print("\nПрименение логических функций:")

    # f7: дизъюнкция (ИЛИ)
    dm.logical_function(1, 2, 7, 4)
    print(f"Слово 4 (1 и 2) после f7 (x ∨ y): {''.join(map(str, dm.read_word(4)))}")

    # f8: операция Пирса (¬(x ∨ y))
    dm.logical_function(1, 2, 8, 5)
    print(f"Слово 5 (1 и 2) после f8 (¬(x ∨ y)): {''.join(map(str, dm.read_word(5)))}")

    # f2: запрет первого аргумента (¬x)
    dm.logical_function(1, 2, 2, 6)
    print(f"Слово 6 (1 и 2) после f2 (¬x): {''.join(map(str, dm.read_word(6)))}")

    # f13: импликация (¬x ∨ y)
    dm.logical_function(1, 2, 13, 7)
    print(f"Слово 7 (1 и 2) после f13 (¬x ∨ y): {''.join(map(str, dm.read_word(7)))}")




    print("\nСложение полей для V")
    v_key = [1, 1, 0]  # например, ключ 111
    dm.add_fields(v_key)

    print(f"Слова с V = {''.join(map(str, v_key))} после сложения:")
    for i in range(dm.size):
        word = dm.read_word(i)
        if word[:3] == v_key:
            print(f"Слово {i}: V: {''.join(map(str, word[:3]))}, "
                  f"A: {''.join(map(str, word[3:7]))}, "
                  f"B: {''.join(map(str, word[7:11]))}, "
                  f"S: {''.join(map(str, word[11:16]))}")


    print("\nФинальная матрица:")
    dm.display()

    print("\nПоиск слов в интервале:")
    low_key = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    high_key = [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    print(f"\n Интервал {low_key} до {high_key} ")
    dm.search_in_range_by_gl(low_key, high_key)


if __name__ == "__main__":
    main()
