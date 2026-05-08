{% extends "base.tpl" %}
{% block content %}
<h1>Импорт данных из ЛР2</h1>
<p style="color:#546E7A;margin-bottom:20px;">
  Файл: <code>data/data.pkl</code>
</p>
<div class="info-box">{{ msg }}</div>
<div style="display:flex;gap:12px;">
  <a class="btn btn-primary" href="{{ url_for('pharmacy.products') }}">Каталог</a>
</div>
{% endblock %}
