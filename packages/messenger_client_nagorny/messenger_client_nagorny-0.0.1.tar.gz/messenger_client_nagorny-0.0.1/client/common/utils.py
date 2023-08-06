import json
from common.default_conf import MAX_PACKAGE_LENGTH, ENCODING


def get_message(sock_get):
    """
    Функция приёма сообщений от удалённых компьютеров.
    Принимает сообщения JSON, декодирует полученное сообщение
    и проверяет что получен словарь.
    :param sock_get: сокет для передачи данных.
    :return: словарь - сообщение.
    """
    # получаем закодированный ответ
    encoded_response = sock_get.recv(MAX_PACKAGE_LENGTH)

    # делаем валидацию на то, что нам пришли действительно байты, которые нужно раскодировать и десериализовать,
    # либо на то, что пришел словарь python, который сразу же вернем
    # в данном случае подойдет и type()
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    """
    Функция отправки словарей через сокет.
    Кодирует словарь в формат JSON и отправляет через сокет.
    :param sock: сокет для передачи
    :param message: словарь для передачи
    :return: ничего не возвращает
    """
    # сериализуем в json, кодируем, отправляем
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
