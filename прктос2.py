import json

users = []
products = []


def load_data():
    global users, products
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    try:
        with open("products.json", "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []


def save_data():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)


def find_user(username):
    return next((user for user in users if user['username'] == username), None)


def sign_in():
    username = input("Логин: ")
    password = input("Пароль: ")
    user = find_user(username)

    if user and user['password'] == password:
        print(f"Добро пожаловать, {username}!")
        return user
    else:
        print("Неверный логин или пароль.")
        return None


def user_menu(user):
    while True:
        print("\n--- Меню пользователя ---")
        print("1. Просмотреть доступные товары")
        print("2. Купить товар")
        print("3. Просмотреть историю покупок")
        print("4. Фильтровать и сортировать товары")
        print("5. Обновить профиль")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            view_products()
        elif choice == "2":
            buy_product(user)
        elif choice == "3":
            view_purchase_history(user)
        elif choice == "4":
            sort_and_filter_products()
        elif choice == "5":
            update_profile(user)
        elif choice == "6":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def admin_menu():
    while True:
        print("\n--- Меню администратора ---")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Редактировать товар")
        print("4. Управление пользователями")
        print("5. Просмотреть статистику")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            remove_product()
        elif choice == "3":
            edit_product()
        elif choice == "4":
            manage_users()
        elif choice == "5":
            view_statistics()
        elif choice == "6":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def view_products():
    if not products:
        print("Нет доступных товаров.")
        return

    print("\nСписок доступных товаров:")
    print(f"{'Название':<50} {'Цена':<15} {'Рейтинг':<10}")
    for product in products:
        print(f"{product['name']:<50} {product['price']:>10,.2f} {product['rating']:>10,.1f}")

def buy_product(user):
    view_products()

    cart = {}
    total_price = 0.0

    while True:
        name = input("Введите название товара для покупки (или 'стоп' для завершения): ")

        if name.lower() == 'стоп':
            break

        product = next((p for p in products if p['name'].lower() == name.lower()), None)

        if product:
            quantity = int(input(f"Введите количество товара '{product['name']}': "))
            cart[product['name']] = {
                'price': product['price'],
                'quantity': quantity
            }
        else:
            print("Товар не найден.")

    if cart:
        print("\n--- Чек ---")
        print(f"{'Название':<36} {'Количество':<17} {'Цена':<13} {'Сумма':<6}")
        for item, details in cart.items():
            item_total = details['price'] * details['quantity']
            total_price += item_total
            print(f"{item:<40} {details['quantity']:<10} {details['price']:>5,.2f} {item_total:>16,.2f}")

        print(f"\nИтоговая сумма: {total_price:,.2f} ")

        user['history'].append(cart)
        save_data()
        print("Покупка завершена!")
    else:
        print("Вы ничего не купили.")


