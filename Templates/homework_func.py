"""
Домашние задания на работу с функциями в Python
Бизнес-ориентированные задачи
"""

# ============================================================================
# ЗАДАНИЕ 1: Расчет скидки
# ============================================================================
# Напишите функцию calc_discount, которая принимает цену
# и процент скидки, возвращает цену со скидкой.
# Вызовите функцию для товара стоимостью 1500 руб. со скидкой 15%.

# Ваш код здесь:
def calc_discount(price, discount):
    return price - price * discount / 100
result = calc_discount(1500, 15)
print(result)
# ============================================================================
# ЗАДАНИЕ 2: Приветствие клиента
# ============================================================================
# Напишите функцию greet_client, которая возвращает
# строку приветствия. Для VIP-клиентов добавьте " (VIP)" в конец.
# Примеры:
#   greet_client("Иван") -> "Добро пожаловать, Иван!"
#   greet_client("Анна", is_vip=True) -> "Добро пожаловать, Анна! (VIP)"

# Ваш код здесь:
def greet_client(name, is_vip=False):
    if is_vip:
        return f"Добро пожаловать, {name}! (VIP)"
    else:
        return f"Добро пожаловать, {name}!"
print(greet_client("Петр"))
print(greet_client("Ольга", is_vip=True))
# ============================================================================
# ЗАДАНИЕ 3: Проверка ИНН
# ============================================================================
# Напишите функцию is_valid_inn, которая проверяет:
# - ИНН должен быть строкой
# - Длина 10 (юрлицо) или 12 (физлицо) символов
# - Все символы — цифры
# Верните True/False. Проитерируйтесь по всему списку

test_inns = ["7701234567", "77012345", "770123456A", "771234567890"]

# Ваш код здесь:
def is_valid_inn(inn):
    if not isinstance(inn, str) or not inn.isdigit():
        return False
    if len(inn) not in (10, 12):
        return False
    else:return True
for inn in test_inns:
    print(inn, ":", is_valid_inn(inn))
# ============================================================================
# ЗАДАНИЕ 4: Расчет бонусов менеджера
# ============================================================================
# Напишите функцию calc_bonus, которая считает бонус
# менеджера как процент от суммы продаж. rate по умолчанию 5%.
# Посчитайте бонусы для трех менеджеров:

sales_data = {
    "Иван": 150000,
    "Ольга": 230000,
    "Дмитрий": 95000,
}

# Ваш код здесь:
def calc_bonus(sales, rate=5):
        return sales * rate / 100
for name, sales in sales_data.items():
        print(name, ":", calc_bonus(sales))

# ============================================================================
# ЗАДАНИЕ 5: Форматирование цены
# ============================================================================
# Напишите функцию format_price, которая возвращает
# отформатированную строку цены с разделителями тысяч.
# Примеры:
#   format_price(1500000) -> "1 500 000 RUB"
#   format_price(2500, "USD") -> "2 500 USD"

prices_to_format = [1234567, 50000, 999]

# Ваш код здесь:
def format_price(amount, currency="RUB"):
    formatted = f"{amount:,}".replace(",", " ")
    return f"{formatted} {currency}"

for price in prices_to_format:
    print(format_price(price))

# ============================================================================
# ЗАДАНИЕ 6: Фильтрация заказов по статусу
# ============================================================================
# Напишите функцию filter_orders, которая принимает
# список заказов (словарей) и возвращает только заказы с указанным статусом.

orders = [
    {"id": 1, "client": "ООО Ромашка", "amount": 15000, "status": "paid"},
    {"id": 2, "client": "ИП Петров", "amount": 8500, "status": "pending"},
    {"id": 3, "client": "ООО Лютик", "amount": 22000, "status": "paid"},
    {"id": 4, "client": "ООО Василек", "amount": 5000, "status": "cancelled"},
    {"id": 5, "client": "ИП Сидоров", "amount": 12000, "status": "pending"},
]

# Ваш код здесь:
def filter_orders(orders, status):
    filtered = []
    for order in orders:
        if order["status"] == status:
            filtered.append(order)
    return filtered
paid_orders = filter_orders(orders, "paid")
pending_orders = filter_orders(orders, "pending")
print(paid_orders)
print(pending_orders)
# ============================================================================
# ЗАДАНИЕ 7: Расчет итога заказа с НДС
# ============================================================================
# Напишите две функции:
# 1. calc_vat — возвращает сумму НДС
# 2. calc_order_total — принимает список позиций (цена, количество),
#    считает общую сумму и добавляет НДС, используя первую функцию.
#    Возвращает словарь: {"subtotal": ..., "vat": ..., "total": ...}

order_items = [
    (1500, 2),  # цена, количество
    (890, 5),
    (3200, 1),
]

# Ваш код здесь:
VAT_RATE = 0.22

def calc_vat(amount):
    return amount * VAT_RATE
def calc_order_total(items):

    subtotal = sum(price * qty for price, qty in items)
    vat = calc_vat(subtotal)
    total = subtotal + vat

    return {
        "subtotal": subtotal,
        "vat": vat,
        "total": total
    }

result = calc_order_total(order_items)
print(result)
# ============================================================================
# ЗАДАНИЕ 8: Система расчета доставки
# ============================================================================
# Напишите три функции:
# 1. calc_distance_cost — стоимость по расстоянию
# -до 2000 км бесплатно,
#  -2000-5000 км: 1000 руб.
#  - более 5000 км: 2000 руб
# 2. calc_weight_cost — стоимость по весу:
#    - до 5 кг: 200 руб.
#    - 5-20 кг: 400 руб.
#    - более 20 кг: 400 + 30 руб. за каждый кг свыше 20
# 3. calc_delivery — итоговая стоимость
#    доставки (сумма стоимостей), для экспресс-доставки умножьте на 1.5
#
# Рассчитайте стоимость доставки для заказов:

deliveries = [
    {"distance": 50, "weight": 3, "express": False},
    {"distance": 120, "weight": 15, "express": True},
    {"distance": 30, "weight": 25, "express": False},
]
def calc_distance_cost(distance):
    if distance <= 2000:
        return 0
    elif distance <= 5000:
        return 1000
    else:
        return 2000
def calc_weight_cost(weight):
    if weight <= 5:
        return 200
    elif weight <= 20:
        return 400
    else:
        return 400 + (weight - 20) * 30
def calc_delivery(distance, weight, express=False):
    distance_cost = calc_distance_cost(distance)
    weight_cost = calc_weight_cost(weight)
    total = distance_cost + weight_cost

    if express:
        total *= 1.5

    return total

for delivery in deliveries:
    cost = calc_delivery(
        delivery["distance"],
        delivery["weight"],
        delivery["express"]
    )
    print(cost)