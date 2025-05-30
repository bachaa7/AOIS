from hash_table import HashTable

def load_data(filename):
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    data.append((key.strip(), value.strip()))
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден!")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return data

def menu():
    print("Меню:")
    print("1. Показать таблицу")
    print("2. Вставить запись (обычная вставка)")
    print("3. Вставить запись (с демонстрацией коллизий)")
    print("4. Найти запись")
    print("5. Обновить запись")
    print("6. Удалить запись")
    print("7. Загрузить записи из файла")
    print("0. Выход")

def main():
    ht = HashTable()

    while True:
        menu()
        choice = input("Выберите действие: ").strip()

        if choice == '1':
            ht.display()

        elif choice == '2':
            key = input("Введите ключ: ").strip()
            value = input("Введите значение: ").strip()
            try:
                ht.insert(key, value)
                print("Запись добавлена.")
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '3':
            key = input("Введите ключ: ").strip()
            value = input("Введите значение: ").strip()
            try:
                ht.insert_with_collision_demo(key, value)
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '4':
            key = input("Введите ключ для поиска: ").strip()
            result = ht.search(key)
            if result is None:
                print("Запись не найдена.")
            else:
                print(f"Значение: {result}")

        elif choice == '5':
            key = input("Введите ключ для обновления: ").strip()
            if ht.search(key) is None:
                print("Запись не найдена.")
            else:
                value = input("Введите новое значение: ").strip()
                ht.update(key, value)
                print("Запись обновлена.")

        elif choice == '6':
            key = input("Введите ключ для удаления: ").strip()
            try:
                ht.delete(key)
                print("Запись удалена.")
            except Exception as e:
                print("Ошибка:", e)

        elif choice == '7':
            filename = input("Введите имя файла: ").strip()
            records = load_data(filename)
            for k, v in records:
                try:
                    ht.insert(k, v)
                except Exception as e:
                    print(f"Ошибка при вставке {k}: {e}")
            print("Данные загружены.")

        elif choice == '0':
            print("Выход...")
            break

        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
