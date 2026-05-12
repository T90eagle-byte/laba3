{% extends "base.tpl" %}
{% block content %}
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
  <div>
    <h1>Мои заказы</h1>
    <p style="color:#546E7A;margin-top:4px;">{{ user.full_name() }}</p>
  </div>
  <a class="btn btn-primary" href="{{ module_url('order_form', order_id=0) }}">+ Новый заказ</a>
</div>

{% if orders %}
<table>
  <tr><th>#</th><th>Состав</th><th>Итого</th><th>Оплата</th><th>Дата</th><th>Действия</th></tr>
  {% for o in orders %}
  <tr>
    <td>{{ o.id }}</td>
    <td>
      {% for item in o.items %}
        <span style="display:inline-block;background:#f3e5f5;color:#7B1FA2;
              padding:2px 8px;border-radius:12px;font-size:.78rem;margin:2px;">
          {{ item.name }} {{ item.dosage }}
        </span>
      {% endfor %}
    </td>
    <td><b>{{ o.total()|int }} руб.</b></td>
    <td>{{ o.payment }}</td>
    <td style="font-size:.82rem;color:#90A4AE;">
      {{ o.created.strftime('%d.%m.%Y') if o.created else '—' }}
    </td>
    <td style="display:flex;gap:8px;align-items:center;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('order_form', order_id=o.id) }}">Изменить</a>
      <form action="{{ module_url('order_delete', order_id=o.id) }}" method="post"
            onsubmit="return confirm('Удалить заказ?')" style="display:inline;">
        {{ action_form.hidden_tag() }}
        <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
      </form>
    </td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">На текущий момент список ваших заказов пуст.</p>
{% endif %}
{% endblock %}
