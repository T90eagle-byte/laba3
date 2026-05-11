{% extends "base.tpl" %}
{% block content %}
<h1>{{ "Изменить заказ" if it.id else "Новый заказ" }}</h1>
<div class="form-card" style="max-width:600px;">
  <form action="{{ module_url('order_add') }}" method="post">
    {{ form.hidden_tag() }}
    {{ form.id(value=it.id) }}
    {{ form.user_id(value=it.user_id) }}

    <div class="form-group">
      <label>Выберите товары</label>
      {% if products %}
        {% for p in products %}
        <label style="display:flex;align-items:center;gap:10px;padding:9px 14px;
               border-radius:12px;margin-top:6px;cursor:{{ 'pointer' if p.in_stock else 'not-allowed' }};
               background:{{ '#fafafa' if p.in_stock else '#fce4e4' }};">
          <input type="checkbox" name="product_ids" value="{{ p.id }}"
            {{ "checked" if p.id in form.product_ids.data }}
            {{ "disabled" if not p.in_stock }}>
          <span>
            <b>{{ p.name }}</b> {{ p.dosage }} — {{ p.price|int }} руб.
            {% if not p.in_stock %}<span class="badge-red" style="margin-left:6px;">Нет</span>{% endif %}
          </span>
        </label>
        {% endfor %}
      {% else %}
        <p class="empty">Каталог пуст.</p>
      {% endif %}
    </div>

    <div class="form-group" style="margin-top:16px;">
      <label>Способ оплаты</label>
      <input type="text" value="Наличные" disabled>
      {{ form.payment(style='display:none;') }}
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Сохранить заказ</button>
      <a class="btn btn-gray" href="{{ module_url('my_orders') }}">Назад</a>
    </div>
  </form>
</div>
{% endblock %}
