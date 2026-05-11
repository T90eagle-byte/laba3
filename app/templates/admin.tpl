{% extends "base.tpl" %}
{% block content %}
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
  <h1>Админка</h1>
  <div style="display:flex;gap:10px;">
    <a class="btn btn-primary" href="{{ module_url('admin_user_form', user_id=0) }}">+ Пользователь</a>
    <a class="btn btn-purple" href="{{ module_url('product_form', id=0) }}">+ Товар</a>
    <a class="btn btn-gray" href="{{ module_url('import_pickle') }}">Импорт</a>
  </div>
</div>

<h2>Пользователи</h2>
{% if users %}
<table style="margin-bottom:28px;">
  <tr><th>ФИО</th><th>Логин</th><th>Роль</th><th>Адрес</th><th>Действия</th></tr>
  {% for u in users %}
  <tr>
    <td><b>{{ u.full_name() or "Без имени" }}</b></td>
    <td>{{ u.login }}</td>
    <td>
      {% if u.is_admin %}<span class="badge-green">Администратор</span>
      {% else %}<span class="badge-red">Пользователь</span>{% endif %}
    </td>
    <td>{{ u.address }}</td>
    <td style="display:flex;gap:8px;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('admin_user_form', user_id=u.id) }}">Изменить</a>
      {% if u.id != current_user.id %}
      <a class="btn btn-danger btn-sm"
         href="{{ module_url('admin_user_delete', user_id=u.id) }}"
         onclick="return confirm('Удалить пользователя? Его заказы тоже будут удалены.')">Удалить</a>
      {% endif %}
    </td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">Пользователей нет.</p>
{% endif %}

<h2>Товары</h2>
{% if products %}
<table>
  <tr><th>Название</th><th>Дозировка</th><th>Цена</th><th>Наличие</th><th>Действия</th></tr>
  {% for p in products %}
  <tr>
    <td><b>{{ p.name }}</b></td>
    <td>{{ p.dosage }}</td>
    <td>{{ p.price|int }} руб.</td>
    <td>
      {% if p.in_stock %}<span class="badge-green">Есть</span>
      {% else %}<span class="badge-red">Нет</span>{% endif %}
    </td>
    <td style="display:flex;gap:8px;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
      <a class="btn btn-danger btn-sm"
         href="{{ module_url('product_delete', id=p.id) }}"
         onclick="return confirm('Удалить товар?')">Удалить</a>
    </td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">Каталог пуст.</p>
{% endif %}
{% endblock %}
