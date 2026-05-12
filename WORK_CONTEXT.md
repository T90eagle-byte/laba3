# WORK_CONTEXT

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
