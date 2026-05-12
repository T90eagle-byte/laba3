# CHANGELOG

## 2026-05-12 — Backend stabilization checkpoint

- D2C assets из `design_export` перенесены и подключены в `app/static`.
- Подключен и используется общий стиль `app/static/css/app.css`.
- `base.tpl` обновлен под общий layout/header/nav и flash-сообщения.
- Реализована session-корзина (`/cart`, `/cart/add`, `/cart/remove`, `/cart/checkout`) без новой DB-модели Cart.
- Проведен backend-аудит соответствия требованиям.
- Обязательные security-пункты закрыты:
  - state-changing маршруты переведены на POST;
  - для критичных POST-действий подключен CSRF через Flask-WTF;
  - добавлен контроль доступа к чужим заказам.
- Хэширование паролей переведено на Werkzeug (`generate_password_hash` / `check_password_hash`).
- Поддержан legacy `sha256` и добавлен автоматический апгрейд legacy-хэша при успешном входе.
- Проверки `py_compile` и интеграционные smoke-проверки через Flask test client прошли.
