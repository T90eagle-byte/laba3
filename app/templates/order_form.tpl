{% extends "base.tpl" %}
{% block content %}
<section class="order-form-d2c-page" aria-label="Форма заказа">
  <header class="order-form-d2c-head">
    <h1 class="order-form-d2c-title">{{ "Изменить заказ" if it.id else "Новый заказ" }}</h1>
    <a class="order-form-d2c-back" href="{{ module_url('my_orders') }}">Назад</a>
  </header>

  <form class="order-form-d2c-card" action="{{ module_url('order_add') }}" method="post">
    {{ form.hidden_tag() }}
    {{ form.id(value=it.id) }}
    {{ form.user_id(value=it.user_id) }}

    <section class="order-form-d2c-products" aria-label="Выбор товаров">
      <h2 class="order-form-d2c-subtitle">Выберите товары</h2>
      {% if products %}
        <div class="order-form-d2c-grid">
          {% for p in products %}
            {% set image_file = product_image(p) %}
            <label class="order-form-d2c-item{% if not p.in_stock %} is-disabled{% endif %}">
              <span
                class="order-form-d2c-item-media"
                style="background-image: url('{{ url_for('static', filename='images/' ~ image_file) }}');"
                aria-hidden="true"
              ></span>
              <span class="order-form-d2c-item-main">
                <span class="order-form-d2c-item-name">{{ p.name }}</span>
                <span class="order-form-d2c-item-dosage">{{ p.dosage or 'Без дозировки' }}</span>
                <span class="order-form-d2c-item-price">{{ p.price|int }} Р</span>
              </span>
              <span class="order-form-d2c-item-side">
                <input
                  class="order-form-d2c-check"
                  type="checkbox"
                  name="product_ids"
                  value="{{ p.id }}"
                  {{ "checked" if p.id in form.product_ids.data }}
                  {{ "disabled" if not p.in_stock }}
                >
                {% if p.in_stock %}
                  <span class="badge-green">Есть</span>
                {% else %}
                  <span class="badge-red">Нет</span>
                {% endif %}
              </span>
            </label>
          {% endfor %}
        </div>
      {% else %}
        <p class="empty">Каталог пуст.</p>
      {% endif %}
    </section>

    <section class="order-form-d2c-payment" aria-label="Оплата">
      <h2 class="order-form-d2c-subtitle">Способ оплаты</h2>
      <input class="order-form-d2c-payment-input" type="text" value="Наличные" disabled>
      {{ form.payment(style='display:none;') }}
    </section>

    <div class="order-form-d2c-actions">
      <button class="btn btn-primary" type="submit">Сохранить заказ</button>
      <a class="btn btn-gray" href="{{ module_url('my_orders') }}">Назад</a>
    </div>
  </form>
</section>
{% endblock %}