def load_data():
    global users, products
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            for user in users:
                if 'history' in user:
                    for index, purchase in enumerate(user['history']):
                        if not isinstance(purchase, dict) or 'items' not in purchase:
                            user['history'][index] = { 'items': {}, 'total_price': 0.0 }  # или просто продолжайте обработку
    except FileNotFoundError:
        users = []

    try:
        with open("products.json", "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []


def view_purchase_history(user):
    print("\nВаша история покупок:")
    history = user.get('history', [])

    if history:
        found_purchases = False

        for index, purchase in enumerate(history):
            if isinstance(purchase, dict) and 'items' in purchase and isinstance(purchase['items'], dict):
                total_price = purchase.get('total_price', 0.00)

                if total_price > 0:
                    found_purchases = True
                    print(f"Покупка #{index + 1}:")
                    for item, details in purchase['items'].items():
                        print(f"Товар: {item}, Количество: {details['quantity']}, Цена: {details['price']:.2f}")
                    print(f"Итоговая сумма: {total_price:.2f}")
                    print("-----------")

        if not found_purchases:
            print("У вас нет покупок с ненулевой суммой.")
    else:
        print("У вас нет истории покупок.")

def sort_and_filter_products():
    print("\nФильтрация товаров по критериям.")
    criteria = [
        {"key": "price", "label": "Цена"},
        {"key": "rating", "label": "Рейтинг"}
    ]

    print("Сортировка по:")
    for i, c in enumerate(criteria, start=1):
        print(f"{i}. {c['label']}")

    choice = input("Введите номер критерия для сортировки: ")

    try:
        if choice in ['1', '2']:
            key = criteria[int(choice) - 1]["key"]
            sorted_products = sorted(products, key=lambda x: x[key])
            print(f"\nСортировка товаров по {criteria[int(choice) - 1]['label']}:")
            print(f"{'Название':<50} {'Цена':<15} {'Рейтинг':<10}")
            for product in sorted_products:
                print(f"{product['name']:<50} {product['price']:>10,.2f} {product['rating']:>10,.1f}")
        else:
            raise ValueError("Неверный выбор.")
    except ValueError as e:
        print(e)


def update_profile(user):
    new_username = input("Введите новое имя пользователя (оставьте пустым, если не требуется): ")
    new_password = input("Введите новый пароль (оставьте пустым, если не требуется): ")

    try:
        if new_username:
            if find_user(new_username):
                raise ValueError("Пользователь с таким именем уже существует.")
            user['username'] = new_username

        if new_password:
            user['password'] = new_password

        save_data()
        print("Профиль успешно обновлён.")
    except ValueError as e:
        print(e)


def add_product():
    name = input("Введите название товара: ")
    price = float(input("Введите цену товара: "))
    rating = float(input("Введите рейтинг товара: "))

    if any(p['name'].lower() == name.lower() for p in products):
        print("Товар с таким названием уже существует.")
        return

    product = {'name': name, 'price': price, 'rating': rating}
    products.append(product)
    save_data()
    print("Товар добавлен.")


def remove_product():
    name = input("Введите название товара для удаления: ")
    product = next((p for p in products if p['name'].lower() == name.lower()), None)

    try:
        if product:
            products.remove(product)
            save_data()
            print("Товар удалён.")
        else:
            raise ValueError("Товар не найден.")
    except ValueError as e:
        print(e)


def edit_product():
    name = input("Введите название товара для редактирования: ")
    product = next((p for p in products if p['name'].lower() == name.lower()), None)

    if product:
        try:
            new_name = input("Введите новое название (оставьте пустым, если не требуется): ")
            new_price = input("Введите новую цену (оставьте пустым, если не требуется): ")
            new_rating = input("Введите новый рейтинг (оставьте пустым, если не требуется): ")

            if new_name:
                if any(p['name'].lower() == new_name.lower() for p in products if p != product):
                    raise ValueError("Товар с таким названием уже существует.")
                product['name'] = new_name

            if new_price:
                product['price'] = float(new_price)

            if new_rating:
                product['rating'] = float(new_rating)

            save_data()
            print("Товар обновлён.")
        except ValueError as e:
            print(e)
    else:
        print("Товар не найден.")


def manage_users():
    while True:
        print("\nУправление пользователями:")
        print("1. Добавить нового пользователя")
        print("2. Удалить пользователя")
        print("3. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def create_user():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    if find_user(username):
        print("Пользователь с таким именем уже существует.")
        return

    user = {
        'username': username,
        'password': password,
        'role': 'user',
        'history': []
    }
    users.append(user)
    save_data()
    print("Пользователь создан.")


def delete_user():
    username = input("Введите имя пользователя для удаления: ")
    user = find_user(username)
    if user:
        users.remove(user)
        save_data()
        print("Пользователь удалён.")
    else:
        print("Пользователь не найден.")


def view_statistics():
    total_products = len(products)
    total_users = len(users)
    print(f"Всего товаров: {total_products}")
    print(f"Всего пользователей: {total_users}")


def main():
    load_data()

    while True:
        print("\nДобро пожаловать в магазин одежды!")
        print("1. Войти как пользователь")
        print("2. Войти как администратор")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user = sign_in()
            if user:
                user_menu(user)
        elif choice == "2":
            username = input("Логин администратора: ")
            password = input("Пароль администратора: ")
            if username == 'admin' and password == 'admin':
                admin_menu()
            else:
                print("Неверный логин или пароль администратора.")
        elif choice == "3":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()