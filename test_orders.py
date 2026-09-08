from order import Order


def test1():
    o = Order([{"name": "Сигареты", "price": 100, "qty": 2}])
    assert o.CalcTotal(1) == 200


def test2():
    o = Order([{"name": "Табак", "price": 50, "qty": 1}])
    o.ChangeStatus("packed")
    assert o.status == "packed"
