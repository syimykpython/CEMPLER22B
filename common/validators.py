from datetime import date
from rest_framework.exceptions import ValidationError

def validate_age_for_product(request):
    """
    Проверка возраста пользователя для создания продукта.
    Берёт birthdate из токена.
    """
    if not request or not request.auth:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    birthdate_str = request.auth.get("birthdate")
    if not birthdate_str:
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    # Преобразуем строку в дату
    try:
        birthdate = date.fromisoformat(birthdate_str)
    except ValueError:
        raise ValidationError("Неверный формат даты рождения в токене.")

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")