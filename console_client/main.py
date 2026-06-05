import getpass
import os

try:
    from .api_client import ApiError, DEFAULT_BASE_URL, ENV_BASE_URL, PharmacyApiClient
except ImportError:
    from api_client import ApiError, DEFAULT_BASE_URL, ENV_BASE_URL, PharmacyApiClient


CATEGORIES = ["Все", "Лекарства", "Витамины и БАД", "Красота", "Гигиена"]
PRODUCT_CATEGORIES = CATEGORIES[1:]


def print_title(text):
    print("\n" + text)
    print("-" * len(text))


def input_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Введите значение.")


def input_int(prompt):
    while True:
        raw = input_nonempty(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Введите число.")
            continue
        if value > 0:
            return value
        print("Введите положительное число.")


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


def input_float(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            value = float(raw.replace(",", "."))
        except ValueError:
            print("Введите число.")
            continue
        if value >= 0:
            return value
        print("Цена не может быть отрицательной.")


def input_yes_no(prompt, default=None):
    suffix = ""
    if default is True:
        suffix = " [Y/n]"
    elif default is False:
        suffix = " [y/N]"
    while True:
        raw = input(prompt + suffix + ": ").strip().lower()
        if not raw and default is not None:
            return default
        if raw in {"y", "yes", "д", "да", "1", "true"}:
            return True
        if raw in {"n", "no", "н", "нет", "0", "false"}:
            return False
        print("Введите y/n или да/нет.")


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
            f"{(item.get('name') or '')[:22]:<22} "
            f"{(item.get('dosage') or '')[:14]:<14} "
            f"{(item.get('category') or '')[:16]:<16} "
            f"{item.get('price', 0):>8.0f}  {stock}"
        )


def print_users(users):
    if not users:
        print("Пользователи не найдены.")
        return
    print(f"{'ID':>4}  {'Логин':<18} {'ФИО':<34} {'Роль':<14} Адрес")
    print("-" * 90)
    for user in users:
        full_name = " ".join(
            part for part in [user.get("surname"), user.get("name"), user.get("patronymic")] if part
        )
        role = "админ" if user.get("is_admin") else "пользователь"
        print(
            f"{user.get('id', ''):>4}  "
            f"{(user.get('login') or '')[:18]:<18} "
            f"{full_name[:34]:<34} "
            f"{role:<14} {user.get('address') or ''}"
        )


def print_order(order):
    print(f"Заказ #{order.get('id')} | пользователь #{order.get('user_id')} | {order.get('payment')}")
    print(f"Дата: {order.get('created')} | сумма: {order.get('total', 0):.0f}")
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


def choose_category(include_all=True, default=None):
    categories = CATEGORIES if include_all else PRODUCT_CATEGORIES
    print("Категории:")
    for index, category in enumerate(categories, start=1):
        marker = ""
        if default and category == default:
            marker = " (текущая)"
        print(f"{index}. {category}{marker}")
    prompt = "Выберите категорию"
    if default:
        prompt += f" [{default}]"
    elif include_all:
        prompt += " [1]"
    prompt += ": "
    raw = input(prompt).strip()
    if not raw:
        return default or ("Все" if include_all else PRODUCT_CATEGORIES[0])
    try:
        index = int(raw)
        return categories[index - 1]
    except (ValueError, IndexError):
        fallback = default or ("Все" if include_all else PRODUCT_CATEGORIES[0])
        print(f"Неизвестная категория, выбрано: {fallback}.")
        return fallback


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
    order_id = safe_api_call(lambda: input_int("ID заказа: "))
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
    order_id = safe_api_call(lambda: input_int("ID заказа: "))
    if order_id is None:
        return
    if not input_yes_no(f"Удалить заказ #{order_id}?", default=False):
        print("Удаление отменено.")
        return
    result = safe_api_call(lambda: client.delete_order(order_id))
    if result:
        print(f"Заказ #{result.get('id')} удалён.")


def admin_show_users(client):
    users = safe_api_call(client.get_users)
    if users is not None:
        print_users(users)


def prompt_user_payload(existing=None, *, create=False):
    existing = existing or {}
    payload = {}
    login_prompt = "Логин"
    if existing.get("login"):
        login_prompt += f" [{existing.get('login')}]"
    login = input((login_prompt + ": ")).strip()
    if login or create:
        payload["login"] = login or existing.get("login") or ""

    for field, label in [
        ("surname", "Фамилия"),
        ("name", "Имя"),
        ("patronymic", "Отчество"),
        ("address", "Адрес"),
    ]:
        prompt = label
        if existing.get(field):
            prompt += f" [{existing.get(field)}]"
        value = input(prompt + ": ").strip()
        payload[field] = value if value or create else existing.get(field, "")

    if create:
        while True:
            password = getpass.getpass("Пароль: ")
            if password:
                payload["password"] = password
                break
            print("Пароль обязателен для нового пользователя.")
    else:
        password = getpass.getpass("Новый пароль (пусто — не менять): ")
        if password:
            payload["password"] = password

    payload["is_admin"] = input_yes_no("Администратор", default=bool(existing.get("is_admin")))
    return payload


def admin_create_user(client):
    payload = safe_api_call(lambda: prompt_user_payload(create=True))
    if payload is None:
        return
    user = safe_api_call(lambda: client.create_user(payload))
    if user:
        print("Пользователь создан:")
        print_users([user])


def admin_update_user(client):
    user_id = safe_api_call(lambda: input_int("ID пользователя: "))
    if user_id is None:
        return
    existing = safe_api_call(lambda: client.get_user(user_id))
    if not existing:
        return
    print("Текущие данные:")
    print_users([existing])
    payload = safe_api_call(lambda: prompt_user_payload(existing))
    if payload is None:
        return
    user = safe_api_call(lambda: client.update_user(user_id, payload))
    if user:
        print("Пользователь обновлён:")
        print_users([user])


def admin_delete_user(client):
    user_id = safe_api_call(lambda: input_int("ID пользователя: "))
    if user_id is None:
        return
    if not input_yes_no(f"Удалить пользователя #{user_id}?", default=False):
        print("Удаление отменено.")
        return
    result = safe_api_call(lambda: client.delete_user(user_id))
    if result:
        print(f"Пользователь #{result.get('id')} удалён.")


def prompt_product_payload(existing=None, *, create=False):
    existing = existing or {}
    payload = {}

    prompt = "Название"
    if existing.get("name"):
        prompt += f" [{existing.get('name')}]"
    name = input(prompt + ": ").strip()
    payload["name"] = name if name or create else existing.get("name", "")

    prompt = "Дозировка"
    if existing.get("dosage"):
        prompt += f" [{existing.get('dosage')}]"
    dosage = input(prompt + ": ").strip()
    payload["dosage"] = dosage if dosage or create else existing.get("dosage", "")

    payload["category"] = choose_category(
        include_all=False,
        default=existing.get("category") or PRODUCT_CATEGORIES[0],
    )
    payload["price"] = input_float(
        f"Цена [{existing.get('price')}]" if existing.get("price") is not None and not create else "Цена",
        default=existing.get("price") if not create else None,
    )
    payload["in_stock"] = input_yes_no("Есть в наличии", default=bool(existing.get("in_stock", True)))
    return payload


def admin_create_product(client):
    payload = safe_api_call(lambda: prompt_product_payload(create=True))
    if payload is None:
        return
    product = safe_api_call(lambda: client.create_product(payload))
    if product:
        print("Товар создан:")
        print_products([product])


def admin_update_product(client):
    product_id = safe_api_call(lambda: input_int("ID товара: "))
    if product_id is None:
        return
    existing = safe_api_call(lambda: client.product(product_id))
    if not existing:
        return
    print("Текущие данные:")
    print_products([existing])
    payload = safe_api_call(lambda: prompt_product_payload(existing))
    if payload is None:
        return
    product = safe_api_call(lambda: client.update_product(product_id, payload))
    if product:
        print("Товар обновлён:")
        print_products([product])


def admin_delete_product(client):
    product_id = safe_api_call(lambda: input_int("ID товара: "))
    if product_id is None:
        return
    if not input_yes_no(f"Удалить товар #{product_id}?", default=False):
        print("Удаление отменено.")
        return
    result = safe_api_call(lambda: client.delete_product(product_id))
    if result:
        print(f"Товар #{result.get('id')} удалён.")


def build_actions(is_admin):
    actions = {
        "1": ("Показать каталог товаров", show_catalog),
        "2": ("Поиск товаров", search_products),
        "3": ("Фильтр по категории", filter_products),
        "4": ("Показать мои заказы", show_orders),
        "5": ("Создать заказ", create_order),
        "6": ("Изменить заказ", update_order),
        "7": ("Удалить заказ", delete_order),
    }
    if is_admin:
        actions.update({
            "8": ("Админ: показать пользователей", admin_show_users),
            "9": ("Админ: добавить пользователя", admin_create_user),
            "10": ("Админ: изменить пользователя", admin_update_user),
            "11": ("Админ: удалить пользователя", admin_delete_user),
            "12": ("Админ: показать товары", show_catalog),
            "13": ("Админ: добавить товар", admin_create_product),
            "14": ("Админ: изменить товар", admin_update_product),
            "15": ("Админ: удалить товар", admin_delete_product),
        })
    actions["0"] = ("Выйти", None)
    return actions


def main():
    base_url = os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL
    client = PharmacyApiClient(base_url)
    print(f"API: {client.base_url}")
    print(f"Можно изменить адрес через переменную {ENV_BASE_URL}.")

    user = login_loop(client)
    is_admin = bool(user.get("is_admin"))
    role = "администратор" if is_admin else "пользователь"
    print(f"Вход выполнен: {user.get('login')} ({role})")
    actions = build_actions(is_admin)

    while True:
        print_title("Главное меню")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
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
