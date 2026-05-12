{% extends "base.tpl" %}
{% block content %}
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
{% endblock %}
