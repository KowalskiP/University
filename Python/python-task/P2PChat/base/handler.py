__author__ = 'kowalski'

import config
import base.net
import base.new_CSR
import base.text


def event_handler(number, conn=None):
    num = int(number[1:])
    # отключение или одного соединения, или мы - клиент
    if num == 1:
        if conn is None:
            base.text.write_to_screen("Соединение закрыто.", "System")
            for i in config.send_array:
                i.send("-001".encode())
            config.send_array.clear()
            config.get_array.clear()
            config.address_array.clear()
        else:
            base.text.write_to_screen("Соединение через " + conn.getpeername()
                                      [0] + " закрыто.", "System")
            for i in config.send_array:
                if i.getpeername()[0] == conn.getpeername()[0]:
                    config.send_array.remove(i)
                    break
            config.get_array.remove(conn)
            config.address_array.remove(conn.getpeername()[0])
    # смена ника
    elif num == 2:
        name = base.net.net_catch(conn)
        if (is_username_free(name)):
            base.text.write_to_screen(
                "Пользователь " + config.username_array[conn] +
                " изменил свой ник на " + name, "System")
            config.username_array[conn] = name
            config.contact_array[
                conn.getpeername()[0]] = [conn.getpeername()[1], name]
    # при подключении пользователя к серверу разослать его адрес и
    # порт для отрпавки сообщения
    elif num == 4:
        data = conn.recv(4)
        data = conn.recv(int(data.decode(encoding='UTF-8')))
        base.new_CSR.Client(data.decode(encoding='UTF-8'),
                            int(config.contact_array[conn.getpeername()[0]][0])
                            ).start()


def is_username_free(name):
    """Прорверить, занят ли никнейм."""
    for conn in config.username_array:
        if name == config.username_array[conn] or name == config.username:
            return False
    return True


def pass_friends(conn):
    """Отправка информации о соединения пользователья к серверу текущим
    пользователям"""
    for connection in config.send_array:
        if conn.getpeername()[0] != connection.getpeername()[0]:
            conn.send("-004".encode(encoding='UTF-8'))
            conn.send(
                base.net.format_number(len(connection.getpeername()[0]))
                .encode(encoding='UTF-8'))
                # отправка ip адреса
            conn.send(connection.getpeername()[0].encode(encoding='UTF-8'))
