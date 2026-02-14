# 1. Опишите класс "Задача". Как в ПРИОС или ЛКБ. Все поля описывать не нужно, достаточно 5-6.
# В классе с помощью методов реализуйте проверку ИНН на валидность и заполненность всех полей
class Task:
    def __init__(self, task_number: str, inn: str, executor: str,
                 deadline: str, status: str, description: str = ""):
        self.task_number = task_number
        self.inn = inn
        self.executor = executor
        self.deadline = deadline
        self.status = status
        self.description = description

    def validate_inn(self) -> bool:
        if not self.inn:
            return False
        inn = self.inn.strip()
        return inn.isdigit() and len(inn) in [10, 12]

    def check_all_fields_filled(self) -> bool:
        required_fields = [
            self.task_number,
            self.inn,
            self.executor,
            self.deadline,
            self.status
        ]
        for field in required_fields:
            if not field or not str(field).strip():
                return False
        return True
    def is_valid(self) -> bool:
        return self.check_all_fields_filled() and self.validate_inn()

    def get_validation_errors(self) -> list:
        errors = []
        if not self.task_number or not str(self.task_number).strip():
            errors.append("Номер задачи не заполнен")

        if not self.inn or not str(self.inn).strip():
            errors.append("ИНН не заполнен")
        elif not self.validate_inn():
            errors.append("ИНН имеет некорректный формат или контрольную сумму")

        if not self.executor or not str(self.executor).strip():
            errors.append("Исполнитель не указан")

        if not self.deadline or not str(self.deadline).strip():
            errors.append("Срок не указан")

        if not self.status or not str(self.status).strip():
            errors.append("Статус не указан")

        return errors
    def __str__(self):
        return f"Задача {self.task_number} - {self.status}"

task = Task(
        task_number = "3120099",
        inn = "771820482660",
        executor = "Иванов И.И.",
        deadline = "02.03.2025",
        status = "В работе",
        description = "Обращение для бухгалтера"
)
if task.is_valid():
    print(f"Задача валидна: {task}")
else:
    print("Ошибки валидации:")
    for error in task.get_validation_errors():
        print(f"- {error}")

# 2.Опишите несколько классов животных. Наследуйтесь от главного класса и опишите других животных
# Напишите метод, который будет принимать как аттрибут другое животное и придумайте как они взаимодействуют друг с другом
class Animal:
    def __init__(self, name, is_predator, energy, speed):
        self.name = name
        self.is_predator = is_predator
        self.energy = energy
        self.speed = speed

    def is_alive(self):
        return self.energy > 0
    def __str__(self):
        status = "жив" if self.is_alive() else "мёртв"
        return f"{self.name} ({self.__class__.__name__}): энергия={self.energy}, скорость={self.speed}, {status}"
class Wolf(Animal):
    def __init__(self, name):
        Animal.__init__(self, name, is_predator=True, energy=80, speed=50)
    def attack(self, other):
        if not self.is_alive():
            print(f"{self.name} слишком слаб для атаки")
            return
        print(f"{self.name} атакует {other.name}!")
        if not other.is_predator:
            damage = 35
            print(f"   Успешная охота на добычу!")
        else:
            damage = 20
            print(f"   Схватка с хищником!")
        self.energy -= 15
        other.energy -= damage

        # Нормализуем энергию
        if self.energy < 0:
            self.energy = 0
        if other.energy < 0:
            other.energy = 0

        if not other.is_alive():
            print(f" {other.name} погиб...")
class Rabbit(Animal):
    def __init__(self, name):
        super().__init__(name, is_predator=False, energy=60, speed=85)
        self.fear_level = 0
    def flee(self, predator):
        if not self.is_alive():
            print(f"{self.name} не может убежать")
            return False
        print(f" {self.name} пытается убежать от {predator.name}!")
        self.energy -= 20
        self.fear_level += 1
        if self.speed > predator.speed:
            print(f"{self.name} успешно скрылся!")
            return True
        else:
            print(f"{self.name} не успел убежать...")
            return False

wolf = Wolf("Петя")
rabbit = Rabbit("Вася")

print("Начало")
for animal in [wolf, rabbit]:
    print(f"  {animal}")

print("\nСхватка")
if rabbit.is_alive():
    escaped = rabbit.flee(wolf)
    if not escaped:
        wolf.attack(rabbit)

print("\nКонец")
for animal in [wolf, rabbit]:
    print(f"  {animal}")

# 3. Напишите класс "Калькулятор". С помощью методов реализуйте сложение и извлечение корня из числа.

import math
class Calculator:
    def sum(self, a, b):
        return a + b
    def sqrt(self, number):
        if number < 0:
            raise ValueError("Нельзя извлечь корень из отрицательного числа")
        result = math.sqrt(number)
        return int(result)

calc = Calculator()
print(f"7 + 3 = {calc.sum(7, 3)}")
print(f"√25 = {calc.sqrt(25)}")


#4. Напишите класс для запросов по API. Используйте библиотеку requests. Напишите 2 метода:
# С помощью API запроса получите токен из кейклок. Подсмотрите как у нас в ЛКБ и ПРИОС реализована авторизация.
# Сохраните этот токен как аттрибут и используйте его для получения любого листинга

import requests
token_url = 'https://lkb-temp-kub.smbconnect.ru/auth/realms/bk-dev/protocol/openid-connect/token'
token_data = {
    'client_id': 'bc',
    'grant_type': 'password',
    'client_secret': 'hVmB4SG1k5DfKNZoSn6KswvOuKPdaPRv',
    'scope': 'openid',
    'username': 'admin@test.ru',
    'password': 'test'
}
response = requests.post(token_url, data=token_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    token = response.json()['access_token']
    api_url = 'https://lkb-temp-kub.smbconnect.ru/api/mdm/documents/v1/d/client'
    headers = {
        'authorization': token,
        'accept': 'application/json, text/plain, */*'
    }
    params = {
        'page_size': 10,
        'page': 1
    }
    response = requests.get(api_url, headers=headers, params=params)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        clients = response.json()
        print("Данные получены успешно!\n")
    else:
        print(f"Ошибка получения данных: {response.status_code}")
        print(f"Ответ: {response.text}")
else:
    print(f"Ошибка получения токена: {response.status_code}")
    print(f"Ответ: {response.text}")