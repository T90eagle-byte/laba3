{% extends "base.tpl" %}
{% block content %}
<h1>{{ "Изменить заказ" if it.id else "Новый заказ" }}</h1>
<div class="form-card" style="max-width:600px;">
  <form action="{{ url_for('pharmacy.order_add') }}" method="post">
    <input type="hidden" name="id" value="{{ it.id }}">
    <input type="hidden" name="user_id" value="{{ it.user_id }}">

    <div class="form-group">
      <label>Выберите товары</label>
      {% if products %}
        {% for p in products %}
        <label style="display:flex;align-items:center;gap:10px;padding:9px 14px;
               border-radius:12px;margin-top:6px;cursor:{{ 'pointer' if p.in_stock else 'not-allowed' }};
               background:{{ '#fafafa' if p.in_stock else '#fce4e4' }};">
          <input type="checkbox" name="product_ids" value="{{ p.id }}"
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
      <select name="payment">
        <option value="наличные" {{ "selected" if it.payment=="наличные" }}>Наличные</option>
        <option value="карта"    {{ "selected" if it.payment=="карта" }}>Карта</option>
        <option value="онлайн"   {{ "selected" if it.payment=="онлайн" }}>Онлайн</option>
      </select>
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Сохранить заказ</button>
      <a class="btn btn-gray" href="{{ url_for('pharmacy.my_orders') }}">Назад</a>
    </div>
  </form>
</div>
{% endblock %}
