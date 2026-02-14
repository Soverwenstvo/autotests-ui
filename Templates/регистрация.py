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
from datetime import date
import dateutil.parser

def parse_log_dates(dates_list):
    parsed_dates = []

    for date_str in dates_list:
        try:
            dt = dateutil.parser.parse(date_str, dayfirst=False)
            parsed_dates.append(dt)
        except (ValueError, dateutil.parser.ParserError) as e:
            print(f"Ошибка парсинга '{date_str}': {e}")

    return parsed_dates


def days_until_deadline_dateparser(deadline_str):
    try:
        deadline = dateutil.parser.parse(deadline_str, dayfirst=False).date()
        today = date.today()
        return (deadline - today).days
    except (ValueError, dateutil.parser.ParserError) as e:
        raise ValueError(f"Не удалось распознать дату: {e}")


log_dates = ["2024-01-15", "15/02/2024", "March 20, 2024"]

parsed_dateutil = parse_log_dates(log_dates)
for original, parsed in zip(log_dates, parsed_dateutil):
    print(f"{original:15} -> {parsed.strftime('%Y-%m-%d')}")

print("\n=== Дни до дедлайна (dateutil) ===")
deadline = "31.12.2024"
days = days_until_deadline_dateparser(deadline)
print(f"До {deadline}: {days} дней")
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
from typing import Dict


def process_api_response_json(api_response: str) -> Dict[str, str]:
    data = json.loads(api_response)
    users = data.get('data', {}).get('users', [])
    active_users = {
        user['email']: f"{user['name']} {user['surname']}"
        for user in users
        if user.get('active', False)
    }
    return active_users


print()
result_json = process_api_response_json(api_response)
for email, name in result_json.items():
    print(f"{email:25} -> {name}")
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
from typing import List, Dict

Sale = namedtuple('Sale', ['id', 'product', 'manager', 'amount'])


def analyze_sales_collections(sales_data: List[Dict]) -> None:
    # Преобразуем данные в список namedtuple
    sales = [Sale(**sale) for sale in sales_data]

    print("=== 1. АНАЛИЗ С COLLECTIONS ===\n")

    product_counter = Counter(sale.product for sale in sales)
    print("Топ-3 самых продаваемых товара:")
    for product, count in product_counter.most_common(3):
        print(f"  {product}: {count} продаж")

    manager_counter = Counter(sale.manager for sale in sales)
    print("\nКоличество продаж по менеджерам:")
    for manager, count in manager_counter.most_common():
        print(f"  {manager}: {count} продаж")

    sales_by_manager = defaultdict(list)
    for sale in sales:
        sales_by_manager[sale.manager].append(sale)

    print("\nПродажи по менеджерам (с деталями):")
    for manager, manager_sales in sales_by_manager.items():
        total = sum(s.amount for s in manager_sales)
        print(f"\n  {manager} (всего: {total:,} руб.):")
        for sale in manager_sales:
            print(f"    - {sale.product}: {sale.amount:,} руб.")

    print("\n\nВсе продажи (namedtuple):")
    for sale in sales[:3]:
        print(f"  {sale}")
    print("  ...")

    return sales


if __name__ == "__main__":
    sales_objects = analyze_sales_collections(sales_log)

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


def generate_order_id() -> str:
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=6))
    return f"ORD-{random_part}"


def generate_test_orders(n: int) -> List[Dict]:
    orders = []

    for i in range(n):
        order = {
            'id': generate_order_id(),
            'client': random.choice(clients),
            'amount': round(random.randint(50, 1000) * 100, -2),
            'status': random.choice(status)
        }
        orders.append(order)

    return orders


def demo_basic_generation():
    print("=== 1. БАЗОВАЯ ГЕНЕРАЦИЯ (random + string) ===\n")

    random.seed(42)

    orders = generate_test_orders(10)

    print("Сгенерировано 10 тестовых заказов:\n")
    for i, order in enumerate(orders, 1):
        print(f"{i:2d}. {order['id']} | {order['client']:20} | "
              f"{order['amount']:>7,} руб. | {order['status']}")

    total = sum(o['amount'] for o in orders)
    avg = total // len(orders)
    print(f"\nОбщая сумма: {total:,} руб.")
    print(f"Средний чек: {avg:,} руб.")

    return orders


def main():
    orders_basic = demo_basic_generation()
    if __name__ == "__main__":
        main()
