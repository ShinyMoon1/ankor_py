"""Серверная часть системы учета заказов (Flask).

Маршруты тонкие: валидация форм здесь, расчет стоимости —
в модуле order.py. Формы защищены CSRF-токеном из сессии.
"""

import secrets

from flask import Flask, request, render_template, session

from order import Order

app = Flask(__name__)
app.secret_key = "ankor-dev-secret-key"
ORDERS = []


def _new_csrf_token():
    """Создание CSRF-токена для формы заказа."""
    token = secrets.token_hex(16)
    session["csrf_token"] = token
    return token


@app.route("/")
def index():
    """Главная страница со списком заявок."""
    return render_template(
        "order.html", orders=ORDERS, csrf_token=_new_csrf_token()
    )


@app.route("/order", methods=["GET", "POST"])
def order_detail():
    """Создание заказа из формы менеджера.

    Проверяет CSRF-токен и числовые поля, затем делегирует
    расчет модулю order.py.
    """
    if request.method == "GET":
        return render_template(
            "order.html", orders=ORDERS,
            csrf_token=_new_csrf_token(),
        )
    if request.form.get("csrf_token") != session.get("csrf_token"):
        return render_template(
            "error.html", message="Недействительный CSRF-токен.",
        ), 403
    customer_name = request.form.get("name", "").strip()
    if not customer_name:
        return render_template(
            "error.html", message="Укажите покупателя.",
        ), 400
    try:
        amount = float(request.form.get("amount", ""))
        qty = int(request.form.get("qty", 1))
    except ValueError:
        return render_template(
            "error.html",
            message="Сумма и количество должны быть числами.",
        ), 400
    order = Order(
        [{"name": customer_name, "price": amount, "qty": qty}]
    )
    ORDERS.append(order)
    total = order.calculate_total(1)
    return render_template("order.html", orders=ORDERS, total=total)


@app.route("/status", methods=["POST"])
def change_order_status():
    """Смена статуса заявки со склада."""
    idx = int(request.form.get("idx", -1))
    if 0 <= idx < len(ORDERS):
        order = ORDERS[idx]
        if isinstance(order, Order):
            order.change_status(request.form.get("status", ""))
    return render_template("order.html", orders=ORDERS)


if __name__ == "__main__":
    app.run(debug=True)
