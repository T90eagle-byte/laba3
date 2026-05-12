{% extends "base.tpl" %}
{% block content %}
<div class="page-heading">
  <div>
    <h1>Каталог товаров</h1>
    <p class="u-muted">Товары для здоровья и красоты</p>
  </div>
  {% if current_user.is_authenticated and current_user.is_admin %}
    <a class="btn btn-primary" href="{{ module_url('product_form', id=0) }}">+ Добавить</a>
  {% endif %}
</div>

<section class="catalog-panel" aria-label="Навигация по каталогу">
  <div class="catalog-search" aria-label="Поиск пока недоступен">
    <span class="app-icon icon-search" aria-hidden="true"></span>
    <span>Искать...</span>
  </div>
  <div class="catalog-tags" aria-label="Категории">
    <span class="catalog-tag catalog-tag-active">Каталог</span>
    <span class="catalog-tag">Лекарства</span>
    <span class="catalog-tag">Красота</span>
    <span class="catalog-tag">Гигиена</span>
  </div>
</section>

{% if products %}
<section class="product-grid" aria-label="Список товаров">
  {% for p in products %}
  <article class="product-card">
    <div class="product-card-media" aria-hidden="true">
      <span class="app-icon icon-medicine"></span>
    </div>
    <div class="product-card-body">
      <h2 class="product-card-title">{{ p.name }}</h2>
      <p class="product-card-dosage">{{ p.dosage }}</p>
      <div class="product-card-meta">
        <strong>{{ p.price|int }} Р</strong>
        {% if p.in_stock %}
          <span class="badge-green">Есть в наличии</span>
        {% else %}
          <span class="badge-red">Нет в наличии</span>
        {% endif %}
      </div>
    </div>
    <div class="product-card-actions">
      {% if current_user.is_authenticated %}
        <form action="{{ module_url('cart_add', product_id=p.id) }}" method="post">
          {{ action_form.hidden_tag() }}
          <button class="btn btn-primary btn-sm" type="submit" {% if not p.in_stock %}disabled{% endif %}>
            В корзину
          </button>
        </form>
      {% else %}
        <a class="btn btn-primary btn-sm" href="{{ module_url('login') }}">В корзину</a>
      {% endif %}
      {% if current_user.is_authenticated and current_user.is_admin %}
        <div class="product-admin-actions">
          <a class="btn btn-gray btn-sm" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
          <form action="{{ module_url('product_delete', id=p.id) }}" method="post"
                onsubmit="return confirm('Удалить товар?')">
            {{ action_form.hidden_tag() }}
            <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
          </form>
        </div>
      {% endif %}
    </div>
  </article>
  {% endfor %}
</section>
{% else %}
<p class="empty">Каталог пуст.</p>
{% endif %}
{% endblock %}
