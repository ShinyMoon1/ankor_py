"""Тесты модуля order.py (pytest)."""

import pytest

from order import Order, format_order


def test_calculate_total_with_discount_returns_correct():
    """Скидка с делителем 2 дает половину суммы позиций."""
    order = Order([{"name": "Сигареты", "price": 100, "qty": 2}])
    assert order.calculate_total(2) == 100


def test_calculate_total_without_discount_returns_subtotal():
    """Делитель 1 возвращает полную сумму позиций."""
    order = Order([{"name": "Табак", "price": 50, "qty": 3}])
    assert order.calculate_total(1) == 150


def test_discount_zero_raises():
    """Нулевой делитель купона выбрасывает ZeroDivisionError."""
    order = Order([{"name": "Сигареты", "price": 100, "qty": 1}])
    with pytest.raises(ZeroDivisionError):
        order.calculate_total(0)


def test_none_items_raises():
    """Конструктор с None выбрасывает ValueError."""
    with pytest.raises(ValueError):
        Order(None)


def test_empty_items_raises():
    """Конструктор с пустым списком выбрасывает ValueError."""
    with pytest.raises(ValueError):
        Order([])


def test_change_status_updates_status():
    """Смена статуса фиксирует новое состояние заказа."""
    order = Order([{"name": "Табак", "price": 50, "qty": 1}])
    order.change_status("packed")
    assert order.status == "packed"


def test_format_order_contains_customer():
    """HTML-карточка содержит название розничной точки."""
    order = Order(
        [{"name": "Сигареты", "price": 100, "qty": 1}],
        customer="Ларек 5",
    )
    assert "Ларек 5" in format_order(order)


def test_unmarked_items_lists_positions_without_mark():
    """Позиции без кода маркировки попадают в список проверки."""
    order = Order([
        {"name": "Сигареты", "price": 100, "qty": 1, "mark": "01046"},
        {"name": "Табак", "price": 50, "qty": 1},
    ])
    assert order.unmarked_items() == ["Табак"]


def test_add_item_invalidates_cached_total():
    """Добавление позиции сбрасывает кэшированную сумму."""
    order = Order([{"name": "Сигареты", "price": 100, "qty": 1}])
    assert order.calculate_total(1) == 100
    order.add_item("Табак", 50, 1)
    assert order.calculate_total(1) == 150
