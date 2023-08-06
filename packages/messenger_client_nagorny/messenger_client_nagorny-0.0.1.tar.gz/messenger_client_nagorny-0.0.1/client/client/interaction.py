import sys
import json
import socket
import time
import logging
import threading
import traceback
import binascii
import hashlib
import hmac

from PyQt5.QtCore import pyqtSignal, QObject

sys.path.append('../')
from common.utils import *
from common.default_conf import *

logger = logging.getLogger('messengerapp_client')

# Объект блокировки сокета и работы с базой данных
socket_lock = threading.Lock()
database_lock = threading.Lock()


class ClientInteraction(threading.Thread, QObject):
    new_message = pyqtSignal(str)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, ip, port, client_account_name, client_database,
                 password, keys):

        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.client_account_name = client_account_name
        self.client_database = client_database
        self.sock = None
        self.password = password
        # Набор ключей для шифрования
        self.keys = keys
        self.connection_init(ip, port)

        try:
            self.get_users_list()
            self.get_contacts_list()
        except OSError as err:
            # print('Ошибка1', traceback.format_exc())
            if err.errno:
                logger.critical(f'Потеряно соединение с сервером.')
            logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            # print('Ошибка2', traceback.format_exc())
            logger.critical(f'Потеряно соединение с сервером.')
            # Флаг продолжения работы взаимодействия.
        self.running = True

    def connection_init(self, ip, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)

        # если удалось соедиться, ставим флаг True
        connected = False
        for i in range(5):
            logger.info(f'Попытка подключения {i + 1}')
            try:
                self.sock.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise Exception("Не удалось установить соединение с сервером")

        logger.debug('Установлено соединение с сервером')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        password_bytes = self.password.encode('utf-8')
        salt = self.client_account_name.lower().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512', password_bytes, salt, 10000)
        password_hash_string = binascii.hexlify(password_hash)

        logger.debug(f'password_hash готов: {password_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Отправляем сообщение о присутствии и получаем ответ, иначе исключение
        try:
            with socket_lock:
                send_message(self.sock, self.create_presence_message(pubkey))
                response = get_message(self.sock)
                logger.debug(f'Ответ сервера - {response}.')
                # Если сервер вернул ошибку, делаем исключение.
                if RESPONSE in response:
                    if response[RESPONSE] == 400:
                        raise print(response[ERROR])
                    elif response[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        response_data = response[DATA]
                        gen_hash = hmac.new(
                            password_hash_string, response_data.encode('utf-8'), 'MD5')
                        digest = gen_hash.digest()
                        answer = {
                            RESPONSE: 511,
                            DATA: binascii.b2a_base64(digest).decode('ascii')
                        }
                        send_message(self.sock, answer)
                        self.get_response(get_message(self.sock))
        except (OSError, json.JSONDecodeError):
            logger.critical('Потеряно соединение с сервером!')
            raise Exception('Потеряно соединение с сервером!')

        # Если все ок, то пишем соответствующее сообщение
        logger.info('Соединение с сервером успешно установлено.')

    # @log # пришлось убрать декоратор, т.к. dis.get_instructions не показывает использование функций
    def create_presence_message(self, pubkey):
        presence_message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name,
                PUBLIC_KEY: pubkey
            }
        }
        logger.info(
            f'Сообщение о присутствии пользователя {self.client_account_name} сформировано')
        return presence_message

    def get_response(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                logger.info(message)
                return message
            elif message[RESPONSE] == 400:
                error = message[ERROR]
                logger.error(error)
            elif message[RESPONSE] == 205:
                self.get_users_list()
                self.get_contacts_list()
                self.message_205.emit()
            else:
                logger.debug(
                    f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу, даём сигнал о
        # новом сообщении
        elif ACTION in message and FROM in message and MESSAGE_CLIENT in message \
                and message[ACTION] == MESSAGE and FROM in message and \
                TO in message and message[TO][ACCOUNT_NAME] == self.client_account_name:
            sender = message[FROM][ACCOUNT_NAME]
            text_message = message[MESSAGE_CLIENT]
            to_user = message[TO][ACCOUNT_NAME]
            logger.debug(
                f'Получено сообщение от {sender}, текст сообщения: {text_message}')
            with database_lock:
                self.client_database.save_message(
                    sender, to_user, text_message)
            self.new_message.emit(sender)

    def send_new_message(self, to_user, message):
        message_dict = self.create_message(to_user, message)
        print(message_dict)
        with socket_lock:
            send_message(self.sock, message_dict)
            logger.info(f'Отправлено сообщение для пользователя {to_user}')
            self.get_response(get_message(self.sock))

    def create_message(self, to_user, client_message):
        with database_lock:
            if not self.client_database.check_user(to_user):
                logger.error(
                    f'Попытка отправить сообщение незарегистрированому пользователю: {to_user}')
                return
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            FROM: {
                ACCOUNT_NAME: self.client_account_name
            },
            TO: {
                ACCOUNT_NAME: to_user

            },
            MESSAGE_CLIENT: client_message,
        }
        return message

    def key_request(self, username):
        """
        Метод запрашивающий с сервера публичный ключ пользователя.
        """
        logger.debug(f'Запрос публичного ключа для {username}')
        request_message = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: username
            }
        }
        with socket_lock:
            send_message(self.sock, request_message)
            response = get_message(self.sock)
        if RESPONSE in response and response[RESPONSE] == 511:
            return response[DATA]
        else:
            logger.error(f'Не удалось получить ключ собеседника {username}.')

    def get_users_list(self):
        """
        Метод запрашивающий с сервера список пользователей.
        """
        logger.debug(
            f'Запрос списка известных пользователей {self.client_account_name}')
        request_message = {
            ACTION: USERS_LIST,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name
            },
        }
        logger.debug(f'Сформирован запрос {request_message}')

        with socket_lock:
            send_message(self.sock, request_message)
            response = get_message(self.sock)
        logger.debug(f'Получен ответ {response}')
        if RESPONSE in response and 'users_list' in response:
            self.client_database.add_known_users(response['users_list'])
        else:
            logger.error('Не удалось обновить список известных пользователей.')

    def get_contacts_list(self):
        """
        Метод запрашивающий с сервера список контактов пользователя.
        """
        logger.debug(
            f'Запрос списка контактов для пользователя {self.client_account_name}')
        request = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name,
            }
        }
        logger.debug(f'Сформирован запрос {request}')
        with socket_lock:
            send_message(self.sock, request)
            response = get_message(self.sock)
        logger.debug(f'Получен ответ {response}')
        if RESPONSE in response and 'contacts_list' in response:
            for contact in response['contacts_list']:
                self.client_database.add_contact(contact)
        else:
            logger.error('Не удалось обновить список контактов.')

    # Функция добавления пользователя в контакт лист
    def add_contact(self, contact):
        """
        Метод отправляющий сообщение на сервер
         о добавлении контакта пользователю.
        """
        logger.debug(f'Создание контакта {contact}')
        request_message = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name,
            },
            CONTACT: {
                ACCOUNT_NAME: contact,
            },
        }
        # print(client_account_name, contact)
        # print(request_message)
        with socket_lock:
            send_message(self.sock, request_message)
            logger.debug(
                f'Отправлено сообщение на создание контакта {request_message}')
            response = self.get_response(get_message(self.sock))
            logger.debug(
                f'Получен ответ сервера на создание контакта {response}')
        if RESPONSE in response and response[RESPONSE] == 200:
            pass
        else:
            raise Exception('Ошибка создания контакта')
        print('Успешное создание контакта')

    # Функция удаления пользователя из списка контактов
    def remove_contact(self, contact):
        """
        Метод отправляющий сообщение на сервер
         об удалении контакта у пользователя.
        """
        logger.debug(f'Создание контакта {contact}')
        request_message = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name,
            },
            CONTACT: {
                ACCOUNT_NAME: contact,
            },
        }
        with socket_lock:
            send_message(self.sock, request_message)
            response = self.get_response(get_message(self.sock))
        if RESPONSE in response and response[RESPONSE] == 200:
            pass
        else:
            raise Exception('Ошибка удаления контакта')
        print('Успешное удаление контакта')

    def get_history(self, command):
        """
        Метод по команде запрашивающий историю сообщений
         по конкретному пользователя.
         Для работы в консоле.
        """
        with database_lock:
            if command == 'in':
                history_list = self.client_database.get_message_history(
                    to_user=self.client_account_name)
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: {message[0]} от {message[3]}:\n{message[2]}')
            elif command == 'out':
                history_list = self.client_database.get_message_history(
                    from_user=self.client_account_name)
                for message in history_list:
                    print(
                        f'\nСообщение пользователю: {message[1]} от {message[3]}:\n{message[2]}')
            elif command == 'all':
                history_list = self.client_database.get_message_history()
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: '
                        f'{message[0]}, пользователю {message[1]} от {message[3]}\n{message[2]}')

    def socket_shutdown(self):
        """
        Метод отключающий сокет в момент выхода пользователя.
        """
        self.running = False
        exit_message = {
            ACTION: 'exit',
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_account_name
            }
        }
        with socket_lock:
            try:
                send_message(self.sock, exit_message)
            except OSError:
                pass
        logger.debug('Взаимодействие завершено.')
        time.sleep(0.5)

    def run(self):
        """
        Метод содержащий основной цикл работы взаимодействия.
        """
        logger.debug('Запущена приемка сообщений с сервера.')
        while self.running:
            time.sleep(1)
            response = None
            with socket_lock:
                try:
                    self.sock.settimeout(0.5)
                    response = get_message(self.sock)
                except OSError as err:
                    if err.errno:
                        logger.critical(f'Содениенение с сервером потеряно.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                    logger.critical(f'Содениенение с сервером потеряно.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.sock.settimeout(5)

            # Если сообщение получено, то вызываем функцию обработчик:
            if response:
                logger.debug(f'Принято сообщение с сервера: {response}')
                self.get_response(response)
