import os
from hashlib import sha256
from binascii import hexlify, unhexlify

PATH = "db/users_information.csv"


def load_database():
    if os.path.exists(PATH):
        with open(PATH, "r") as file:
            for i in file:
                yield i.strip().split(",")


def register_user(user_information):
    with open(PATH, mode="a") as file:
        name_user = user_information[0]
        password, salt = encript(user_information[1])
        save = (name_user + "," + password + "," +
                salt + "\n")
        file.write(save)


def get_user_information(name_user):
    """
    Retorna la informacion del usuario en caso de existir, de lo contrario
    retorna False
    :param name_user:
    :return:
    """
    exist = False
    for i in filter(lambda x: x[0] == name_user, load_database()):
        exist = i
    return exist


def encript(password: str, salt_=None):
    coder = sha256()
    if salt_ is None:
        salt = os.urandom(8)
    else:
        salt = salt_
    password_encode = str.encode(password)
    coder.update(salt + password_encode)
    return coder.hexdigest(), hexlify(salt).decode()


def check_input_password(input_password, correct_password, salt):
    return encript(input_password, salt)[0] == correct_password


def check_correct_log_in(name_user, password):
    user_data = get_user_information(name_user)
    if user_data:
        correct_password = user_data[1]
        salt = unhexlify(user_data[2].encode().strip())
        return check_input_password(password, correct_password, salt)
    return False


def check_correct_sign_in(name_user, password):
    if not get_user_information(name_user):  # El usuario no existe
        register_user((name_user, password))  # Se registra
        return True  # Se ha regitrado correctamente
    return False  # Hubo un error al registrarse
