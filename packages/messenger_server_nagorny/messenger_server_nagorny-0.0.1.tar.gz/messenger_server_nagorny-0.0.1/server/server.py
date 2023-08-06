import configparser
import os
import select
import socket
import sys
import json
import threading
import time
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from server.server_ui_old import MainWindow, HistoryWindow, ConfigWindow, create_users_model, create_history_model
import logs.log_configs.server_log_config
import logging
from common.decorators import log

from common.default_conf import *
from common.utils import get_message, send_message

from common.metaclasses import ServerVerifier

from server.server_db import ServerStorage
from server.server_core import Server
from server.main_window import MainWindow

logger = logging.getLogger('messengerapp_server')


@log
def load_params(default_port, default_address):
    """
    Метод загрузки параметров.
    Валидация и загрузка адреса и порта.
    """
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = default_port
    except IndexError:
        logger.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)

    # валидация и загрузка адреса
    try:
        if '-address' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-address') + 1]
        else:
            listen_address = default_address
    except IndexError:
        logger.error(
            'После параметра -\'address\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    try:
        if '--no_gui' in sys.argv:
            gui_flag = True
        else:
            gui_flag = False
    except Exception as ex:
        logger.error(f'{ex}')
        sys.exit(1)

    return listen_address, listen_port, gui_flag


def make_sock_get_msg_send_answer():
    config = configparser.ConfigParser()

    dir_path = os.getcwd()
    config.read(f"{dir_path}/server/{'server_config.ini'}")

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = load_params(
        int(config['SETTINGS']['default_port']), config['SETTINGS']['listen_address'])

    # Инициализация базы данных
    server_database = ServerStorage(
        os.path.join(
            config['SETTINGS']['database_path'],
            config['SETTINGS']['database_file']))

    # -p 8081 -address 192.168.1.109 (при проверке: работает как через терминал, так и через PyCharm)
    # listen_address, listen_port = load_params()
    # server_database = ServerStorage()

    server = Server(listen_address, listen_port, server_database)
    server.daemon = True
    server.start()

    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(server_database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    make_sock_get_msg_send_answer()
