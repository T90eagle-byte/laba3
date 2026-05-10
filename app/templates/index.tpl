{% extends "base.tpl" %}
{% block content %}
<h1>Добро пожаловать в Invalidhelp</h1>
<p style="color:#546E7A;margin-bottom:24px;">Интернет-аптека — товары для здоровья и красоты</p>
<div style="display:flex;gap:14px;flex-wrap:wrap;">
  <a class="btn btn-purple" href="{{ url_for('pharmacy.products') }}">Каталог товаров</a>
  {% if current_user.is_authenticated %}
    <a class="btn btn-primary" href="{{ url_for('pharmacy.my_orders') }}">Мои заказы</a>
  {% else %}
    <a class="btn btn-primary" href="{{ url_for('pharmacy.login') }}">Войти</a>
  {% endif %}
</div>
{% endblock %}
