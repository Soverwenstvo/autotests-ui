"""
Домашние задания на работу со стандартной библиотекой Python
Бизнес-ориентированные задачи
"""

# ============================================================================
# ЗАДАНИЕ 1: Парсинг дат из логов (datetime)
# ============================================================================
# Напишите функцию parse_log_dates, которая принимает список строк с датами
# в разных форматах и возвращает список объектов datetime.
# Используйте модуль datetime и метод strptime.
#
# Функция должна распознавать форматы:
# - "2024-01-15" (ISO формат)
# - "15.01.2024" (российский формат)
# - "01/15/2024" (американский формат)
#
# Дополнительно: напишите функцию days_until_deadline, которая принимает
# дату дедлайна в любом из форматов выше и возвращает количество дней до неё.

log_dates = [
    "2024-03-15",
    "20.03.2024",
    "03/25/2024",
    "2024-04-01",
    "05.04.2024",
]

# Ваш код здесь:

import arrow
def parse_log_dates(date_strings):
    return [arrow.get(d, ["YYYY-MM-DD", "DD.MM.YYYY", "MM/DD/YYYY"]).datetime
            for d in date_strings]


def days_until_deadline(deadline_str):
    deadline = arrow.get(deadline_str).date()
    return (deadline - arrow.now().date()).days

# ============================================================================
# ЗАДАНИЕ 2: Обработка данных из API (json)
# ============================================================================
# Вам пришёл ответ от API в виде JSON-строки. Напишите функцию
# process_api_response, которая:
# 1. Парсит JSON
# 2. Извлекает список пользователей
# 3. Возвращает словарь {email: full_name} только для активных пользователей

api_response = '''
{
    "status": "success",
    "data": {
        "users": [
            {"id": 1, "email": "ivan@company.ru", "name": "Иван", "surname": "Петров", "active": true},
            {"id": 2, "email": "anna@company.ru", "name": "Анна", "surname": "Сидорова", "active": true},
            {"id": 3, "email": "petr@company.ru", "name": "Пётр", "surname": "Иванов", "active": false},
            {"id": 4, "email": "maria@company.ru", "name": "Мария", "surname": "Козлова", "active": true}
        ],
        "total": 4
    }
}
'''

# Ваш код здесь:

import json

def process_api_response(api_response):
    data = json.loads(api_response)
    users = data["data"]["users"]

    return {
        user["email"]: f'{user["name"]} {user["surname"]}'
        for user in users
        if user["active"]
    }
# ============================================================================
# ЗАДАНИЕ 3: Анализ продаж (collections)
# ============================================================================
# Используя модуль collections, проанализируйте данные о продажах:
#
# 1. Используя Counter, найдите:
#    - Топ-3 самых продаваемых товара
#    - Сколько раз каждый менеджер совершил продажу
#
# 2. Используя defaultdict, сгруппируйте продажи по менеджерам
#    (словарь, где ключ — имя менеджера, значение — список его продаж)
#
# 3. Используя namedtuple, создайте структуру Sale(id, product, manager, amount)
#    и преобразуйте данные в список таких структур

sales_log = [
    {"id": 1, "product": "Ноутбук", "manager": "Иван", "amount": 75000},
    {"id": 2, "product": "Телефон", "manager": "Анна", "amount": 45000},
    {"id": 3, "product": "Ноутбук", "manager": "Анна", "amount": 72000},
    {"id": 4, "product": "Планшет", "manager": "Иван", "amount": 35000},
    {"id": 5, "product": "Телефон", "manager": "Пётр", "amount": 48000},
    {"id": 6, "product": "Ноутбук", "manager": "Иван", "amount": 80000},
    {"id": 7, "product": "Наушники", "manager": "Анна", "amount": 12000},
    {"id": 8, "product": "Телефон", "manager": "Иван", "amount": 52000},
    {"id": 9, "product": "Планшет", "manager": "Пётр", "amount": 33000},
    {"id": 10, "product": "Телефон", "manager": "Анна", "amount": 47000},
]

# Ваш код здесь:
from collections import Counter, defaultdict, namedtuple
product_counter = Counter()
manager_counter = Counter()

for sale in sales_log:
    product_counter[sale["product"]] += 1
    manager_counter[sale["manager"]] += 1

top_products = product_counter.most_common(3)
manager_sales_count = dict(manager_counter)
sales_by_manager = defaultdict(list)

for sale in sales_log:
    sales_by_manager[sale["manager"]].append(sale)
    Sale = namedtuple("Sale", ["id", "product", "manager", "amount"])

    sales_structured = [
        Sale(
            sale["id"],
            sale["product"],
            sale["manager"],
            sale["amount"]
        )
        for sale in sales_log
    ]

# ============================================================================
# ЗАДАНИЕ 4: Генератор отчётов (random + string)
# ============================================================================
# Вам нужно создать систему генерации тестовых данных для отчётов.
# Напишите функции:
#
# 1. generate_order_id() — генерирует уникальный ID заказа
#    в формате "ORD-XXXXXX" (6 случайных букв и цифр)
#
# 2. generate_test_orders(n) — генерирует n тестовых заказов со случайными:
#    - id (используя функцию выше)
#    - client (случайный выбор из списка clients)
#    - amount (случайная сумма от 5000 до 100000, округлённая до 100)
#    - status (случайный выбор: "new", "processing", "shipped", "delivered")
#
# 3. Установите random.seed(42) перед генерацией для воспроизводимости
#    и сгенерируйте 10 тестовых заказов

clients = [
    "ООО Ромашка",
    "ИП Петров",
    "АО Технологии",
    "ООО Строй-Мастер",
    "ИП Сидорова",
]

# Ваш код здесь:
import random
import string

def generate_order_id():
    symbols = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(symbols, k=6))
    return f"ORD-{random_part}"

def generate_test_orders(n):
    orders = []
    statuses = ["new", "processing", "shipped", "delivered"]

    for _ in range(n):
        order = {
            "id": generate_order_id(),
            "client": random.choice(clients),
            "amount": random.randrange(5000, 100001, 100),
            "status": random.choice(statuses)
        }
        orders.append(order)

    return orders
random.seed(42)

test_orders = generate_test_orders(10)

for order in test_orders:
    print(order)