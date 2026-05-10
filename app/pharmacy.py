# -*- coding: utf-8 -*-
import os, sqlite3, pickle, datetime, hashlib
from dataclasses import dataclass, field
from flask import (Blueprint, render_template, request, redirect,
                   url_for, g)
from flask_login import (
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app.forms import (
    LoginForm,
    OrderForm,
    ProductForm,
    ProfileForm,
    RegisterForm,
)

bp = Blueprint('pharmacy', __name__)

_BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH   = os.path.join(_BASE, 'data', 'pharmacy.sqlite')
PKL_PATH  = os.path.join(_BASE, 'data', 'data.pkl')


# ─────────────────────────────────────────────────────────────────
#  Утилита хэширования
# ─────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# ─────────────────────────────────────────────────────────────────
#  Элементы картотеки
# ─────────────────────────────────────────────────────────────────

@dataclass
class UserItem(UserMixin):
    id: int = 0
    name: str = ''
    surname: str = ''
    patronymic: str = ''
    login: str = ''
    password_hash: str = ''
    address: str = ''

    def full_name(self):
        return f"{self.surname} {self.name} {self.patronymic}".strip()

    def initials(self):
        parts = [self.surname, self.name]
        return ''.join(p[0].upper() for p in parts if p)

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return self.full_name()

    def DBLoad(self, r):
        self.id            = r['id']
        self.name          = r['name']
        self.surname       = r['surname']
        self.patronymic    = r['patronymic']
        self.login         = r['login']
        self.password_hash = r['password_hash']
        self.address       = r['address']

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO users VALUES(NULL,?,?,?,?,?,?)",
                (self.name, self.surname, self.patronymic,
                 self.login, self.password_hash, self.address)
            )
        else:
            db.execute(
                "UPDATE users SET name=?,surname=?,patronymic=?,"
                "login=?,address=? WHERE id=?",
                (self.name, self.surname, self.patronymic,
                 self.login, self.address, self.id)
            )

    def Input(self, io):
        self.id         = int(io.Input('id') or 0)
        self.name       = io.Input('name') or ''
        self.surname    = io.Input('surname') or ''
        self.patronymic = io.Input('patronymic') or ''
        self.login      = io.Input('login') or ''
        self.address    = io.Input('address') or ''

    def Output(self, io):
        return io.OutputProfile(self)


@dataclass
class ProductItem:
    id: int = 0
    name: str = ''
    dosage: str = ''
    price: float = 0.0
    in_stock: int = 1

    def __str__(self):
        return f"{self.name} {self.dosage} — {self.price:.0f} руб."

    def DBLoad(self, r):
        self.id       = r['id']
        self.name     = r['name']
        self.dosage   = r['dosage']
        self.price    = r['price']
        self.in_stock = r['in_stock']

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO products VALUES(NULL,?,?,?,?)",
                (self.name, self.dosage, self.price, self.in_stock)
            )
        else:
            db.execute(
                "UPDATE products SET name=?,dosage=?,price=?,in_stock=? WHERE id=?",
                (self.name, self.dosage, self.price, self.in_stock, self.id)
            )

    def Input(self, io):
        self.id       = int(io.Input('id') or 0)
        self.name     = io.Input('name') or ''
        self.dosage   = io.Input('dosage') or ''
        self.price    = float(io.Input('price') or 0)
        self.in_stock = int(io.Input('in_stock') or 1)

    def Output(self, io):
        return io.OutputProduct(self)


@dataclass
class OrderItem:
    id: int = 0
    user_id: int = 0
    payment: str = 'наличные'
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    items: list = field(default_factory=list)

    def total(self):
        return sum(i['price'] for i in self.items)

    def __str__(self):
        return f"Заказ #{self.id} | {self.total():.0f} руб. | {self.payment}"

    def DBLoad(self, r, dbc):
        self.id      = r['id']
        self.user_id = r['user_id']
        self.payment = r['payment']
        self.created = r['created']
        dbc.execute("SELECT * FROM order_items WHERE order_id=?", (self.id,))
        self.items = [
            {'name': i['product_name'],
             'dosage': i['product_dosage'],
             'price': i['price']}
            for i in dbc.fetchall()
        ]

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO orders VALUES(NULL,?,?,?)",
                (self.user_id, self.payment, self.created)
            )
            self.id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        else:
            db.execute(
                "UPDATE orders SET payment=? WHERE id=?",
                (self.payment, self.id)
            )
            db.execute("DELETE FROM order_items WHERE order_id=?", (self.id,))

        for it in self.items:
            db.execute(
                "INSERT INTO order_items VALUES(NULL,?,?,?,?)",
                (self.id, it['name'], it['dosage'], it['price'])
            )

    def Input(self, io):
        self.id      = int(io.Input('id') or 0)
        self.user_id = int(io.Input('user_id') or 0)
        self.payment = io.Input('payment') or 'наличные'
        product_ids  = io.InputList('product_ids')
        storage = get_pharmacy().storage
        self.items = []
        for pid in product_ids:
            p = storage.GetProduct(int(pid))
            if p.id and p.in_stock:
                self.items.append({
                    'name': p.name, 'dosage': p.dosage, 'price': p.price
                })

    def Output(self, io):
        return io.OutputOrder(self)


