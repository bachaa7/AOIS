class DiagonalMatrix:
    def __init__(self):
        self.size = 16
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]


    def set_matrix(self, matrix):
        if len(matrix) != self.size or any(len(row) != self.size for row in matrix):
            raise ValueError("Матрица должна быть 16x16")
        self.matrix = [row[:] for row in matrix]

    def read_word(self, word_index):
        """Считать слово по индексу (вертикально со сдвигом строк)."""
        if not 0 <= word_index < self.size:
            raise ValueError("Недопустимый индекс слова")
        result = []
        col = word_index  # столбец фиксирован для слова
        for i in range(self.size):
            row = (i + word_index) % self.size  # циклический сдвиг строк на word_index
            result.append(self.matrix[row][col])
        return result

    def read_column(self, col_index):
        """Считать адресный столбец по индексу (просто вернуть столбец без сдвигов)."""
        if not 0 <= col_index < self.size:
            raise ValueError("Недопустимый индекс столбца")
        return [self.matrix[i][col_index] for i in range(self.size)]

    def write_word(self, word_index, word):
        """Записать слово по индексу (вертикально со сдвигом строк)."""
        if len(word) != self.size:
            raise ValueError("Длина слова должна быть 16")
        if not all(bit in (0, 1) for bit in word):
            raise ValueError("Слово должно содержать только 0 и 1")
        col = word_index
        for i in range(self.size):
            row = (i + word_index) % self.size
            self.matrix[row][col] = word[i]

    def read_address_column(self, bit_index):
        if not 0 <= bit_index < self.size:
            raise ValueError("Недопустимый индекс разряда")

        result = []
        for j in range(self.size):
            row = (j + bit_index) % self.size
            col = j
            result.append(self.matrix[row][col])
        return result

    def logical_function(self, col1, col2, func_index, result_word_index):
        if not (0 <= col1 < self.size and 0 <= col2 < self.size):
            raise ValueError("Недопустимые индексы столбцов")
        if not 0 <= result_word_index < self.size:
            raise ValueError("Недопустимый индекс слова для записи результата")

        # Логические функции
        def f7(x, y):
            return x | y

        def f8(x, y):
            return int(not (x or y))  # Операция Пирса (NOR)

        def f2(x, y):
            return int(not x)

        def f13(x, y):
            return int((not x) or y)

        func_map = {7: f7, 8: f8, 2: f2, 13: f13}
        if func_index not in func_map:
            raise ValueError("Недопустимый индекс функции")

        col1_data = self.read_column(col1)
        col2_data = self.read_column(col2)

        # Приводим значения к 0 и 1
        col1_data = [int(bool(x)) for x in col1_data]
        col2_data = [int(bool(x)) for x in col2_data]

        # Применяем функцию
        result = [func_map[func_index](x, y) for x, y in zip(col1_data, col2_data)]
        self.write_word(result_word_index, result)

###################### g l

    def compare_words(self, word, key):
        """Сравнивает два слова побитно, возвращает:
           1 — если word > key
           -1 — если word < key
           0 — если равны
        """
        for w_bit, k_bit in zip(word, key):
            if w_bit > k_bit:
                return 1
            elif w_bit < k_bit:
                return -1
        return 0

    def compute_g_l_flags(self, key):
        """Возвращает списки флагов g и l для всех слов"""
        g = [0] * self.size
        l = [0] * self.size
        for j in range(self.size):
            word = self.read_word(j)
            cmp = self.compare_words(word, key)
            if cmp == 1:
                g[j] = 1
            elif cmp == -1:
                l[j] = 1
        return g, l

    def search_in_range_by_gl(self, low_key, high_key):
        """Поиск всех слов, заключённых в интервал [low_key, high_key]"""
        if len(low_key) != self.size or len(high_key) != self.size:
            raise ValueError("Ключи должны быть длиной в одно слово")

        g_low, l_low = self.compute_g_l_flags(low_key)
        g_high, l_high = self.compute_g_l_flags(high_key)

        print("Слова в интервале:")
        for j in range(self.size):
            # Условие: слово >= low и слово <= high
            # greater_equal_low = g_low[j] or self.compare_words(self.read_word(j), low_key) == 0
            # less_equal_high = not g_high[j]
            # if greater_equal_low and less_equal_high:
            word_j = self.read_word(j)
            greater_equal_low = g_low[j] or self.compare_words(word_j, low_key) == 0
            less_equal_high = not g_high[j]
            if greater_equal_low and less_equal_high:
                print(f"Слово {j}: {''.join(map(str, self.read_word(j)))}")

    def add_fields(self, v_key):
        """Сложить поля Aj и Bj в словах Sj, где первые 3 бита совпадают с v_key."""

        if len(v_key) != 3 or not all(bit in (0, 1) for bit in v_key):
            raise ValueError("Ключ V должен быть 3-битным списком из 0 и 1")

        for j in range(self.size):
            word = self.read_word(j)
            vj = word[:3]

            if vj == v_key:
                aj = word[3:7]  # 4 бита A
                bj = word[7:11]  # 4 бита B

                # Преобразуем A и B из бит в числа
                aj_val = sum(bit << (3 - i) for i, bit in enumerate(aj))
                bj_val = sum(bit << (3 - i) for i, bit in enumerate(bj))

                sum_val = aj_val + bj_val

                # Преобразуем сумму в 5 бит (S)
                sum_bits = [(sum_val >> (4 - i)) & 1 for i in range(5)]

                # Формируем новое слово: V + A + B + S
                new_word = vj + aj + bj + sum_bits

                # Записываем обратно в матрицу
                self.write_word(j, new_word)



    def display(self):
        """Вывести матрицу."""
        for row in self.matrix:
            print(' '.join(map(str, row)))
        print()
