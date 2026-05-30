"""Валидация входных данных"""


def validate_positive_float(value, name):
    try:
        v = float(value)
        if v <= 0:
            return f"{name} должно быть > 0"
        return None
    except (ValueError, TypeError):
        return f"{name} должно быть числом"


def validate_non_negative_float(value, name):
    try:
        v = float(value)
        if v < 0:
            return f"{name} должно быть ≥ 0"
        return None
    except (ValueError, TypeError):
        return f"{name} должно быть числом"


def validate_positive_int(value, name, min_val=1):
    try:
        v = int(value)
        if v < min_val:
            return f"{name} должно быть ≥ {min_val}"
        return None
    except (ValueError, TypeError):
        return f"{name} должно быть целым числом"
