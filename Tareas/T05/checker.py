from webservices import get_categories
import re


def check_category(category):
    categories = get_categories()
    if category in categories:
        return categories[category]
    return None


def check_categories(categories):
    final = ""
    for i in re.split(",", categories):
        checked = check_category(i)
        if checked is not None:
            final += checked + ","
    if categories != "" and final == "":
        return None
    return final[:-1]


def check_number(number):
    """
    Devuelve un numeo entero si posible, None en otro caso
    """
    if bool(re.match("[0-9]+$", number)):
        return int(number)
    return None
