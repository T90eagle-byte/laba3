# WORK_CONTEXT

## Final Checkpoint (2026-05-31)

### Актуальный путь проекта
- `C:\Users\User\DATA\Моя учеба\Web-razrab\pharmacy`

### Архитектура и стек
- Backend стабилизирован.
- Используются: Flask, Flask-Login, Flask-WTF, SQLite.
- База данных: `data/pharmacy.sqlite`.
- Шаблоны: `app/templates`.
- Static: `app/static`.

### Безопасность и данные
- Пароли хранятся через Werkzeug-хэши (`generate_password_hash` / `check_password_hash`).
- Legacy `sha256` поддержан и автоапгрейдится при успешном входе.
- SQL использует DB-API placeholders (`?`).
- Реализован owner-check заказов (чужие заказы недоступны обычному пользователю).
- Все destructive actions выполняются через POST + CSRF (`hidden_tag()`).
- Logout работает только через POST + CSRF.

### Корзина и заказы
- Реализована session-корзина (без отдельной Cart-модели и без миграций).
- Маршруты корзины:
  - `GET /cart`
  - `POST /cart/add/<int:product_id>`
  - `POST /cart/remove/<int:product_id>`
  - `POST /cart/checkout`
- Старый flow заказа через `/orders/form/0` сохранён.

### Дизайн
- Дизайн перенесён на страницы:
  - `login.tpl`
  - `register.tpl`
  - `products.tpl`
  - `cart.tpl`
  - `orders.tpl`
  - `profile.tpl`
- Для админки выполнен `admin light styling`:
  - `admin.tpl`
  - `admin_user_form.tpl`
  - `product_form.tpl`
  - `import.tpl`

### Импорт ЛР1 и legacy-файлы
- Для демонстрационного импорта добавлен файл `data/catalog.pkl`.
- Корневые legacy-файлы ЛР1 (`catalog.py`, `medicine.py`, `product.py` и др., включая корневой `catalog.pkl`) добавлены в `.gitignore` и не входят в рабочий Flask-контур.

### Финальный аудит
- Финальный аудит пройден:
  - `py_compile` ключевых Python-файлов;
  - smoke/integration-проверки через Flask test client;
  - проверки доступа (гость/пользователь/админ);
  - проверки POST + CSRF для state-changing действий;
  - проверки отсутствия Jinja errors на основных маршрутах.

### Важные запреты (сохраняются)
- Не ломать Flask / Flask-Login / Flask-WTF.
- Не ломать `module_url` / `url_for`.
- Не ломать WTForms, `hidden_tag()`, `action/method/name/value`.
- Не менять SQLite-схему и backend-логику без отдельного согласования.

## Проект
Flask-приложение аптеки/картотеки с поэтапным переносом дизайна из Pixso D2C в существующую Flask/Jinja архитектуру без переписывания backend с нуля.

## Текущее техническое состояние
- База данных: SQLite, файл `data/pharmacy.sqlite`.
- Шаблоны: `app/templates`.
- Static: `app/static`.
- В проекте есть выгрузка дизайна: `design_export` (Pixso D2C).
- Подключен общий стиль `app/static/css/app.css`.
- Сохранены Flask, Flask-Login, Flask-WTF.
- Сохранена админка.
- Сохранен импорт данных из ЛР1 (`/import`).
- SQL-запросы выполняются через DB-API placeholders (`?`), без небезопасной конкатенации пользовательских данных.

## D2C и UI-фундамент
- D2C assets перенесены в `app/static` (fonts/images).
- Базовый layout и header/nav уже интегрированы в `base.tpl`.
- Подключены общие стили и дизайн-токены через `app.css`.

## Корзина и заказы
- Реализована session-корзина (без отдельной Cart-модели и без миграций).
- Добавлены cart routes:
  - `GET /cart`
  - `POST /cart/add/<int:product_id>`
  - `POST /cart/remove/<int:product_id>`
  - `POST /cart/checkout`
- Заказ из корзины создается через существующую order-логику и сохраняется в SQLite.
- Старый flow `/orders/form/0` сохранен.

## Безопасность и доступ
- Закрыты обязательные backend security-пункты:
  - state-changing действия переведены на POST;
  - в опасные POST-действия добавлен CSRF (Flask-WTF `hidden_tag`);
  - добавлен контроль доступа к чужим заказам (обычный пользователь не может открыть/изменить/удалить чужой заказ).

## Пароли
- Хэширование переведено на Werkzeug:
  - `generate_password_hash` для сохранения новых паролей;
  - `check_password_hash` для проверки.
- Оставлена обратная совместимость со старыми `sha256`:
  - при успешном входе по legacy-хэшу выполняется автоматический апгрейд до Werkzeug-формата;
  - пользователи не сбрасываются, БД не пересоздается.

## Следующий большой этап
Полный pixel-perfect перенос дизайна (D2C/PDF) в существующие шаблоны:
1. login/register
2. catalog
3. cart
4. orders
5. profile
6. admin (light styling, без ломки CRUD и backend-логики)

## Нельзя ломать
- Flask / Flask-Login / Flask-WTF.
- Существующие routes и backend flow без необходимости.
- Jinja-логику, `module_url` / `url_for`.
- WTForms поля и form action/method/name/value.
- Админские сценарии и импорт ЛР1.
- Структуру БД и миграции (без отдельного согласования).
