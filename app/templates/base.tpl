<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Invalidhelp</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body>
<div class="app-shell">
  <header class="app-header">
    <a class="nav-logo" href="{{ module_url('products') }}">Invalidhelp</a>

    <nav class="app-nav" aria-label="Основная навигация">
      <a class="nav-catalog" href="{{ module_url('products') }}">
        <span class="nav-icon nav-icon-list" aria-hidden="true"></span>
        <span>Каталог</span>
      </a>
      {% if current_user.is_authenticated %}
        <a class="nav-link" href="{{ module_url('my_orders') }}">Мои заказы</a>
        {% if current_user.is_admin %}
          <a class="nav-link" href="{{ module_url('admin') }}">Админка</a>
        {% endif %}
      {% endif %}
    </nav>

    <div class="nav-spacer"></div>

    <div class="nav-support" aria-label="Служба поддержки">
      <span class="nav-icon nav-icon-call" aria-hidden="true"></span>
      <span>+7 (800) 500 69 69</span>
    </div>

    <div class="nav-actions">
      {% if current_user.is_authenticated %}
        {% set header_cart_count = cart_count() %}
        <a class="nav-cart" href="{{ module_url('cart') }}" title="Корзина">
          <span class="nav-icon nav-icon-cart" aria-hidden="true"></span>
          <span>Корзина</span>
          {% if header_cart_count %}
            <span class="nav-cart-count">{{ header_cart_count }}</span>
          {% endif %}
        </a>
        <a class="nav-profile" href="{{ module_url('profile') }}" title="Настройки профиля">
          <span class="nav-avatar">{{ current_user.initials() }}</span>
          <span class="nav-profile-name">{{ current_user.full_name() or current_user.login }}</span>
        </a>
        <form class="nav-logout-form" action="{{ module_url('logout') }}" method="post">
          {{ action_form.hidden_tag() }}
          <button class="nav-link nav-link-logout nav-logout-button" type="submit">Выйти</button>
        </form>
      {% else %}
        <a class="nav-cart nav-cart-muted" href="{{ module_url('login') }}" title="Войдите, чтобы создать заказ">
          <span class="nav-icon nav-icon-cart" aria-hidden="true"></span>
          <span>Корзина</span>
        </a>
        <a class="nav-link" href="{{ module_url('login') }}">Войти</a>
        <a class="btn btn-primary btn-sm" href="{{ module_url('register') }}">Регистрация</a>
      {% endif %}
    </div>
  </header>

  <main class="container">
    {% with messages = get_flashed_messages(with_categories=True) %}
      {% if messages %}
        <div class="flash-messages" role="status" aria-live="polite">
          {% for category, message in messages %}
            <div class="flash-message flash-{{ category }}">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </main>
</div>
</body>
</html>
