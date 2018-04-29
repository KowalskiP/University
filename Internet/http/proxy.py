import socket
import threading
import select
import argparse

BUFFER = 8192
BLOCKED = []
METHODS = (b'GET', b'POST', b'HEAD', b'PUT', b'OPTIONS', b'TRACE', b'DELETE')


class Proxy(threading.Thread):
    def __init__(self, connection, address, timeout):
        threading.Thread.__init__(self)
        self.client = connection
        self.address = address
        self.timeout = timeout
        self.buffer_storage = b''

    def print_method(self, method):
        m = method.split(' ')
        print(self.name + ': ' + m[0] + ' ' + m[1])

    def get_headres(self):

        while True:
            self.buffer_storage += self.client.recv(BUFFER)
            end = self.buffer_storage.find(b'\n')
            if end != -1:
                break

        self.print_method(self.buffer_storage[:end].decode())

        data = (self.buffer_storage[:end+1]).split()
        self.buffer_storage = self.buffer_storage[end+1:]
        return data

    def connect_through_proxy(self):

        self.make_connection(self.URL)
        self.client.send(
            'HTTP/1.1 200 Connection established'
            '\nProxy-agent: Python Proxy/1.0\n\n'.encode())
        self.buffer_storage = b''
        self.send_packets()

    def process_method(self):

        for i in range(0, len(BLOCKED)):
            if BLOCKED[i].encode() in self.URL:
                print ("BLOCKED " + self.URL.decode())
                return

        self.URL = self.URL[7:]
        i = self.URL.find(b'/')
        host = self.URL[:i]
        URL = self.URL[i:]

        self.make_connection(host)
        self.target.send(
            self.method + b' ' + URL +
            b' ' + self.proto + b'\n' + self.buffer_storage)
        self.buffer_storage = b''

        self.send_packets()

    def make_connection(self, host):

        i = host.find(b':')
        if i != -1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80

        (socket_option, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(socket_option)
        self.target.connect(address)

    def send_packets(self):
        max_timeout = self.timeout/2
        sockets = [self.client, self.target]
        count = 0

        while True:
            count += 1
            (recv, _, error) = select.select(sockets, [], sockets, 3)
            if error:
                break

            if recv:
                for in_ in recv:
                    data = in_.recv(BUFFER)
                    if in_ is self.client:
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.send(data)
                        count = 0

            if count == max_timeout:
                break

    def run(self):
        self.method, self.URL, self.proto = self.get_headres()
        if self.method == b'CONNECT':
            self.connect_through_proxy()
        elif self.method in METHODS:
            self.process_method()

        try:
            self.client.close()
            self.target.close()
        except Exception as e:
            pass


if __name__ == '__main__':
    with open('ads.txt') as ads:
        BLOCKED = ads.readlines()

    BLOCKED = [i[:-1] for i in BLOCKED]

    parser = argparse.ArgumentParser(description='Proxy server on Python3')
    parser.add_argument('port', help='port for proxy',
                        nargs='?', type=int, default=31337)
    args = parser.parse_args()

    proxy_socket = socket.socket()
    proxy_socket.bind(('localhost', args.port))
    proxy_socket.listen(0)

    print ("Start Proxy on %s:%d" % ('localhost', args.port))

    while True:
        conn, address = proxy_socket.accept()
        Proxy(conn, address, 60).start()
