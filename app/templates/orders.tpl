{% extends "base.tpl" %}
{% block content %}
{% if false %}
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
{% endif %}

{% set order_images = [
  '70b63ef52bb9c8e4a75f3a6c46afb62e8b21d8c3.png',
  '8af2af4ea1fe6457c7dfbeb1d53e527d1ce6b985.png',
  '8cf2c29fefeef2f884c05aa49a43170c2f0f9d92.png'
] %}

<section class="orders-d2c-page" aria-label="Мои заказы">
  <header class="orders-d2c-top">
    <div class="orders-d2c-heading">
      <h1 class="orders-d2c-title">Мои заказы</h1>
      <p class="orders-d2c-user">{{ user.full_name() }}</p>
    </div>
    <div class="orders-d2c-top-actions">
      <a class="orders-d2c-back-link" href="{{ module_url('products') }}">
        <span class="orders-d2c-back-icon" aria-hidden="true"></span>
        <span>Назад</span>
      </a>
      <a class="orders-d2c-create-link" href="{{ module_url('order_form', order_id=0) }}">создать заказ</a>
    </div>
  </header>

  {% if orders %}
    <section class="orders-d2c-list" aria-label="Список заказов">
      {% for o in orders %}
        <article class="orders-d2c-card">
          <header class="orders-d2c-card-head">
            <h2 class="orders-d2c-order-number">Заказ {{ o.id }}</h2>
            <div class="orders-d2c-order-meta">
              <span class="orders-d2c-payment">{{ o.payment }}</span>
              <span class="orders-d2c-date">{{ o.created.strftime('%d.%m.%Y') if o.created else '—' }}</span>
            </div>
          </header>

          {% if o.items %}
            <ul class="orders-d2c-items">
              {% for item in o.items %}
                {% set image_file = order_images[(loop.index0 + o.id) % (order_images|length)] %}
                <li class="orders-d2c-item">
                  <div class="orders-d2c-item-image" style="background-image: url('{{ url_for('static', filename='images/' ~ image_file) }}');"></div>
                  <div class="orders-d2c-item-main">
                    <p class="orders-d2c-item-name">{{ item.name }}</p>
                    <p class="orders-d2c-item-dosage">{{ item.dosage }}</p>
                  </div>
                  <strong class="orders-d2c-item-price">{{ item.price|int }} Р</strong>
                </li>
              {% endfor %}
            </ul>
          {% else %}
            <p class="orders-d2c-empty-items">В заказе пока нет товаров.</p>
          {% endif %}

          <footer class="orders-d2c-card-foot">
            <p class="orders-d2c-total">Итого: <strong>{{ o.total()|int }} Р</strong></p>
            <div class="orders-d2c-actions">
              <a class="orders-d2c-edit-btn" href="{{ module_url('order_form', order_id=o.id) }}">изменить заказ</a>
              <form action="{{ module_url('order_delete', order_id=o.id) }}" method="post"
                    onsubmit="return confirm('Удалить заказ?')">
                {{ action_form.hidden_tag() }}
                <button class="orders-d2c-cancel-btn" type="submit">отменить заказ</button>
              </form>
            </div>
          </footer>
        </article>
      {% endfor %}
    </section>
  {% else %}
    <section class="orders-d2c-empty">
      <h2 class="orders-d2c-empty-title">Мои заказы</h2>
      <p class="orders-d2c-empty-text">На текущий момент список ваших заказов пуст</p>
      <div class="orders-d2c-empty-actions">
        <a class="orders-d2c-back-link" href="{{ module_url('products') }}">
          <span class="orders-d2c-back-icon" aria-hidden="true"></span>
          <span>Назад</span>
        </a>
        <a class="orders-d2c-create-link" href="{{ module_url('order_form', order_id=0) }}">создать заказ</a>
      </div>
    </section>
  {% endif %}
</section>
{% endblock %}
