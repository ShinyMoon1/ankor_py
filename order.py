"""Модуль бизнес-логики учета заказов оптового поставщика.

Класс Order хранит позиции заявки розничной точки, считает
стоимость с учетом скидки, следит за статусом комплектации
и контролирует коды маркировки табачной номенклатуры.
"""

TAX_RATE = 0.2
MAX_DISCOUNT = 0.9
STATUSES = ["new", "packed", "shipped", "paid"]


class Order:
    """Заказ клиента."""

    def __init__(self, items, customer=""):
        """Создание заказа из списка позиций.

        Args:
            items: список словарей с ключами name, price, qty, mark.
            customer: название розничной точки.

        Raises:
            ValueError: если список позиций пуст или равен None.
        """
        if items is None:
            raise ValueError("items is None")
        if not items:
            raise ValueError("items is empty")
        self.items = items
        self.customer = customer
        self.status = "new"
        self._cached_total = None

    def _subtotal(self):
        """Промежуточная сумма позиций без скидки и налога."""
        total = 0
        for item in self.items:
            total += item["price"] * item["qty"]
        return total

    def _invalidate_cache(self):
        """Сброс кэшированной суммы после изменения позиций."""
        self._cached_total = None

    def calculate_total(self, discount=1):
        """Расчет стоимости заказа с учетом скидки.

        Args:
            discount: делитель купона (1 — без скидки,
                2 — скидка 50 процентов).

        Returns:
            Итоговая стоимость заказа.

        Raises:
            ZeroDivisionError: если делитель купона равен нулю.
        """
        if discount == 0:
            raise ZeroDivisionError("discount is zero")
        if self._cached_total is None:
            self._cached_total = self._subtotal()
        return self._cached_total / discount

    def total_with_tax(self):
        """Стоимость заказа с учетом налога."""
        if self._cached_total is None:
            self._cached_total = self._subtotal()
        return self._cached_total * (1 + TAX_RATE)

    def add_item(self, name, price, qty, mark=""):
        """Добавление позиции в заказ.

        Args:
            name: наименование товара.
            price: цена за единицу.
            qty: количество.
            mark: код маркировки (для табачной номенклатуры).
        """
        self.items.append(
            {"name": name, "price": price, "qty": qty, "mark": mark}
        )
        self._invalidate_cache()

    def remove_item(self, name):
        """Удаление всех позиций с указанным наименованием."""
        self.items = [
            item for item in self.items if item["name"] != name
        ]
        self._invalidate_cache()

    def item_count(self):
        """Общее количество единиц товара в заказе."""
        count = 0
        for item in self.items:
            count += item["qty"]
        return count

    def change_status(self, new_status):
        """Смена статуса комплектации заказа.

        Args:
            new_status: одно из значений STATUSES.
        """
        if new_status in STATUSES:
            self.status = new_status

    def discounted_total(self):
        """Стоимость заказа с максимальной скидкой за объем."""
        if self._cached_total is None:
            self._cached_total = self._subtotal()
        return self._cached_total * (1 - MAX_DISCOUNT)

    def unmarked_items(self):
        """Позиции без кода маркировки.

        Табачная номенклатура отпускается только с кодом
        маркировки, поэтому менеджер проверяет этот список
        перед отправкой заявки на склад.

        Returns:
            Список наименований позиций без кода маркировки.
        """
        return [
            item["name"] for item in self.items if not item.get("mark")
        ]

    def to_dict(self):
        """Словарь заказа для шаблонов страниц и отчетов.

        Returns:
            Словарь с покупателем, статусом, позициями
            и итоговой суммой без скидки.
        """
        return {
            "customer": self.customer,
            "status": self.status,
            "items": list(self.items),
            "total": self._subtotal(),
        }


def format_order(order):
    """Форматирование заказа в HTML для страницы списка заявок.

    Args:
        order: экземпляр класса Order.

    Returns:
        Строка с HTML-разметкой карточки заказа.
    """
    lines = ["<div class='order'>", "<p>" + order.customer + "</p>"]
    for item in order.items:
        lines.append(
            "<p>" + item["name"] + ": " + str(item["price"]) + "</p>"
        )
    lines.append("</div>")
    return "".join(lines)
