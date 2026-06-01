{% extends "base.tpl" %}
{% block content %}
{% if false %}
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
{% endif %}

{% set catalog_images = [
  '70b63ef52bb9c8e4a75f3a6c46afb62e8b21d8c3.png',
  '8af2af4ea1fe6457c7dfbeb1d53e527d1ce6b985.png',
  '8cf2c29fefeef2f884c05aa49a43170c2f0f9d92.png'
] %}

<section class="catalog-d2c-page" aria-label="Каталог товаров">
  <header class="catalog-d2c-top">
    <div class="catalog-d2c-heading">
      <h1 class="catalog-d2c-title">Каталог</h1>
      <p class="catalog-d2c-subtitle">Витамины и БАД</p>
    </div>
    {% if current_user.is_authenticated and current_user.is_admin %}
      <a class="catalog-d2c-admin-add" href="{{ module_url('product_form', id=0) }}">+ Добавить</a>
    {% endif %}
  </header>

  <section class="catalog-d2c-controls" aria-label="Фильтры каталога">
    <div class="catalog-d2c-active-category">
      <span class="catalog-d2c-active-icon" aria-hidden="true"></span>
      <span class="catalog-d2c-active-text">Каталог</span>
    </div>
    <form class="catalog-d2c-search-form" action="{{ module_url('products') }}" method="get" role="search">
      <label class="catalog-d2c-search" aria-label="Поиск товаров">
        <input
          class="catalog-d2c-search-input"
          type="search"
          name="q"
          value="{{ search_query or '' }}"
          placeholder="Искать..."
        >
        <button class="catalog-d2c-search-submit" type="submit" aria-label="Найти"></button>
      </label>
    </form>
  </section>

  <div class="catalog-d2c-categories" aria-label="Категории">
    <span class="catalog-d2c-category catalog-d2c-category-active">
      <span class="catalog-d2c-category-arrow" aria-hidden="true"></span>
      <span>Лекарства</span>
      <span class="catalog-d2c-category-arrow" aria-hidden="true"></span>
    </span>
    <span class="catalog-d2c-category">Красота</span>
    <span class="catalog-d2c-category">Гигиена</span>
  </div>

  {% if products %}
    <section class="catalog-d2c-grid" aria-label="Список товаров">
      {% for p in products %}
        {% set product_name_key = (p.name or '')|lower %}
        {% if 'кур' in product_name_key %}
          {% set image_file = '70b63ef52bb9c8e4a75f3a6c46afb62e8b21d8c3.png' %}
        {% elif 'греч' in product_name_key %}
          {% set image_file = '8cf2c29fefeef2f884c05aa49a43170c2f0f9d92.png' %}
        {% elif 'рис' in product_name_key %}
          {% set image_file = '8af2af4ea1fe6457c7dfbeb1d53e527d1ce6b985.png' %}
        {% else %}
          {% set image_file = catalog_images[loop.index0 % (catalog_images|length)] %}
        {% endif %}
        <article class="catalog-d2c-card">
          <div class="catalog-d2c-media" style="background-image: url('{{ url_for('static', filename='images/' ~ image_file) }}');"></div>

          <div class="catalog-d2c-body">
            <h2 class="catalog-d2c-name">{{ p.name }}</h2>
            <p class="catalog-d2c-dosage">{{ p.dosage or 'Без дозировки' }}</p>
            <p class="catalog-d2c-price">{{ p.price|int }} Р</p>

            {% if p.in_stock %}
              <div class="catalog-d2c-stock is-in-stock">
                <span class="catalog-d2c-stock-icon" aria-hidden="true"></span>
                <span>Есть в наличии</span>
              </div>
            {% else %}
              <div class="catalog-d2c-stock is-out-stock">
                <span class="catalog-d2c-stock-icon" aria-hidden="true"></span>
                <span>Нет в наличии</span>
              </div>
            {% endif %}
          </div>

          <div class="catalog-d2c-actions">
            {% if current_user.is_authenticated %}
              <form action="{{ module_url('cart_add', product_id=p.id) }}" method="post">
                {{ action_form.hidden_tag() }}
                <button class="catalog-d2c-cart-btn" type="submit" {% if not p.in_stock %}disabled{% endif %}>
                  В корзину
                </button>
              </form>
            {% else %}
              <a class="catalog-d2c-cart-btn catalog-d2c-cart-link" href="{{ module_url('login') }}">В корзину</a>
            {% endif %}

            {% if current_user.is_authenticated and current_user.is_admin %}
              <div class="catalog-d2c-admin-actions">
                <a class="catalog-d2c-edit-btn" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
                <form action="{{ module_url('product_delete', id=p.id) }}" method="post"
                      onsubmit="return confirm('Удалить товар?')">
                  {{ action_form.hidden_tag() }}
                  <button class="catalog-d2c-delete-btn" type="submit">Удалить</button>
                </form>
              </div>
            {% endif %}
          </div>
        </article>
      {% endfor %}
    </section>
  {% else %}
    {% if search_query %}
      <p class="catalog-d2c-empty">По запросу "{{ search_query }}" товары не найдены.</p>
    {% else %}
      <p class="catalog-d2c-empty">Каталог пуст.</p>
    {% endif %}
  {% endif %}
</section>
{% endblock %}
