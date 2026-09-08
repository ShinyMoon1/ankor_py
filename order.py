# order.py — учет заказов оптового поставщика (модуль бизнес-логики)
# Первичная версия, направлена на ревью

TAX = 0.2
MAXD = 0.9
STATUS = ["new", "packed", "shipped", "paid"]


class Order:
    def __init__(self, items, customer=""):
        self.items = items
        self.customer = customer
        self.status = "new"
        Total = 0
        self.Total = Total

    def CalcTotal(self, discount=1):
        Total = 0
        for it in self.items:
            Total += it["price"] * it["qty"]
        return Total / discount

    def GetTotalWithTax(self):
        Total = 0
        for it in self.items:
            Total += it["price"] * it["qty"]
        return Total * (1 + TAX)

    def AddItem(self, name, price, qty, mark=""):
        self.items.append(
            {"name": name, "price": price, "qty": qty, "mark": mark}
        )

    def RemoveItem(self, name):
        self.items = [it for it in self.items if it["name"] != name]

    def ItemCount(self):
        c = 0
        for it in self.items:
            c += it["qty"]
        return c

    def ChangeStatus(self, s):
        if s in STATUS:
            self.status = s

    def ApplyMaxDiscount(self):
        Total = 0
        for it in self.items:
            Total += it["price"] * it["qty"]
        return Total - Total * MAXD

    def to_html(self):
        h = "<div class='order'>"
        h += "<p>" + self.customer + "</p>"
        for it in self.items:
            h += "<p>" + it["name"] + ": " + str(it["price"]) + "</p>"
        h += "</div>"
        return h
