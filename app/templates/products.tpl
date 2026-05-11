{% extends "base.tpl" %}
{% block content %}
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
  <h1>Каталог товаров</h1>
  {% if current_user.is_authenticated and current_user.is_admin %}
    <a class="btn btn-primary" href="{{ module_url('product_form', id=0) }}">+ Добавить</a>
  {% endif %}
</div>

{% if products %}
<table>
  <tr><th>Название</th><th>Дозировка</th><th>Цена</th><th>Наличие</th>
  {% if current_user.is_authenticated and current_user.is_admin %}<th>Действия</th>{% endif %}</tr>
  {% for p in products %}
  <tr>
    <td><b>{{ p.name }}</b></td>
    <td>{{ p.dosage }}</td>
    <td>{{ p.price|int }} руб.</td>
    <td>
      {% if p.in_stock %}<span class="badge-green">Есть</span>
      {% else %}<span class="badge-red">Нет</span>{% endif %}
    </td>
    {% if current_user.is_authenticated and current_user.is_admin %}
    <td style="display:flex;gap:8px;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
      <a class="btn btn-danger btn-sm"
         href="{{ module_url('product_delete', id=p.id) }}"
         onclick="return confirm('Удалить товар?')">Удалить</a>
    </td>
    {% endif %}
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">Каталог пуст.</p>
{% endif %}
{% endblock %}
