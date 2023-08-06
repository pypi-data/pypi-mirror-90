
import sys
import logging
# import logs.log_configs.client_log_config
# import logs.log_configs.server_log_config
import inspect
import socket

if sys.argv[0].find('client.py') >= 0:
    logger = logging.getLogger('messengerapp_client')
elif sys.argv[0].find('server.py') >= 0:
    logger = logging.getLogger('messengerapp_server')


# В виде функции
def log(function):

    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        logger.debug(
            f'Функция {function.__name__}, аргументы - {args}, {kwargs}, результат - {result} | '
            f'Вызов из функции "{inspect.currentframe().f_back.f_code.co_name}"', stacklevel=2)
        return result

    return wrapper


# В виде класса
# class Log:
#     """
#     Основной класс для серверной базы данных.
#     """
#
#     def __call__(self, function):
#         def wrapper(*args, **kwargs):
#             result = function(*args, **kwargs)
#             logger.debug(f'Функция {function.__name__}, аргументы - {args}, {kwargs}, результат - {result} | '
#                          f'Вызов из функции "{inspect.currentframe().f_back.f_code.co_name}"', stacklevel=2)
#             return result
#         return wrapper


def login_required(function):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.server_core import Server
        from common.default_conf import ACTION, PRESENCE
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].account_names_list:
                        if args[0].account_names_list[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presence, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return function(*args, **kwargs)

    return checker
