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
        """Проверка ИНН на валидность"""
        if not self.inn:
            return False
        inn = self.inn.strip()
        # Проверяем, что ИНН состоит только из цифр и имеет длину 10 или 12
        return inn.isdigit() and len(inn) in [10, 12]

    def check_all_fields_filled(self) -> bool:
        """Проверка заполненности всех обязательных полей"""
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
        """Комплексная проверка валидности задачи"""
        return self.check_all_fields_filled() and self.validate_inn()

    def get_validation_errors(self) -> list:
        """Возвращает список ошибок валидации"""
        errors = []
        if not self.check_all_fields_filled():
            errors.append("Не все обязательные поля заполнены")
        if not self.validate_inn():
            errors.append("ИНН невалиден или не заполнен")
        return errors

    def __str__(self):
        return f"Задача {self.task_number} - {self.status}"


if __name__ == "__main__":
    # Создаем задачу с данными из скриншота
    task1 = Task(
        task_number="316",
        inn="236501381240",
        executor="Первый Контакт Центр",
        deadline="11.02.2026",
        status="Назначена",
        description="0f8e7423-2eae-45d5-abf7-f5e393859795 - 316"
    )

    print(task1)
    print(f"Все поля заполнены: {task1.check_all_fields_filled()}")
    print(f"ИНН валиден: {task1.validate_inn()}")
    print(f"Задача валидна: {task1.is_valid()}")