import os
import select
import socket
import sys
import threading
import hmac
import binascii
import traceback

# import logs.log_configs.server_log_config
import logging

from homework.hw08.server_rls.common.decorators import log
from homework.hw08.server_rls.common.decorators import login_required
from homework.hw08.server_rls.common.default_conf import *
from homework.hw08.server_rls.common.utils import get_message, send_message

logger = logging.getLogger('messengerapp_server')


# дескриптор на проверку порта
class CheckPort:
    """
    Класс дескриптор для проверки порта.
    """

    def __set__(self, instance, value):
        try:
            if not 1024 < value < 65536:
                raise ValueError
        except ValueError:
            logger.critical(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)
        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner_class, my_attr):
        self.my_attr = my_attr


# Флаг о том, что был подключён новый пользователь нужен для того, чтобы не мучать базу данных
# постоянными запросами на обновление
new_connection = False
connection_lock = threading.Lock()


class Server(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    port = CheckPort()

    def __init__(self, listen_address, listen_port, server_database):
        self.address = listen_address
        self.port = listen_port
        self.clients_list = []
        self.list_of_messages = []
        self.account_names_list = {}
        self.server_database = server_database

        self.sock = None

        # Сокеты
        self.listen_sockets = None
        self.error_sockets = None

        # Флаг продолжения работы
        self.running = True
        super().__init__()

    def socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.settimeout(0.5)
        self.sock.listen(MAX_CONNECTIONS)

    def run(self):
        self.socket()

        while self.running:
            try:
                client, client_address = self.sock.accept()
            except socket.error:
                pass
            else:
                logger.info(
                    f'Установлено соедение с клиентом {client_address}')
                self.clients_list.append(client)

            get_message_list = []
            send_message_list = []
            # self.errors_list = []

            try:
                if self.clients_list:
                    get_message_list, send_message_list, errors_list = select.select(
                        self.clients_list, self.clients_list, [], 0)
            except OSError:
                pass

            # прием сообщений, если ошибка, отсоединяем пользователя
            if get_message_list:
                # info = 'good client' # ЗАГЛУШКА ДЛЯ ТЕСТА ПЕРЕДАЧИ ДОП
                # ПАРАМЕТРА В БАЗУ
                for client_with_message in get_message_list:
                    try:
                        self.process_client_message(
                            get_message(client_with_message), client_with_message)
                    except Exception as ex:
                        print(f'Error: {traceback.format_exc()}')
                        logger.info(
                            f'Потеряно соединение с клиентом {client_with_message.getpeername()}.')
                        self.remove_client(client_with_message)

            for msg in self.list_of_messages:
                try:
                    self.prc_message(
                        msg, self.account_names_list, send_message_list)
                except Exception:
                    logger.info(
                        f'Потеряно соединение с клиентом {msg[TO][ACCOUNT_NAME]}.')
                    self.remove_client(
                        self.account_names_list[msg[TO][ACCOUNT_NAME]])
            self.list_of_messages.clear()

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        """
        # logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.account_names_list:
            if self.account_names_list[name] == client:
                self.server_database.user_logout(name)
                del self.account_names_list[name]
                break
        self.clients_list.remove(client)
        client.close()

    @log
    def prc_message(self, msg, account_names_list, send_message_list):
        """
        Метод обработчик сообщения, которое необходимо отправить
        другому пользователю. Обрабатывает и отправляет сообщение.
        """
        if msg[FROM][ACCOUNT_NAME] in account_names_list and \
                account_names_list[msg[TO][ACCOUNT_NAME]] in send_message_list:
            send_message(account_names_list[msg[TO][ACCOUNT_NAME]], msg)

            logger.info(
                f'Cообщение отправлено пользователю {msg[TO][ACCOUNT_NAME]} '
                f'от пользователя {msg[FROM][ACCOUNT_NAME]}.')
        elif msg[TO][ACCOUNT_NAME] in account_names_list and \
                account_names_list[msg[TO][ACCOUNT_NAME]] not in send_message_list:
            raise ConnectionError
        else:
            logger.error(
                f'Пользователь {msg[TO][ACCOUNT_NAME]} не существует, отправка сообщения невозможна.')

    @login_required
    @log
    def process_client_message(self, message, client_with_message):
        """
        Метод обработчик сообщения, которое приходит от клиента через сервер.
        Принимает, обрабатывает в зависимости от типа собщения.
        Если нужно, то отправляет ответ или закрывает соединение.
        Если полученное сообщение не валидно, отдает ошибку и отключает клиента.
        При сообщении о присутствии вызывает метод авторизации.
        """
        global new_connection
        logger.debug(f'Разбор сообщения от клиента {client_with_message}')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message:
            self.authorize_user(message, client_with_message)
            # if message[USER][ACCOUNT_NAME] not in self.account_names_list.keys():
            #     self.account_names_list[message[USER][ACCOUNT_NAME]] = client_with_message
            #     client_ip_address, client_port = client_with_message.getpeername()
            #     # info = message[USER][INFO]
            #     # print(client_ip_address, client_port, info)
            #     self.server_database.user_login(message[USER][ACCOUNT_NAME], client_ip_address, client_port)
            #     answer = send_message(client_with_message, {RESPONSE: 200})
            #     logger.info(answer)
            #     with connection_lock:
            #         new_connection = True
            # else:
            #     response = {RESPONSE: 400, ERROR: 'Пользователь с таким именем уже существует.'}
            #     send_message(client_with_message, response)
            #     self.clients_list.remove(client_with_message)
            #     client_with_message.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_CLIENT in message and \
                FROM in message and TO in message:
            if message[TO][ACCOUNT_NAME] in self.account_names_list:
                self.list_of_messages.append(message)
                self.server_database.message_count_history(
                    message[FROM][ACCOUNT_NAME], message[TO][ACCOUNT_NAME])
                send_message(client_with_message, {RESPONSE: '200'})
            else:
                response = {
                    RESPONSE: '400',
                    ERROR: 'Пользователь не зарегистрирован на сервере.'}
                send_message(client_with_message, response)
            return

        elif ACTION in message and message[ACTION] == GET_CONTACTS and \
                TIME in message and USER in message and \
                self.account_names_list[message[USER][ACCOUNT_NAME]] == client_with_message:
            response = {
                RESPONSE: 202,
                'contacts_list': self.server_database.contacts_list(
                    message[USER][ACCOUNT_NAME])}
            try:
                send_message(client_with_message, response)
            except OSError:
                self.remove_client(client_with_message)

        elif ACTION in message and message[ACTION] == ADD_CONTACT and \
                TIME in message and USER in message and CONTACT in message and \
                self.account_names_list[message[USER][ACCOUNT_NAME]] == client_with_message:
            self.server_database.add_contact(
                message[USER][ACCOUNT_NAME],
                message[CONTACT][ACCOUNT_NAME])
            response = {RESPONSE: 200}
            try:
                send_message(client_with_message, response)
            except OSError:
                self.remove_client(client_with_message)

        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and \
                TIME in message and USER in message and CONTACT in message and \
                self.account_names_list[message[USER][ACCOUNT_NAME]] == client_with_message:
            self.server_database.remove_contact(
                message[USER][ACCOUNT_NAME],
                message[CONTACT][ACCOUNT_NAME])
            response = {RESPONSE: 200}
            try:
                send_message(client_with_message, response)
            except OSError:
                self.remove_client(client_with_message)

        elif ACTION in message and message[ACTION] == USERS_LIST and USER in message \
                and self.account_names_list[message[USER][ACCOUNT_NAME]] == client_with_message:
            response = {
                RESPONSE: 202, 'users_list': [
                    user[0] for user in self.server_database.select_users()]}
            try:
                send_message(client_with_message, response)
            except OSError:
                self.remove_client(client_with_message)

        elif ACTION in message and message[ACTION] == 'exit' and ACCOUNT_NAME in message:
            self.clients_list.remove(
                self.account_names_list[message[ACCOUNT_NAME]])
            self.server_database.user_logout(message[ACCOUNT_NAME])
            # self.clients_list[message[ACCOUNT_NAME]].close()
            # del self.clients_list[message[ACCOUNT_NAME]]
            with connection_lock:
                new_connection = True
            return

        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and USER in message:
            response = {
                RESPONSE: 511,
                DATA: self.server_database.get_pubkey(
                    message[USER][ACCOUNT_NAME])}
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда отправялем 400)
            if response[DATA]:
                try:
                    send_message(client_with_message, response)
                except OSError:
                    self.remove_client(client_with_message)
            else:
                response = {
                    RESPONSE: 400,
                    ERROR: 'Нет публичного ключа для данного пользователя.'
                }
                try:
                    send_message(client_with_message, response)
                except OSError:
                    self.remove_client(client_with_message)

        else:
            error = send_message(client_with_message, {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            })
            logger.info(error)
            return error

    def authorize_user(self, message, sock):
        """Метод реализующий авторизцию пользователей."""
        # Если имя пользователя уже занято то возвращаем 400
        logger.debug(f'Запуск процесса авторизации {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.account_names_list.keys():
            response = {
                RESPONSE: 400,
                ERROR: 'Имя пользователя уже занято.'
            }
            try:
                logger.debug(f'Username занят, отправка ответа {response}')
                send_message(sock, response)
            except OSError:
                logger.debug('OS Error')
                pass
            self.clients_list.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере
        elif not self.server_database.check_user(message[USER][ACCOUNT_NAME]):
            response = {
                RESPONSE: 400,
                ERROR: 'Пользователь не зарегистрирован.'
            }
            try:
                logger.debug(
                    f'Неизвестный пользователь, отправка ответа {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients_list.remove(sock)
            sock.close()
        else:
            logger.debug('Username корректный, проверка пароля')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = {
                RESPONSE: 511,
                DATA: None
            }
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # необходимо декодировать
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            auth_hash = hmac.new(
                self.server_database.get_password_hash(
                    message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = auth_hash.digest()
            logger.debug(f'Сообщение авторизации = {message_auth}')
            try:
                # Обмен с клиентом
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                logger.debug('Ошибка авторизации:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.account_names_list[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                response = {
                    RESPONSE: 200
                }
                try:
                    send_message(sock, response)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.server_database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:

                response = {
                    RESPONSE: 400,
                    ERROR: 'Неверный пароль.'
                }
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients_list.remove(sock)
                sock.close()

    def service_update_lists(self):
        """Метод реализующий отправки сервисного сообщения 205 клиентам."""
        for client in self.account_names_list:
            response = {
                RESPONSE: 205
            }
            try:
                send_message(self.account_names_list[client], response)
            except OSError:
                self.remove_client(self.account_names_list[client])
