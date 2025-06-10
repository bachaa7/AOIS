import sys
import os
import re
import itertools
from typing import List, Tuple, Dict, Set, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from AOIS_2lab.Truth_table_processor import TruthTableProcessor

class LogicMinimizer:
    """Класс для минимизации логических выражений различными методами"""

    def __init__(self, truth_table, variables):
        self.truth_table = truth_table
        self.variables = variables
        self.num_vars = len(variables)
        self.minterms = self._get_minterms()
        self.maxterms = self._get_minterms()

    def _get_minterms(self) -> List[int]:
        """Получение номеров строк, где результат 1 (для СДНФ)"""
        return [i for i, (_, _, result) in enumerate(self.truth_table) if result]

    def _get_maxterms(self) -> List[int]:
        """Получение номеров строк, где результат 0 (для СКНФ)"""
        return [i for i, (_, _, result) in enumerate(self.truth_table) if not result]

    def _term_to_binary(self, term: int) -> str:
        """Преобразование номера строки в бинарное представление"""
        return format(term, f'0{self.num_vars}b')

    def _binary_to_term(self, binary: str, is_minterm: bool) -> str:
        """Бинарное представление в термы СДНФ или СКНФ"""
        term = []
        for i, bit in enumerate(binary):
            if bit == '-':
                continue
            var = self.variables[i]
            if is_minterm:
                term.append(var if bit == '1' else f"!{var}")
            else:
                term.append(f"!{var}" if bit == '1' else var)
        return f"({' & '.join(term)})" if is_minterm and term else f"({' | '.join(term)})" if term else "True" if is_minterm else "False"

    def _can_glue(self, term1: str, term2: str) -> Tuple[bool, str]:
        """Проверка возможности склеивания двух термов"""
        if term1 == term2:
            return False, ''
        differences = 0
        glued = []
        for b1, b2 in zip(term1, term2):
            if b1 != b2:
                differences += 1
                glued.append('-')
            else:
                glued.append(b1)
            if differences > 1:
                return False, ''
        return True, ''.join(glued)

    def _is_term_covered(self, implicant: str, term: str) -> bool:
        """Проверка, покрывает ли импликанта заданный терм"""
        if len(implicant) != len(term):
            return False
        for i, j in zip(implicant, term):
            if i != '-' and i != j:
                return False
        return True

    def _build_coverage_table(self, implicants: List[Tuple[str, str]], terms: List[Tuple[str, str]]) -> str:
        """Построение таблицы соответствий с выравниванием столбцов"""
        if not implicants or not terms:
            return "====================== Таблица ======================\nПустая таблица\n"

        max_term_len = max(len(expr) for _, expr in terms)
        max_implicant_len = max(len(expr) for _, expr in implicants)
        cell_width = max(max_term_len, max_implicant_len, 5) + 4

        header = f"{'':<{max_implicant_len + 2}} | " + " | ".join(expr.center(cell_width) for _, expr in terms)
        separator = "-" * (max_implicant_len + 2) + "+-" + "-+-".join("-" * cell_width for _ in terms)

        rows = []
        for bin_implicant, implicant_expr in implicants:
            row = f"{implicant_expr:<{max_implicant_len + 2}} | "
            row += " | ".join(
                "X".center(cell_width) if self._is_term_covered(bin_implicant, bin_term) else " ".center(cell_width)
                for bin_term, _ in terms)
            rows.append(row)

        return ("====================== Таблица ======================\n" +
                header + "\n" +
                separator + "\n" +
                "\n".join(rows) + "\n")

    def _glue_terms(self, terms: List[Tuple[str, str]], is_minterm: bool) -> Tuple[
        List[Tuple[str, str]], List[Tuple[str, str, str]], Set[str]]:
        """Склеивание термов с возвратом истории и использованных терминов"""
        glued_terms = []
        glue_history = []
        used = set()
        seen_results = set()

        for i, (bin1, expr1) in enumerate(terms):
            for j, (bin2, expr2) in enumerate(terms[i + 1:], start=i + 1):
                if bin1 == bin2:
                    continue
                can_glue, result_bin = self._can_glue(bin1, bin2)
                if can_glue and result_bin not in seen_results:
                    result_expr = self._binary_to_term(result_bin, is_minterm)
                    glued_terms.append((result_bin, result_expr))
                    seen_results.add(result_bin)
                    used.add(bin1)
                    used.add(bin2)
                    glue_history.append((expr1, expr2, result_expr))

        return glued_terms, glue_history, used

    def _minimize_quin(self, is_minterm: bool, build_table: bool = False) -> Tuple[str, List[str]]:
        """Минимизация методом Квайна с выводом таблиц"""
        initial_terms = [(self._term_to_binary(t), self._binary_to_term(self._term_to_binary(t), is_minterm))
                         for t in (self.minterms if is_minterm else self.maxterms)]
        if not initial_terms:
            return "True" if is_minterm else "False", ["Склеиваний нет"]

        groups = {i: [] for i in range(self.num_vars + 1)}
        for bin_term, expr in initial_terms:
            count = bin_term.count('1')
            groups[count].append((bin_term, expr))

        prime_implicants = []
        all_glue_history = []
        used_terms = set()
        step = 1
        max_steps = 1000

        while groups and step <= max_steps:
            new_groups = {}
            stage_history = []
            stage_used = set()

            current_terms = []
            for count in sorted(groups.keys()):
                current_terms.extend(groups[count])

            glued_terms, glue_history, used = self._glue_terms(current_terms, is_minterm)
            stage_history.extend(glue_history)
            stage_used.update(used)

            for count, term_list in groups.items():
                for bin_term, expr in term_list:
                    if bin_term not in stage_used and (bin_term, expr) not in prime_implicants:
                        prime_implicants.append((bin_term, expr))

            if stage_history or build_table:
                step_str = f"=== Шаг {step} склеивания ===\n"
                if stage_history:
                    for t1, t2, result in stage_history:
                        step_str += f"{t1} & {t2} => {result}\n"
                else:
                    step_str += "Больше нечего склеивать, минимизация завершена.\n"

                if build_table:
                    current_implicants = [(bin_term, expr) for bin_term, expr in prime_implicants if
                                          bin_term not in stage_used] + glued_terms
                    step_str += self._build_coverage_table(current_implicants, initial_terms)

                all_glue_history.append(step_str)
                step += 1

            used_terms.update(stage_used)
            for bin_term, expr in glued_terms:
                ones = bin_term.count('1')
                new_groups.setdefault(ones, []).append((bin_term, expr))
            groups = new_groups

        if step > max_steps:
            print(f"[DEBUG] Достигнуто максимальное количество шагов ({max_steps})")

        for bin_term, expr in initial_terms:
            if bin_term not in used_terms and (bin_term, expr) not in prime_implicants:
                prime_implicants.append((bin_term, expr))

        result_terms = [expr for _, expr in prime_implicants]
        result = " | ".join(result_terms) if is_minterm and result_terms else " & ".join(
            result_terms) if result_terms else "True" if is_minterm else "False"

        return result, all_glue_history

    def _get_gray_code(self, n: int) -> List[str]:
        """Генерация кода Грэя для n бит"""
        if n == 0:
            return ['0']
        gray = ['0', '1']
        for _ in range(1, n):
            gray = ['0' + x for x in gray] + ['1' + x for x in reversed(gray)]
        return gray

    def _build_karnaugh_map(self, is_minterm: bool) -> List[List[int]]:
        """Построение карты Карно"""
        size = 2 ** self.num_vars
        map_size = (2 ** (self.num_vars // 2), 2 ** (self.num_vars - self.num_vars // 2))
        k_map = [[0] * map_size[1] for _ in range(map_size[0])]

        for i in range(size):
            binary = self._term_to_binary(i)
            row = int(binary[:self.num_vars // 2], 2) if self.num_vars > 1 else 0
            col = int(binary[self.num_vars // 2:], 2)
            k_map[row][col] = 1 if (i in self.minterms if is_minterm else i in self.maxterms) else 0

        return k_map

    def _display_karnaugh_map(self, k_map: List[List[int]]) -> str:
        """Форматирование карты Карно в стиле примера"""
        # Определяем количество бит для строк и столбцов
        row_bits = self.num_vars // 2 if self.num_vars > 1 else 1
        col_bits = self.num_vars - row_bits if self.num_vars > 1 else 1

        # Генерируем код Грэя для строк и столбцов
        row_gray = self._get_gray_code(row_bits)
        col_gray = self._get_gray_code(col_bits)

        # Вычисляем ширину ячейки
        cell_width = 4  # Фиксированная ширина для ячеек (как в примере: " 0  ")
        label_width = max(len(label) for label in row_gray + col_gray) + 1

        # Формируем заголовок
        header = ' ' * label_width + ' | ' + ' | '.join(f"{cd:^{cell_width}}" for cd in col_gray)
        separator = '-' * (label_width + 1) + '-+-' * (len(col_gray) - 1) + '-' * cell_width

        # Формируем строки
        output = [header, separator]
        for row_idx, ab in enumerate(row_gray):
            row = f"{ab:<{label_width}}| " + ' | '.join(f"{cell:^{cell_width}}" for cell in k_map[row_idx])
            output.append(row)

        return '\n'.join(output)

    def _terms_sknf(self) -> List[List[int]]:
        """Получение термов СКНФ из макстермов"""
        result = []
        for maxterm in self.maxterms:
            binary = self._term_to_binary(maxterm)
            term = [1 if bit == '0' else 0 for bit in binary]  # Инвертируем для СКНФ
            result.append(term)
        return result

    def _term_to_expression_sknf(self, term: List[int]) -> str:
        """Преобразование терма СКНФ в выражение"""
        expression = []
        for value, var in zip(term, self.variables):
            if value == 1:
                expression.append(var)
            elif value == 0:
                expression.append(f"!{var}")
            elif value == "X":
                continue
        return f"({' | '.join(expression)})" if expression else "False"

    def _compare_terms_sknf(self, terms: List[List[int]], verbose: bool = False) -> List[List[int]]:
        """Сравнение и склеивание термов СКНФ"""
        n = len(terms[0])
        step_result = []
        used = [False] * len(terms)

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                diff_positions = []
                for k in range(n):
                    if terms[i][k] != terms[j][k]:
                        diff_positions.append(k)
                if len(diff_positions) == 1:
                    new_term = terms[i].copy()
                    new_term[diff_positions[0]] = "X"
                    if verbose:
                        term_i_expr = self._term_to_expression_sknf(terms[i])
                        term_j_expr = self._term_to_expression_sknf(terms[j])
                        new_term_expr = self._term_to_expression_sknf(new_term)
                        print(f"{term_i_expr} & {term_j_expr} => {new_term_expr}")
                    step_result.append(new_term)
                    used[i] = True
                    used[j] = True

        for idx in range(len(terms)):
            if not used[idx]:
                step_result.append(terms[idx])

        return step_result

    def _parse_implicant_k(self, term: str) -> Dict[str, int]:
        """Парсинг импликанты СКНФ"""
        term = term.strip('()')
        components = term.split(" | ")
        term_vars = {}
        for comp in components:
            if comp.startswith('!'):
                term_vars[comp[1:]] = 0
            else:
                term_vars[comp] = 1
        for var in self.variables:
            if var not in term_vars:
                term_vars[var] = "X"
        return term_vars

    def _generate_false_sets_k(self, term_vars: Dict[str, int]) -> List[Dict[str, int]]:
        """Генерация ложных наборов для СКНФ"""
        fixed_vars = {var: (1 - val) for var, val in term_vars.items() if val != "X"}
        free_vars = [var for var in self.variables if var not in fixed_vars]
        combinations = list(itertools.product([0, 1], repeat=len(free_vars)))
        false_sets = []
        for comb in combinations:
            var_values = fixed_vars.copy()
            var_values.update(dict(zip(free_vars, comb)))
            false_sets.append(var_values)
        return false_sets

    def _evaluate_expression_k(self, expression: str, values: Dict[str, int]) -> bool:
        """Оценка выражения СКНФ"""
        for var, val in values.items():
            expression = expression.replace(f"!{var}", str(int(not val)))
            expression = expression.replace(var, str(val))
        expression = expression.replace("&", " and ").replace("|", " or ")
        if not expression.strip():
            return False
        return eval(expression)

    def _remove_redundant_implicants_k(self, term_expressions: List[str]) -> List[str]:
        """Удаление избыточных импликант СКНФ"""
        result = term_expressions[:]
        for term in term_expressions:
            term_vars = self._parse_implicant_k(term)
            temp_result = [t for t in result if t != term]
            remaining_expression = " & ".join(temp_result) if temp_result else "True"
            false_sets = self._generate_false_sets_k(term_vars)
            is_redundant = True
            for var_values in false_sets:
                if self._evaluate_expression_k(remaining_expression, var_values):
                    is_redundant = False
                    break
            if is_redundant and term in result:
                result.remove(term)
        return result

    def _build_sknf_coverage_table(self, expression_terms: List[List[int]], minimized_terms: List[List[int]]) -> str:
        """Построение таблицы соответствий для СКНФ"""
        def term_to_str(term):
            return [f"!{self.variables[idx]}" if var == 0 else self.variables[idx] for idx, var in enumerate(term) if var != "X"]

        header_terms = [" | ".join(term_to_str(term)) for term in expression_terms]
        minimized_terms_str = [" | ".join(term_to_str(term)) for term in minimized_terms]

        table = [["" for _ in range(len(header_terms) + 1)] for _ in range(len(minimized_terms) + 1)]
        table[0][0] = ""
        for j, term in enumerate(header_terms, start=1):
            table[0][j] = f"({term})"

        for i, min_term in enumerate(minimized_terms_str, start=1):
            table[i][0] = f"({min_term})"
            for j, expr_term in enumerate(expression_terms, start=1):
                min_term_parts = term_to_str(minimized_terms[i - 1])
                expr_term_parts = term_to_str(expr_term)
                if all(item in expr_term_parts for item in min_term_parts):
                    table[i][j] = "X"

        col_widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
        output = [" | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))) for row in table]
        return "\n".join(["====================== Таблица ======================"] + output)

    def _minimize_sknf_quin(self, build_table: bool = False) -> Tuple[str, List[str]]:
        """Минимизация СКНФ расчётным методом (адаптировано из Minimizing.minimize_sknf)"""
        terms = self._terms_sknf()
        if not terms:
            return "False", ["Склеиваний нет"]

        steps = []
        step = 0
        initial_terms = terms.copy()
        final_result = "False"  # Значение по умолчанию

        while True:
            step_str = f"\n=== Шаг {step + 1} склеивания ===\n"
            next_terms = self._compare_terms_sknf(terms, verbose=True)

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            term_expressions_before = [self._term_to_expression_sknf(term) for term in terms]
            step_str += f"ТЕРМЫ ДО СКЛЕЙКИ: {' & '.join(term_expressions_before)}\n"

            term_expressions_after = [self._term_to_expression_sknf(term) for term in unique_terms]
            step_str += f"\nТЕРМЫ ПОСЛЕ СКЛЕЙКИ: {' & '.join(term_expressions_after)}\n"

            if build_table:
                step_str += self._build_sknf_coverage_table(initial_terms, unique_terms) + "\n"

            steps.append(step_str)

            if not unique_terms or unique_terms == terms:
                result = self._remove_redundant_implicants_k(term_expressions_after)
                final_result = " & ".join(result) if result else "False"
                steps.append("\nБольше нечего склеивать, минимизация завершена.\n")
                steps.append(f"ВЫВОД: {final_result}")
                break

            terms = unique_terms
            step += 1
            if step > 1000:
                steps.append(f"[DEBUG] Достигнуто максимальное количество шагов (1000)")
                result = self._remove_redundant_implicants_k(term_expressions_after)
                final_result = " & ".join(result) if result else "False"
                steps.append(f"ВЫВОД: {final_result}")
                break

        return final_result, steps

    def minimize_sdnf_quin(self) -> Tuple[str, List[str]]:
        """Минимизация СДНФ расчетным методом"""
        return self._minimize_quin(is_minterm=True, build_table=False)

    def minimize_sknf_quin(self) -> Tuple[str, List[str]]:
        """Минимизация СКНФ расчетным методом"""
        return self._minimize_sknf_quin(build_table=False)

    def minimize_sdnf_quin_table(self) -> Tuple[str, List[str], str]:
        """Минимизация СДНФ расчетно-табличным методом"""
        result, glue_steps = self._minimize_quin(is_minterm=True, build_table=True)
        k_map = self._build_karnaugh_map(is_minterm=True)
        k_map_str = self._display_karnaugh_map(k_map)
        return result, glue_steps, k_map_str

    def minimize_sknf_quin_table(self) -> Tuple[str, List[str], str]:
        """Минимизация СКНФ расчетно-табличным методом"""
        result, glue_steps = self._minimize_sknf_quin(build_table=True)
        k_map = self._build_karnaugh_map(is_minterm=False)
        k_map_str = self._display_karnaugh_map(k_map)
        return result, glue_steps, k_map_str

    def minimize_sdnf_karnaugh(self) -> Tuple[str, str]:
        """Минимизация СДНФ с помощью карты Карно"""
        k_map = self._build_karnaugh_map(is_minterm=True)
        k_map_str = self._display_karnaugh_map(k_map)

        terms = []
        for term in self.minterms:
            binary = self._term_to_binary(term)
            terms.append(self._binary_to_term(binary, is_minterm=True))

        result = " | ".join(terms) if terms else "True"
        return result, k_map_str

    def minimize_sknf_karnaugh(self) -> Tuple[str, str]:
        """Минимизация СКНФ с помощью карты Карно"""
        k_map = self._build_karnaugh_map(is_minterm=False)
        k_map_str = self._display_karnaugh_map(k_map)

        terms = []
        for term in self.maxterms:
            binary = self._term_to_binary(term)
            terms.append(self._binary_to_term(binary, is_minterm=False))

        result = " & ".join(terms) if terms else "False"
        return result, k_map_str
