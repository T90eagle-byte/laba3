{% extends "base.tpl" %}
{% block content %}
{% if false %}
<div class="page-heading">
  <div>
    <h1>Корзина</h1>
    <p class="u-muted">Проверьте товары перед оформлением заказа</p>
  </div>
  <a class="btn btn-gray" href="{{ module_url('products') }}">Назад в каталог</a>
</div>

{% if items %}
<div class="cart-layout">
  <section class="cart-items" aria-label="Товары в корзине">
    {% for item in items %}
    <article class="cart-card">
      <div class="cart-card-media" aria-hidden="true">
        <span class="app-icon icon-medicine"></span>
      </div>
      <div class="cart-card-body">
        <h2 class="cart-card-title">{{ item.product.name }}</h2>
        <p class="u-muted">{{ item.product.dosage }}</p>
        <div class="cart-card-meta">
          <span>{{ item.product.price|int }} Р</span>
          <span>{{ item.quantity }} шт.</span>
          <strong>{{ item.line_total|int }} Р</strong>
        </div>
      </div>
      <form action="{{ module_url('cart_remove', product_id=item.product.id) }}" method="post">
        {{ action_form.hidden_tag() }}
        <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
      </form>
    </article>
    {% endfor %}
  </section>

  <aside class="cart-summary" aria-label="Итого">
    <h2>Оплата</h2>
    <div class="cart-summary-row">
      <span>К оплате</span>
      <strong>{{ total|int }} Р</strong>
    </div>
    <div class="cart-summary-row">
      <span>Способ</span>
      <strong>наличные</strong>
    </div>
    <form action="{{ module_url('cart_checkout') }}" method="post">
      {{ action_form.hidden_tag() }}
      <button class="btn btn-primary" type="submit">Оформить заказ</button>
    </form>
  </aside>
</div>
{% else %}
<section class="cart-empty">
  <h2>Корзина пуста</h2>
  <p class="u-muted">Добавьте товары из каталога, чтобы оформить заказ.</p>
  <a class="btn btn-primary" href="{{ module_url('products') }}">Перейти в каталог</a>
</section>
{% endif %}
{% endif %}

<section class="cart-d2c-page" aria-label="Корзина">
  <header class="cart-d2c-top">
    <div class="cart-d2c-title-wrap">
      <h1 class="cart-d2c-title">Корзина</h1>
      <a class="cart-d2c-catalog-link" href="{{ module_url('products') }}">
        <span class="cart-d2c-catalog-icon" aria-hidden="true"></span>
        <span>Каталог</span>
      </a>
    </div>
    <a class="cart-d2c-orders-link" href="{{ module_url('my_orders') }}">
      <span class="cart-d2c-orders-icon" aria-hidden="true"></span>
      <span>Мои заказы</span>
    </a>
  </header>

  <div class="cart-d2c-search" aria-label="Поиск пока недоступен">
    <span class="cart-d2c-search-text">Искать...</span>
    <span class="cart-d2c-search-icon" aria-hidden="true"></span>
  </div>

  {% if items %}
    <div class="cart-d2c-layout">
      <section class="cart-d2c-list" aria-label="Товары в корзине">
        {% for item in items %}
          {% set image_file = product_image(item.product) %}
          <article class="cart-d2c-item">
            <div class="cart-d2c-item-media" style="background-image: url('{{ url_for('static', filename='images/' ~ image_file) }}');"></div>

            <div class="cart-d2c-item-main">
              <h2 class="cart-d2c-item-name">{{ item.product.name }}</h2>
              <p class="cart-d2c-item-dosage">{{ item.product.dosage }}</p>
              <div class="cart-d2c-stock">
                <span class="cart-d2c-stock-icon" aria-hidden="true"></span>
                <span>Есть в наличии</span>
              </div>
              <div class="cart-d2c-item-meta">
                <span class="cart-d2c-item-qty">{{ item.quantity }} шт.</span>
                <span class="cart-d2c-item-unit">{{ item.product.price|int }} Р</span>
              </div>
            </div>

            <div class="cart-d2c-item-side">
              <strong class="cart-d2c-item-total">{{ item.line_total|int }} Р</strong>
              <form action="{{ module_url('cart_remove', product_id=item.product.id) }}" method="post">
                {{ action_form.hidden_tag() }}
                <button class="cart-d2c-remove-btn" type="submit">Удалить</button>
              </form>
            </div>
          </article>
        {% endfor %}
      </section>

      <aside class="cart-d2c-summary" aria-label="Итог заказа">
        <h2 class="cart-d2c-summary-title">Итог</h2>
        <div class="cart-d2c-summary-row">
          <span>Товаров</span>
          <strong>{{ items|length }}</strong>
        </div>
        <div class="cart-d2c-summary-row">
          <span>К оплате</span>
          <strong>{{ total|int }} Р</strong>
        </div>
        <div class="cart-d2c-summary-row">
          <span>Способ</span>
          <strong>наличные</strong>
        </div>

        <form action="{{ module_url('cart_checkout') }}" method="post">
          {{ action_form.hidden_tag() }}
          <button class="cart-d2c-checkout-btn" type="submit">создать заказ</button>
        </form>
      </aside>
    </div>
  {% else %}
    <section class="cart-d2c-empty">
      <h2 class="cart-d2c-empty-title">Корзина пуста</h2>
      <p class="cart-d2c-empty-text">Добавьте товары из каталога, чтобы оформить заказ.</p>
      <a class="cart-d2c-empty-btn" href="{{ module_url('products') }}">Перейти в каталог</a>
    </section>
  {% endif %}
</section>
{% endblock %}
