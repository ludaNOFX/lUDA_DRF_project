"""ЭТО ПРИМЕР КОНВЕРТЕРА ВДРУГ МНЕ НУЖГНО БУДЕТ ИМИ ВОСПОЛЬЗОВАТЬСЯ
ЕГО ИМПОРТИРУЮТ В ДАННОМ СЛУЧАЕ В store.urls"""


class FourDigitYearConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value