from dataclasses import dataclass, field
from typing import List
@dataclass
class Dragon:
    name: str = "Терракс"
    legs: int = 8
    long_claw: bool = True
    predator: bool = True
    can_bite: bool = True
    age: int = 22
    friends: List[str] = field(default_factory=list)
    color: str = "чернее ночи"
dragon = Dragon()
dragon.friends.append("Урракс")
dragon.friends.append("Мераксес")
print(f"Я, {dragon.name}, мне {dragon.age} года, я {dragon.color}, у меня {dragon.legs} лап.\n"
    f"У меня есть верные друзья {', '.join(dragon.friends)}")


inn = "12223323323"
if len(inn) == 10:
    print("ООО")
elif len(inn) == 12:
    print("ИП")
else:
    print("Непонятно")

    company_name = "ООО 'Среда'"
    company_industry = "IT",
    company_founded = 2021,
    company_employees_count = 350,
    has_offices = True,
    company_offices = ["Москва", "Берлин", "Тбилиси"]



    text = "  hello world  "
    text.strip()   # "hello world"
    "---hi---".strip("-")  # "hi"

card_number = "1234567890123456"
card_number [12:]