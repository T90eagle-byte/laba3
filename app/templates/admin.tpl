{% extends "base.tpl" %}
{% block content %}
{% if false %}
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
  <h1>Админка</h1>
  <div style="display:flex;gap:10px;align-items:center;">
    <a class="btn btn-primary" href="{{ module_url('admin_user_form', user_id=0) }}">+ Пользователь</a>
    <a class="btn btn-purple" href="{{ module_url('product_form', id=0) }}">+ Товар</a>
    <form action="{{ module_url('import_pickle') }}" method="post" style="display:inline;">
      {{ action_form.hidden_tag() }}
      <button class="btn btn-gray" type="submit">Импорт</button>
    </form>
  </div>
</div>

<h2>Пользователи</h2>
{% if users %}
<table style="margin-bottom:28px;">
  <tr><th>ФИО</th><th>Логин</th><th>Роль</th><th>Адрес</th><th>Действия</th></tr>
  {% for u in users %}
  <tr>
    <td><b>{{ u.full_name() or "Без имени" }}</b></td>
    <td>{{ u.login }}</td>
    <td>
      {% if u.is_admin %}<span class="badge-green">Администратор</span>
      {% else %}<span class="badge-red">Пользователь</span>{% endif %}
    </td>
    <td>{{ u.address }}</td>
    <td style="display:flex;gap:8px;align-items:center;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('admin_user_form', user_id=u.id) }}">Изменить</a>
      {% if u.id != current_user.id %}
      <form action="{{ module_url('admin_user_delete', user_id=u.id) }}" method="post"
            onsubmit="return confirm('Удалить пользователя? Его заказы тоже будут удалены.')"
            style="display:inline;">
        {{ action_form.hidden_tag() }}
        <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
      </form>
      {% endif %}
    </td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">Пользователей нет.</p>
{% endif %}

<h2>Товары</h2>
{% if products %}
<table>
  <tr><th>Название</th><th>Дозировка</th><th>Цена</th><th>Наличие</th><th>Действия</th></tr>
  {% for p in products %}
  <tr>
    <td><b>{{ p.name }}</b></td>
    <td>{{ p.dosage }}</td>
    <td>{{ p.price|int }} руб.</td>
    <td>
      {% if p.in_stock %}<span class="badge-green">Есть</span>
      {% else %}<span class="badge-red">Нет</span>{% endif %}
    </td>
    <td style="display:flex;gap:8px;align-items:center;">
      <a class="btn btn-gray btn-sm" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
      <form action="{{ module_url('product_delete', id=p.id) }}" method="post"
            onsubmit="return confirm('Удалить товар?')" style="display:inline;">
        {{ action_form.hidden_tag() }}
        <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
      </form>
    </td>
  </tr>
  {% endfor %}
</table>
{% else %}
<p class="empty">Каталог пуст.</p>
{% endif %}
{% endif %}

<section class="admin-lite-page" aria-label="Админка">
  <header class="admin-lite-header">
    <h1 class="admin-lite-title">Админка</h1>
    <div class="admin-lite-header-actions">
      <a class="btn btn-primary" href="{{ module_url('admin_user_form', user_id=0) }}">+ Пользователь</a>
      <a class="btn btn-purple" href="{{ module_url('product_form', id=0) }}">+ Товар</a>
      <form class="admin-lite-inline-form" action="{{ module_url('import_pickle') }}" method="post">
        {{ action_form.hidden_tag() }}
        <button class="btn btn-gray" type="submit">Импорт</button>
      </form>
    </div>
  </header>

  <section class="admin-lite-section" aria-label="Пользователи">
    <h2 class="admin-lite-section-title">Пользователи</h2>
    {% if users %}
      <div class="admin-lite-table-wrap">
        <table class="admin-lite-table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Логин</th>
              <th>Роль</th>
              <th>Адрес</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {% for u in users %}
              <tr>
                <td><b>{{ u.full_name() or "Без имени" }}</b></td>
                <td>{{ u.login }}</td>
                <td>
                  {% if u.is_admin %}
                    <span class="badge-green">Администратор</span>
                  {% else %}
                    <span class="badge-red">Пользователь</span>
                  {% endif %}
                </td>
                <td>{{ u.address }}</td>
                <td class="admin-lite-actions-cell">
                  <a class="btn btn-gray btn-sm" href="{{ module_url('admin_user_form', user_id=u.id) }}">Изменить</a>
                  {% if u.id != current_user.id %}
                    <form
                      class="admin-lite-inline-form"
                      action="{{ module_url('admin_user_delete', user_id=u.id) }}"
                      method="post"
                      onsubmit="return confirm('Удалить пользователя? Его заказы тоже будут удалены.')"
                    >
                      {{ action_form.hidden_tag() }}
                      <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
                    </form>
                  {% endif %}
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    {% else %}
      <p class="empty admin-lite-empty">Пользователей нет.</p>
    {% endif %}
  </section>

  <section class="admin-lite-section" aria-label="Товары">
    <h2 class="admin-lite-section-title">Товары</h2>
    {% if products %}
      <div class="admin-lite-table-wrap">
        <table class="admin-lite-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Дозировка</th>
              <th>Цена</th>
              <th>Наличие</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {% for p in products %}
              <tr>
                <td><b>{{ p.name }}</b></td>
                <td>{{ p.dosage }}</td>
                <td>{{ p.price|int }} руб.</td>
                <td>
                  {% if p.in_stock %}
                    <span class="badge-green">Есть</span>
                  {% else %}
                    <span class="badge-red">Нет</span>
                  {% endif %}
                </td>
                <td class="admin-lite-actions-cell">
                  <a class="btn btn-gray btn-sm" href="{{ module_url('product_form', id=p.id) }}">Изменить</a>
                  <form
                    class="admin-lite-inline-form"
                    action="{{ module_url('product_delete', id=p.id) }}"
                    method="post"
                    onsubmit="return confirm('Удалить товар?')"
                  >
                    {{ action_form.hidden_tag() }}
                    <button class="btn btn-danger btn-sm" type="submit">Удалить</button>
                  </form>
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    {% else %}
      <p class="empty admin-lite-empty">Каталог пуст.</p>
    {% endif %}
  </section>
</section>
{% endblock %}
