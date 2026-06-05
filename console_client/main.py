import getpass
import os
import sys

try:
    from .api_client import ApiError, DEFAULT_BASE_URL, ENV_BASE_URL, PharmacyApiClient
except ImportError:
    from api_client import ApiError, DEFAULT_BASE_URL, ENV_BASE_URL, PharmacyApiClient


CATEGORIES = ["Все", "Лекарства", "Витамины и БАД", "Красота", "Гигиена"]


def print_title(text):
    print("\n" + text)
    print("-" * len(text))


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Введите значение.")


def parse_ids(text):
    values = []
    for part in text.replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            value = int(part)
        except ValueError:
            raise ValueError("ID товаров должны быть числами через запятую.")
        if value <= 0:
            raise ValueError("ID товаров должны быть положительными числами.")
        values.append(value)
    if not values:
        raise ValueError("Нужно указать хотя бы один ID товара.")
    return values


def print_products(products):
    if not products:
        print("Товары не найдены.")
        return
    print(f"{'ID':>4}  {'Название':<22} {'Дозировка':<14} {'Категория':<16} {'Цена':>8}  Наличие")
    print("-" * 82)
    for item in products:
        stock = "есть" if item.get("in_stock") else "нет"
        print(
            f"{item.get('id', ''):>4}  "
            f"{item.get('name', ''):<22.22} "
            f"{item.get('dosage', ''):<14.14} "
            f"{item.get('category', ''):<16.16} "
            f"{item.get('price', 0):>8.0f}  "
            f"{stock}"
        )


def print_order(order):
    print(f"Заказ #{order.get('id')} | оплата: {order.get('payment')} | сумма: {order.get('total', 0):.0f}")
    items = order.get("items") or []
    if not items:
        print("  Позиции отсутствуют.")
        return
    for item in items:
        print(
            f"  - {item.get('name')} {item.get('dosage')} | "
            f"{item.get('category') or 'без категории'} | {item.get('price', 0):.0f}"
        )


def print_orders(orders):
    if not orders:
        print("Заказов пока нет.")
        return
    for order in orders:
        print_order(order)
        print()


def choose_category():
    print("Категории:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")
    raw = input("Выберите категорию [1]: ").strip()
    if not raw:
        return "Все"
    try:
        index = int(raw)
        return CATEGORIES[index - 1]
    except (ValueError, IndexError):
        print("Неизвестная категория, показываю все товары.")
        return "Все"


def safe_api_call(action):
    try:
        return action()
    except ApiError as exc:
        status = f" HTTP {exc.status_code}" if exc.status_code else ""
        print(f"Ошибка{status}: {exc.message}")
    except ValueError as exc:
        print(f"Ошибка ввода: {exc}")
    return None


def login_loop(client):
    print_title("Вход в аптечную систему")
    while True:
        login = input_nonempty("Логин: ")
        password = getpass.getpass("Пароль: ")
        data = safe_api_call(lambda: client.login(login, password))
        if data:
            me = safe_api_call(client.me)
            if me:
                return me.get("user") or {}
            return data.get("user") or {}
        again = input("Повторить вход? [Y/n]: ").strip().lower()
        if again in {"n", "no", "н", "нет"}:
            raise SystemExit(1)


def show_catalog(client):
    products = safe_api_call(lambda: client.products())
    if products is not None:
        print_products(products)


def search_products(client):
    query = input("Поиск по названию/дозировке: ").strip()
    products = safe_api_call(lambda: client.products(q=query))
    if products is not None:
        print_products(products)


def filter_products(client):
    category = choose_category()
    products = safe_api_call(lambda: client.products(category=category))
    if products is not None:
        print_products(products)


def show_orders(client):
    orders = safe_api_call(client.orders)
    if orders is not None:
        print_orders(orders)


def prompt_order_payload():
    raw_ids = input_nonempty("ID товаров через запятую: ")
    product_ids = parse_ids(raw_ids)
    payment = input("Способ оплаты [наличные]: ").strip() or "наличные"
    return product_ids, payment


def create_order(client):
    products = safe_api_call(lambda: client.products())
    if products is not None:
        print_products(products)
    payload = safe_api_call(prompt_order_payload)
    if payload is None:
        return
    product_ids, payment = payload
    order = safe_api_call(lambda: client.create_order(product_ids, payment))
    if order:
        print("Заказ создан:")
        print_order(order)


def update_order(client):
    order_id = safe_api_call(lambda: int(input_nonempty("ID заказа: ")))
    if order_id is None:
        return
    payload = safe_api_call(prompt_order_payload)
    if payload is None:
        return
    product_ids, payment = payload
    order = safe_api_call(lambda: client.update_order(order_id, product_ids, payment))
    if order:
        print("Заказ обновлён:")
        print_order(order)


def delete_order(client):
    order_id = safe_api_call(lambda: int(input_nonempty("ID заказа: ")))
    if order_id is None:
        return
    confirm = input(f"Удалить заказ #{order_id}? [y/N]: ").strip().lower()
    if confirm not in {"y", "yes", "д", "да"}:
        print("Удаление отменено.")
        return
    result = safe_api_call(lambda: client.delete_order(order_id))
    if result:
        print(f"Заказ #{result.get('id')} удалён.")


def main():
    base_url = os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL
    client = PharmacyApiClient(base_url)
    print(f"API: {client.base_url}")
    print(f"Можно изменить адрес через переменную {ENV_BASE_URL}.")

    user = login_loop(client)
    role = "администратор" if user.get("is_admin") else "пользователь"
    print(f"Вход выполнен: {user.get('login')} ({role})")

    actions = {
        "1": ("Показать каталог товаров", show_catalog),
        "2": ("Поиск товаров", search_products),
        "3": ("Фильтр по категории", filter_products),
        "4": ("Показать мои заказы", show_orders),
        "5": ("Создать заказ", create_order),
        "6": ("Изменить заказ", update_order),
        "7": ("Удалить заказ", delete_order),
        "8": ("Выйти", None),
    }

    while True:
        print_title("Главное меню")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        choice = input("Выберите действие: ").strip()
        if choice == "8":
            safe_api_call(client.logout)
            print("Выход выполнен.")
            return 0
        action = actions.get(choice)
        if not action:
            print("Неизвестный пункт меню.")
            continue
        action[1](client)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nРабота прервана пользователем.")
        raise SystemExit(130)
