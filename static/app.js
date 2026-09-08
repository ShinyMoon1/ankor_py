function validateForm() {
    var a = document.getElementById('famount').value;
    var q = document.getElementById('fqty').value;
    if (a == '' || q == '') {
        alert('Заполните сумму и количество');
        return false;
    }
    if (isNaN(a) || isNaN(q)) {
        alert('Сумма и количество должны быть числами');
        return false;
    }
    var n = document.getElementById('fname').value;
    if (n == '') {
        alert('Укажите покупателя');
        return false;
    }
    return true;
}
