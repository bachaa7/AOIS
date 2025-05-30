from hash_table import HashTable
from io import StringIO
from unittest.mock import patch  # Правильный импорт
import unittest

class TestHashTable(unittest.TestCase):
    def setUp(self):
        """Инициализация хеш-таблицы перед каждым тестом."""
        self.ht = HashTable(size=11)

    def test_init(self):
        """Тест инициализации хеш-таблицы."""
        self.assertEqual(self.ht.size, 11)
        self.assertEqual(len(self.ht.table), 11)
        self.assertTrue(all(x is None for x in self.ht.table))

    def test_hash(self):
        """Тест функции хеширования."""
        self.assertEqual(self.ht._hash("key1"), sum(ord(c) for c in "key1") % 11)
        self.assertEqual(self.ht._hash("key2"), sum(ord(c) for c in "key2") % 11)
        self.assertTrue(0 <= self.ht._hash("anykey") < self.ht.size)

    def test_find_slot_for_insert(self):
        """Тест поиска слота для вставки."""
        self.ht.table[0] = ("key1", "value1")
        slot = self.ht._find_slot("key2", for_insert=True)
        self.assertIsNotNone(slot)
        self.assertNotEqual(slot, 0)

    def test_find_slot_for_search(self):
        """Тест поиска слота для поиска."""
        hash_index = self.ht._hash("key1")  # Вычисляем хеш для "key1"
        self.ht.table[hash_index] = ("key1", "value1")
        slot = self.ht._find_slot("key1")
        self.assertEqual(slot, hash_index)
        slot = self.ht._find_slot("key2")
        self.assertIsNone(slot)

    def test_insert(self):
        """Тест вставки элементов."""
        self.ht.insert("key1", "value1")
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertIsNone(self.ht.search("key2"))

    def test_insert_duplicate_key(self):
        """Тест вставки с существующим ключом."""
        self.ht.insert("key1", "value1")
        with self.assertRaises(KeyError):
            self.ht.insert("key1", "value2")

    def test_insert_full_table(self):
        """Тест вставки в переполненную таблицу."""
        for i in range(self.ht.size):
            self.ht.insert(f"key{i}", f"value{i}")
        with self.assertRaises(OverflowError):
            self.ht.insert("extra_key", "extra_value")

    def test_insert_with_collision(self):
        """Тест вставки с коллизией."""
        self.ht.insert("a", "value1")  # Хеш = 9
        self.ht.insert("k", "value2")  # Хеш = 9
        self.assertEqual(self.ht.search("a"), "value1")
        self.assertEqual(self.ht.search("k"), "value2")

    def test_search(self):
        """Тест поиска элементов."""
        self.ht.insert("key1", "value1")
        self.assertEqual(self.ht.search("key1"), "value1")
        self.assertIsNone(self.ht.search("key2"))

    def test_update(self):
        """Тест обновления значения."""
        self.ht.insert("key1", "value1")
        self.ht.update("key1", "new_value")
        self.assertEqual(self.ht.search("key1"), "new_value")

    def test_update_nonexistent_key(self):
        """Тест обновления несуществующего ключа."""
        with self.assertRaises(KeyError):
            self.ht.update("key1", "value1")

    def test_delete(self):
        """Тест удаления элемента."""
        self.ht.insert("key1", "value1")
        self.ht.delete("key1")
        self.assertEqual(self.ht.table[self.ht._find_slot("key1", for_insert=True)], HashTable._DELETED)
        self.assertIsNone(self.ht.search("key1"))

    def test_delete_nonexistent_key(self):
        """Тест удаления несуществующего ключа."""
        with self.assertRaises(KeyError):
            self.ht.delete("key1")

    def test_insert_after_delete(self):
        """Тест вставки в слот после удаления."""
        self.ht.insert("key1", "value1")
        slot = self.ht._find_slot("key1")
        self.ht.delete("key1")
        self.assertEqual(self.ht.table[slot], HashTable._DELETED)
        self.ht.insert("key2", "value2")
        self.assertEqual(self.ht.search("key2"), "value2")
        new_slot = self.ht._find_slot("key2")
        self.assertEqual(self.ht.table[new_slot], ("key2", "value2"))


    def test_display(self):
        """Тест отображения таблицы."""
        self.ht.insert("key1", "value1")
        self.ht.delete("key1")
        self.ht.display()  # Проверяем, что метод не вызывает ошибок

    def test_insert_with_collision_demo(self):
        """Тест вставки с коллизией в insert_with_collision_demo."""
        self.ht.insert("a", "value1")  # Хеш = 9
        key, value = "k", "value2"  # Хеш = 9
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.ht.insert_with_collision_demo(key, value)
            output = fake_out.getvalue()
        self.assertEqual(self.ht.search(key), value)
        slot = self.ht._find_slot(key)
        self.assertEqual(self.ht.table[slot], (key, value))

if __name__ == "__main__":
    unittest.main()