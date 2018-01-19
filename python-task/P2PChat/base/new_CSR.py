__author__ = 'kowalski'
import threading
import socket

import config
import base.text
import base.net
import base.handler


class Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.running = 1

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))

        if len(config.send_array) == 0:
            base.text.write_to_screen(
                "Socket is good, waiting for connections on port: " +
                str(self.port), "System")
        s.listen(1)

        while self.running:
            conn, addr = s.accept()
            if conn_check(conn, config.send_array):
                config.send_array.append(conn)
            else:
                conn.close()
                continue

            base.text.write_to_screen("Connected by " + str(addr[0]), "System")
            #отправление длины и самого никнейма
            conn.send(base.net.format_number(len(config.username))
                      .encode(encoding='UTF-8'))
            conn.send(config.username.encode(encoding='UTF-8'))
            # получения никнейма
            data = conn.recv(4)
            data = conn.recv(int(data.decode(encoding='UTF-8')))
            if data.decode(encoding='UTF-8') != "Self":
                config.username_array[conn] = data.decode(encoding='UTF-8')
                config.contact_array[str(addr[0])] = [str(self.port),
                                                      data.decode(encoding=
                                                                  'UTF-8')]
            else:
                config.username_array[conn] = addr[0]
                config.contact_array[str(addr[0])] = [str(self.port),
                                                      "No_nick"]
            base.handler.pass_friends(conn)
            if addr[0] not in config.address_array:
                config.address_array.append(addr[0])
                Client(addr[0], config.port).start()
            else:
                continue


def runner(conn):
    while 1:
        data = base.net.net_catch(conn)
        if data != 1:
            base.text.write_to_screen(data, config.username_array[conn])


class Client(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.running = 1

    def run(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))
        if conn_check(conn, config.get_array):
            config.get_array.append(conn)
            base.text.write_to_screen("Connected to: " + self.host +
                                      " on port: " + str(self.port), "System")
            config.address_array.append(self.host)

            conn.send(base.net.format_number(len(config.username))
                      .encode(encoding='UTF-8'))
            conn.send(config.username.encode(encoding='UTF-8'))

            data = conn.recv(4)
            data = conn.recv(int(data.decode(encoding='UTF-8')))
            if data.decode(encoding='UTF-8') != "Self":
                config.username_array[conn] = data.decode(encoding='UTF-8')
                config.contact_array[conn.getpeername()[0]] = [str(self.port),
                                                               data.decode(
                                                               encoding=
                                                               'UTF-8')]
            else:
                config.username_array[conn] = self.host
                config.contact_array[conn.getpeername()[0]] = [str(self.port),
                                                               "No_nick"]
            threading.Thread(target=runner, args=(conn,)).start()
        else:
            conn.close()


def conn_check(conn, array):
    for i in array:
        if conn.getpeername()[0] == i.getpeername()[0]:
            return False
    return True