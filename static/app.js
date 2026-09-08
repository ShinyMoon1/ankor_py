/**
 * Проверка формы заказа перед отправкой на сервер.
 * @returns {boolean} true, если форму можно отправлять.
 */
function validateForm() {
    const amount = document.getElementById('famount').value;
    const qty = document.getElementById('fqty').value;
    const customerName = document.getElementById('fname').value;
    if (amount === '' || qty === '') {
        alert('Заполните сумму и количество');
        return false;
    }
    if (isNaN(amount) || isNaN(qty)) {
        alert('Сумма и количество должны быть числами');
        return false;
    }
    if (customerName === '') {
        alert('Укажите покупателя');
        return false;
    }
    return true;
}
