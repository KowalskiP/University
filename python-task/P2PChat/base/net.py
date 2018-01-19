__author__ = 'kowalski'
import socket

import config
import base.text
import base.handler


def format_number(number):
    """Перевод числа в строки и проверка на длину. Если меньше 4 -
    добавление 0-й впереди"""
    temp = str(number)
    while len(temp) < 4:
        temp = '0' + temp
    return temp


def net_throw(conn, message):
    """Отправка сообщения черер открытый сокет. Отправляет сначала длину
    сообщения, а потом само сообщение"""
    try:
        # print("throw: "+format_number(2*len(message)))
        # print("throw: "+message)
        conn.send(format_number(2*len(message)).encode(encoding='UTF-8'))
        conn.send(message.encode(encoding='UTF-8'))
    except socket.error:
        if len(config.send_array) != 0:
            base.text.write_to_screen(
                "Проблемы с соединением. Отправка сообщения не удалась.",
                "System")
            base.handler.event_handler("-001")


def net_catch(conn):
    """Получения сообщения через открытый сокет. Если длина начинается на
    '-' - вызывается обработка сообщения и возвращает 1"""
    try:
        data = conn.recv(4)
        # print("catch: "+data.decode(encoding='UTF-8'))
        if data.decode(encoding='UTF-8')[0] == '-':
            base.handler.event_handler(data.decode(encoding='UTF-8'), conn)
            return 1
        data = conn.recv(int(data.decode(encoding='UTF-8')))
        # print("catch: "+data.decode(encoding='UTF-8'))
        return data.decode(encoding='UTF-8')
    except socket.error:
        if len(config.get_array) != 0:
            base.text.write_to_screen(
                "Проблемы с соединением. Получить сообщение не удалось.",
                "System")
        base.handler.event_handler("-001")