# ─────────────────────────────────────────────────────────────────
#  Стратегия ввода/вывода
# ─────────────────────────────────────────────────────────────────

class FlaskInputOutput:
    def __init__(self, req):
        self.form = req.form

    def Input(self, field):
        return self.form.get(field)

    def InputList(self, field):
        return self.form.getlist(field)

    def OutputProfile(self, item):
        return render_template('profile.tpl', it=item, form=ProfileForm(obj=item))

    def OutputProduct(self, item):
        return render_template('product_form.tpl', it=item, form=ProductForm(obj=item))

    def OutputOrder(self, item):
        products = list(get_pharmacy().storage.GetProducts())
        form = OrderForm(obj=item)
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        return render_template('order_form.tpl', it=item, products=products, form=form)


# ─────────────────────────────────────────────────────────────────
#  Хранилище
# ─────────────────────────────────────────────────────────────────

class DBStorage:
    def __init__(self):
        self.Load()

    def Load(self):
        self.db = sqlite3.connect(
            DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, surname TEXT, patronymic TEXT,
                login TEXT UNIQUE, password_hash TEXT, address TEXT)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, dosage TEXT, price REAL, in_stock INTEGER)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, payment TEXT, created TIMESTAMP)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS order_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER, product_name TEXT,
                product_dosage TEXT, price REAL)""")
        self.db.commit()
        self.db.row_factory = sqlite3.Row
        self.dbc = self.db.cursor()

    def Store(self):
        self.db.commit()
        self.db.close()

    # --- Auth ---
    def GetUserByLogin(self, login):
        self.dbc.execute("SELECT * FROM users WHERE login=?", (login,))
        r = self.dbc.fetchone()
        if r:
            u = UserItem()
            u.DBLoad(r)
            return u
        return None

    def LoginExists(self, login):
        self.dbc.execute("SELECT id FROM users WHERE login=?", (login,))
        return self.dbc.fetchone() is not None

    def RegisterUser(self, item):
        item.DBStore(self.db)

    # --- Users ---
    def GetUser(self, id):
        item = UserItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM users WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r)
        return item

    def GetUsers(self):
        self.dbc.execute("SELECT * FROM users ORDER BY surname")
        for r in self.dbc:
            u = UserItem()
            u.DBLoad(r)
            yield u

    def UpdateUser(self, item):
        item.DBStore(self.db)

    def UpdatePassword(self, user_id, new_hash):
        self.db.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (new_hash, user_id))

    def DeleteUser(self, id):
        self.db.execute(
            "DELETE FROM order_items WHERE order_id IN "
            "(SELECT id FROM orders WHERE user_id=?)", (id,))
        self.db.execute("DELETE FROM orders WHERE user_id=?", (id,))
        self.db.execute("DELETE FROM users WHERE id=?", (id,))

    # --- Products ---
    def GetProduct(self, id):
        item = ProductItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM products WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r)
        return item

    def GetProducts(self):
        self.dbc.execute("SELECT * FROM products ORDER BY name")
        for r in self.dbc:
            p = ProductItem()
            p.DBLoad(r)
            yield p

    def AddProduct(self, item):
        item.DBStore(self.db)

    def DeleteProduct(self, id):
        self.db.execute("DELETE FROM products WHERE id=?", (id,))

    # --- Orders ---
    def GetOrder(self, id):
        item = OrderItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM orders WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r, self.db.cursor())
        return item

    def GetUserOrders(self, user_id):
        self.dbc.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",
            (user_id,))
        for r in self.dbc.fetchall():
            o = OrderItem()
            o.DBLoad(r, self.db.cursor())
            yield o

    def AddOrder(self, item):
        item.DBStore(self.db)

    def DeleteOrder(self, id):
        self.db.execute("DELETE FROM order_items WHERE order_id=?", (id,))
        self.db.execute("DELETE FROM orders WHERE id=?", (id,))

    # --- Импорт из pickle ЛР2 ---
    def ImportFromPickle(self, path):
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
        except Exception as e:
            return f"Ошибка чтения файла: {e}"

        count_u = count_p = 0
        for u in data.get('users', []):
            if not self.LoginExists(u.get('login', '')):
                self.db.execute(
                    "INSERT INTO users VALUES(NULL,?,?,?,?,?,?)",
                    (u.get('name',''), u.get('surname',''),
                     u.get('patronymic',''), u.get('login',''),
                     hash_password('changeme'), u.get('address','')))
                count_u += 1

        for p in data.get('products', []):
            self.dbc.execute(
                "SELECT id FROM products WHERE name=? AND dosage=?",
                (p.get('name',''), p.get('dosage','')))
            if not self.dbc.fetchone():
                self.db.execute(
                    "INSERT INTO products VALUES(NULL,?,?,?,?)",
                    (p.get('name',''), p.get('dosage',''),
                     p.get('price', 0), int(p.get('in_stock', True))))
                count_p += 1

        self.db.commit()
        note = " (пароль по умолчанию: changeme)" if count_u else ""
        return f"Импортировано: {count_u} пользователей{note}, {count_p} товаров"


# ─────────────────────────────────────────────────────────────────
#  Главный класс
# ─────────────────────────────────────────────────────────────────

class Pharmacy:
    def __init__(self):
        self.storage = DBStorage()
        self.io = FlaskInputOutput(request)

    # --- Auth ---
    def ShowLogin(self, error=''):
        return render_template('login.tpl', error=error, form=LoginForm())

    def DoLogin(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = self.storage.GetUserByLogin(form.login.data)
            if user and user.password_hash == hash_password(form.password.data):
                login_user(user)
                next_url = request.args.get('next')
                return redirect(next_url or url_for('pharmacy.my_orders'))
        return self.ShowLogin(error='Неверный логин или пароль')

    def ShowRegister(self, error=''):
        return render_template('register.tpl', error=error, form=RegisterForm())

    def DoRegister(self):
        form = RegisterForm()
        if not form.validate_on_submit():
            error = next(iter(form.errors.values()))[0] if form.errors else ''
            return self.ShowRegister(error=error)

        login = form.login.data.strip()
        if self.storage.LoginExists(login):
            return self.ShowRegister(error='Логин уже занят')

        u = UserItem(
            name       = (form.name.data or '').strip(),
            surname    = (form.surname.data or '').strip(),
            patronymic = (form.patronymic.data or '').strip(),
            login      = login,
            password_hash = hash_password(form.password.data),
            address    = (form.address.data or '').strip(),
        )
        self.storage.RegisterUser(u)
        self.storage.db.commit()
        user = self.storage.GetUserByLogin(login)
        login_user(user)
        return redirect(url_for('pharmacy.my_orders'))

    def DoLogout(self):
        logout_user()
        return redirect(url_for('pharmacy.login'))

    # --- Профиль ---
    def ShowProfile(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        form = ProfileForm(obj=user)
        return render_template('profile.tpl', it=user, form=form)

    def SaveProfile(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        form = ProfileForm()
        if not form.validate_on_submit():
            return render_template('profile.tpl', it=user, form=form)

        user.name = form.name.data or ''
        user.surname = form.surname.data or ''
        user.patronymic = form.patronymic.data or ''
        user.login = form.login.data or ''
        user.address = form.address.data or ''
        self.storage.UpdateUser(user)

        if form.new_password.data:
            if (user.password_hash == hash_password(form.current_password.data or '')
                    and form.new_password.data == form.confirm_password.data):
                self.storage.UpdatePassword(user.id, hash_password(form.new_password.data))
        return redirect(url_for('pharmacy.profile'))

    # --- Каталог (публичный) ---
    def ShowProducts(self):
        return render_template('products.tpl',
                               products=list(self.storage.GetProducts()))

    def ShowProductForm(self, id):
        item = self.storage.GetProduct(id)
        form = ProductForm(obj=item)
        return render_template('product_form.tpl', it=item, form=form)

    def AddProduct(self):
        item = self.storage.GetProduct(int(request.form.get('id') or 0))
        form = ProductForm()
        if form.validate_on_submit():
            item.name = form.name.data
            item.dosage = form.dosage.data or ''
            item.price = form.price.data
            item.in_stock = form.in_stock.data
            self.storage.AddProduct(item)
            return redirect(url_for('pharmacy.products'))
        return render_template('product_form.tpl', it=item, form=form)

    def DeleteProduct(self, id):
        self.storage.DeleteProduct(id)
        return redirect(url_for('pharmacy.products'))

    # --- Заказы (только своего пользователя) ---
    def ShowMyOrders(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        orders = list(self.storage.GetUserOrders(user.id))
        return render_template('orders.tpl', user=user, orders=orders)

    def ShowOrderForm(self, order_id):
        user_id = int(current_user.get_id())
        order   = self.storage.GetOrder(order_id)
        order.user_id = user_id
        products = list(self.storage.GetProducts())
        form = OrderForm(obj=order)
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        form.product_ids.data = [
            p.id for p in products
            if any(i['name'] == p.name and i['dosage'] == p.dosage for i in order.items)
        ]
        if form.product_ids.data is None:
            form.product_ids.data = []
        return render_template('order_form.tpl', it=order, products=products, form=form)

    def AddOrder(self):
        user_id = int(current_user.get_id())
        item    = self.storage.GetOrder(int(request.form.get('id') or 0))
        item.user_id = user_id
        products = list(self.storage.GetProducts())
        form = OrderForm()
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        if form.product_ids.data is None:
            form.product_ids.data = []
        if form.validate_on_submit():
            item.payment = form.payment.data
            item.items = []
            for pid in form.product_ids.data:
                p = self.storage.GetProduct(pid)
                if p.id and p.in_stock:
                    item.items.append({
                        'name': p.name, 'dosage': p.dosage, 'price': p.price
                    })
            self.storage.AddOrder(item)
            return redirect(url_for('pharmacy.my_orders'))
        return render_template('order_form.tpl', it=item, products=products, form=form)

    def DeleteOrder(self, order_id):
        self.storage.DeleteOrder(order_id)
        return redirect(url_for('pharmacy.my_orders'))

    # --- Импорт ---
    def ImportPickle(self):
        msg = self.storage.ImportFromPickle(PKL_PATH)
        return render_template('import.tpl', msg=msg)


# ─────────────────────────────────────────────────────────────────
#  Per-request singleton
# ─────────────────────────────────────────────────────────────────

def get_pharmacy():
    if 'pharmacy' not in g:
        g.pharmacy = Pharmacy()
    return g.pharmacy


@bp.teardown_app_request
def teardown(ctx):
    p = g.pop('pharmacy', None)
    if p is not None:
        try:
            p.storage.Store()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────
#  Маршруты
# ─────────────────────────────────────────────────────────────────

# Auth
@bp.route("/login", methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pharmacy.my_orders'))
    return get_pharmacy().ShowLogin()

@bp.route("/login", methods=['POST'])
def login_post():
    return get_pharmacy().DoLogin()

@bp.route("/register", methods=['GET'])
def register():
    return get_pharmacy().ShowRegister()

@bp.route("/register", methods=['POST'])
def register_post():
    return get_pharmacy().DoRegister()

@bp.route("/logout")
def logout():
    return get_pharmacy().DoLogout()

# Профиль
@bp.route("/profile", methods=['GET'])
@login_required
def profile():
    return get_pharmacy().ShowProfile()

@bp.route("/profile", methods=['POST'])
@login_required
def profile_save():
    return get_pharmacy().SaveProfile()

# Каталог (доступен всем)
@bp.route("/")
@bp.route("/products")
def products():
    return get_pharmacy().ShowProducts()

@bp.route("/products/form/<int:id>")
@login_required
def product_form(id):
    return get_pharmacy().ShowProductForm(id)

@bp.route("/products/add", methods=['POST'])
@login_required
def product_add():
    return get_pharmacy().AddProduct()

@bp.route("/products/delete/<int:id>")
@login_required
def product_delete(id):
    return get_pharmacy().DeleteProduct(id)

# Мои заказы
@bp.route("/orders")
@login_required
def my_orders():
    return get_pharmacy().ShowMyOrders()

@bp.route("/orders/form/<int:order_id>")
@login_required
def order_form(order_id):
    return get_pharmacy().ShowOrderForm(order_id)

@bp.route("/orders/add", methods=['POST'])
@login_required
def order_add():
    return get_pharmacy().AddOrder()

@bp.route("/orders/delete/<int:order_id>")
@login_required
def order_delete(order_id):
    return get_pharmacy().DeleteOrder(order_id)

# Импорт
@bp.route("/import")
def import_pickle():
    return get_pharmacy().ImportPickle()
