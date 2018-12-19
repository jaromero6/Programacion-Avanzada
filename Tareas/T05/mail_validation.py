import re


def validate_mail(user_mail):
    """
    Retorna True si el correo ingresado es correcto, False en otro caso
    :return:
    """
    is_only_one_point = 1 == len(re.split("[.]", user_mail)) - 1
    pattern = "(^\w{3,8}@[A-Za-z0-9_.]{4,12})"
    return bool(re.fullmatch(pattern, user_mail)) and is_only_one_point


def validate_password(user_password):
    """
    Retorna True si la contraseña ingresada es valida, False en otro caso
    :return:
    """
    upper_letter = len(re.split("[A-Z]", user_password)) > 1
    pattern = "(^[A-Za-z0-9]{8,12}$)"
    return bool(re.fullmatch(pattern, user_password)) and upper_letter


def validate_user_settings(user_mail, user_password):
    return validate_mail(user_mail) and validate_password(user_password)
