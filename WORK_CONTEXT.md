# WORK CONTEXT

## Цель проекта
Flask-приложение аптеки сохранить рабочим по backend-логике и поэтапно привести UI к Pixso D2C (`design_export`) без переписывания проекта с нуля.

## Что уже сделано по D2C / design_export
- Добавлена и проанализирована папка `design_export` (17 HTML-экранов + assets).
- Выделены основные D2C-экраны: каталог, корзина/checkout-сценарии, мои заказы, профиль, login/register.
- Перенесены assets в Flask static:
  - шрифт `Inter_1.ttf`;
  - PNG-иконки/изображения из `design_export/_/image`.

## Что изменено в `base.tpl`
- Убраны старые inline-стили.
- Подключен общий стиль: `{{ url_for('static', filename='css/app.css') }}`.
- Реализован общий shell/layout (`app-shell`, `app-header`, `container`).
- Навигация переведена на текущие Flask/Jinja ссылки через `module_url(...)`.
- Добавлена логика header для:
  - гостя (вход/регистрация, корзина ведет на login);
  - пользователя (каталог, мои заказы, корзина, профиль, выход);
  - админа (дополнительная ссылка на админку).
- Добавлен вывод flash-сообщений в base layout.

## Что добавлено в `app.css`
- Базовая дизайн-система: токены цветов/радиусов/типографики, Inter `@font-face`.
- Общие стили layout/header/nav/buttons/forms/tables/cards.
- Компоненты для каталога и корзины:
  - `product-grid`, `product-card`, `catalog-panel`, `catalog-search`, `catalog-tags`;
  - `cart-layout`, `cart-card`, `cart-summary`, `cart-empty`;
  - `flash-success`, `flash-warning`, `flash-error`.
- Иконки header/страниц через `app/static/images`.

## Какие assets перенесены
- `app/static/fonts/Inter_1.ttf`.
- `app/static/images/*.png` (иконки `list`, `call`, `add_shopping_cart`, `search`, `medicinebottleline` и др.).
- `app/static/css/app.css`.

## Как реализована session-корзина
- Корзина хранится в `Flask session` как dict:
  - ключ: `product_id` (string),
  - значение: `quantity` (int).
- Логика корзины в `app/pharmacy.py`:
  - `get_cart()`, `save_cart()`, `get_cart_count()`, `normalize_cart_quantity()`;
  - очистка невалидных значений/товаров;
  - ограничение количества (`CART_MAX_QUANTITY = 99`);
  - flash-сообщения по ключевым действиям.
- Checkout создает обычный `OrderItem` (без новой DB-модели Cart).
- После успешного checkout корзина очищается.

## Какие routes корзины добавлены
- `GET /cart` -> просмотр корзины (login required).
- `POST /cart/add/<int:product_id>` -> добавить товар.
- `POST /cart/remove/<int:product_id>` -> удалить товар.
- `POST /cart/checkout` -> оформить заказ.

## Что уже изменено в шаблонах сценариев
- `app/templates/products.tpl`:
  - карточки каталога;
  - кнопка "В корзину" (для гостя -> login, для пользователя -> POST add);
  - админские кнопки edit/delete сохранены.
- `app/templates/cart.tpl`:
  - страница корзины;
  - список товаров, quantity, line total, итог;
  - remove и checkout через POST.

## Ограничения, которые остались
- Нет отдельной DB-модели Cart и нет миграций (и не планируется).
- Quantity в заказе хранится повторными `order_items`, а не отдельным полем.
- Поиск/категории в каталоге пока визуальные, backend-фильтрации нет.
- `login.tpl` и `register.tpl` пока отдельные страницы, еще не унифицированы с base-layout.
- Изменяющие действия старого legacy-кода (например некоторые delete по GET) еще существуют и требуют отдельного hardening-этапа.

## Что делать следующим этапом
1. Повторно стабилизировать и регрессионно проверить backend-корзину.
2. После подтверждения стабильности перейти к точечной отрисовке:
   - catalog/cart/orders/profile/login/register;
   - без переписывания backend.

## Важные запреты (не нарушать)
- Не ломать Flask, Flask-Login, Flask-WTF.
- Не ломать админку.
- Не удалять и не ломать Jinja-логику (`module_url`, условия, циклы).
- Не ломать WTForms и существующие поля форм.
- Не менять routes/flows без явной задачи.
- Не вводить миграции/новые DB-модели без отдельного согласования.
