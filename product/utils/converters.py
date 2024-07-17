"""ЭТО ПРИМЕР КОНВЕРТЕРА ВДРУГ МНЕ НУЖГНО БУДЕТ ИМИ ВОСПОЛЬЗОВАТЬСЯ
ЕГО ИМПОРТИРУЮТ В ДАННОМ СЛУЧАЕ В store.urls"""
from typing import Any


class FourDigitYearConverter:
    regex = "[0-9]{4}"

    @staticmethod
    def to_python(value: Any) -> int:
        return int(value)

    @staticmethod
    def to_url(value: Any) -> str:
        return "%04d" % value
