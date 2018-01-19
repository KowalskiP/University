import argparse
import re
import socket
import select
from ipaddress import IPv4Address

BUFFER = 4 * 1024
DEFAULT_WHOIS_PORT = 43
SOCKET_CONNECT_TIMEOUT = 1
SOCKET_POLLING_PERIOD = 0.25
PORT = 31337
MAX_HOPS = 30
TYPE = 8
CODE = 0
CHECKSUM = 247, 248
ICMP_PRTCL = socket.getprotobyname('icmp')
PACKET = bytearray(
    [TYPE, CODE, CHECKSUM[0], CHECKSUM[1], 0, 1, 0, 6] + 64 * [0])


class WhoIs:
    def __init__(self, address):
        self.address = address

    @staticmethod
    def get_address(address_string):
        part = address_string.split(':')
        return part[0], int(part[1]) if len(part) > 1 else DEFAULT_WHOIS_PORT

    @staticmethod
    def receive_data(sock):
        result = b''
        while select.select([sock], [], [], SOCKET_POLLING_PERIOD)[0]:
            data = sock.recv(BUFFER)
            if len(data) == 0:
                break
            result += data
        return result

    def receive_information(self, target, address):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(SOCKET_CONNECT_TIMEOUT)
            sock.connect(address)
            sock.setblocking(0)
            result = self.receive_data(sock).decode('utf-8')
            sock.sendall((target + "\r\n").encode('utf-8'))
            result += self.receive_data(sock).decode('utf-8')
        return result

    def main(self):
        try:
            socket_address = self.get_address(self.address[1])
            target = str(IPv4Address(self.address[0]))
            temp_res = self.receive_information(target, socket_address)
            res = re.search("whois\.(.)+", temp_res)
            if res:
                provider = res.group(0).strip()
                socket_address = (provider, DEFAULT_WHOIS_PORT)
                temp_res = self.receive_information(target, socket_address)
                res = re.search('country:(.)+', temp_res)
                if res:
                    print(res.group(0))
                else:
                    print("country is not defined")
                res = re.search('(origin:)|(AS\d+)(.)+', temp_res)
                if res:
                    print(res.group(0))
                else:
                    print("AS is not defined")
            else:
                print("country is not defined. IP status - RESERVE")
        except Exception as e:
            print(e)
            print("Failed to request info about {} from {}"
                  .format(self.address[0], self.address[1]))


class Tracer:
    @staticmethod
    def trace(address):
        TTL = 1
        icmp_socket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, ICMP_PRTCL)
        icmp_socket.bind(('', PORT))
        address_list = []
        try:
         while True:
            icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
            TTL += 1
            icmp_socket.sendto(PACKET, (address, PORT))
            current_addr = ''
            try:
                icmp_socket.settimeout(3)
                _, current_addr = icmp_socket.recvfrom(BUFFER)
            except socket.error:
                print(str(TTL - 1) + " Time out for request")
            if current_addr:
                current_addr = current_addr[0]
                if not (current_addr in address_list):
                    address_list.append(current_addr)
            if current_addr == address:
                return address_list
            if TTL - 1 == MAX_HOPS:
                return address_list
        except socket.error as e:
            print(e)
        finally:
            icmp_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python 3 Tracer")
    parser.add_argument(
        "addresses", nargs="+", help="addresses of destination")
    args = parser.parse_args()
    result = []
    for i in args.addresses:
        result.append(Tracer.trace(socket.gethostbyname(i)))
    for i in result:
        print(args.addresses[result.index(i)])
        for j in i:
            print(j)
            w = WhoIs([j, "whois.iana.org:43"])
            w.main()
        print()