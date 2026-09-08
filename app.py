from flask import Flask, request, render_template
from order import Order

app = Flask(__name__)
ORDERS = []


@app.route("/")
def index():
    return render_template("order.html", orders=ORDERS)


@app.route("/order", methods=["GET", "POST"])
def f1():
    s = request.form["name"]
    amount = float(request.form["amount"])
    qty = int(request.form.get("qty", 1))
    Total = 0
    for i in range(qty):
        Total += amount
    ORDERS.append({"name": s, "total": Total})
    return render_template("order.html", orders=ORDERS, total=Total)


@app.route("/status", methods=["POST"])
def chstatus():
    s = request.form["idx"]
    o = ORDERS[int(s)]
    if isinstance(o, Order):
        o.ChangeStatus(request.form["st"])
    return render_template("order.html", orders=ORDERS)


if __name__ == "__main__":
    app.run(debug=True)
