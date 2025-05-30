class HashTable:
    _DELETED = "<удалено>"

    def __init__(self, size=11):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def _find_slot(self, key, for_insert=False):
        index = self._hash(key)
        i = 0

        while i < self.size:
            probe_index = (index + i * i) % self.size
            if self.table[probe_index] is None:
                if for_insert:
                    return probe_index
                else:
                    return None
            elif self.table[probe_index] == HashTable._DELETED:
                if for_insert:
                    return probe_index
            elif self.table[probe_index][0] == key:
                return probe_index
            i += 1
        return None

    def insert(self, key, value):
        if self.search(key) is not None:
            raise KeyError(f"Ключ '{key}' уже существует")

        slot = self._find_slot(key, for_insert=True)
        if slot is None:
            raise OverflowError("Таблица переполнена")

        self.table[slot] = (key, value)

    def insert_with_collision_demo(self, key, value):
        if self.search(key) is not None:
            raise KeyError(f"Ключ '{key}' уже существует")

        index = self._hash(key)
        i = 0
        print(f"Попытка вставить ключ '{key}' с хешем {index}")
        while i < self.size:
            probe_index = (index + i * i) % self.size
            if self.table[probe_index] is None or self.table[probe_index] == HashTable._DELETED:
                self.table[probe_index] = (key, value)
                if i == 0:
                    print(f"Вставлено без коллизий в ячейку {probe_index}.")
                else:
                    print(f"Коллизия! Вставлено в ячейку {probe_index} после {i} попыток.")
                return
            else:
                print(f"Коллизия на ячейке {probe_index}, пробуем следующую i={i+1}")
            i += 1

        raise OverflowError("Таблица переполнена")

    def search(self, key):
        slot = self._find_slot(key)
        if slot is not None:
            return self.table[slot][1]
        return None

    def update(self, key, value):
        slot = self._find_slot(key)
        if slot is None:
            raise KeyError(f"Ключ '{key}' не найден")
        self.table[slot] = (key, value)

    def delete(self, key):
        slot = self._find_slot(key)
        if slot is None:
            raise KeyError(f"Ключ '{key}' не найден")
        self.table[slot] = HashTable._DELETED

    def display(self):
        print("\nТекущая хеш-таблица:")
        for i, item in enumerate(self.table):
            if item is None:
                print(f"[{i}] Пусто")
            elif item == HashTable._DELETED:
                print(f"[{i}] Удалено")
            else:
                print(f"[{i}] {item[0]}: {item[1]}")
        print()
