from decimal import Decimal
import socket
import argparse
import threading
import struct
import time
import sys

DEFAULT_PORT = 8000
HEADER_LENGTH = 28 * 8
SYN = 2
WINDOW_SIZE = 8192
CHECK_SUM = 7644
ICMP = socket.getprotobyname('icmp')
NTP_HEADER_FORMAT = ">BBBBII4sQQQQ"
DNS_HEADER_FORMAT_START = ">HHHHHH"
DNS_HEADER_FORMAT_END = ">BHH"
MAIL_PROTOCOLOS = {'SMTP', "POP3"}
signatures = {'NTP': [], 'DNS': [], 'SMTP': [], 'POP3': [], 'HTTP': []}


def send_recv_packets(sock, data, addr, port):
    # print(data)
    # print((addr, port))
    sock.sendto(data, (addr, port))
    try:
        sock.settimeout(1)
        recv_data, recv_addr = sock.recvfrom(64*1024)
        # print(recv_data)
        print(10000)
        return 0, recv_data
    except socket.error as e:
        return 1, 0


def HTTP_proto(sock, addr, port):
    http_packet = b'GET / HTTP/1.1/\r\n\r\n'
    sock.sendto(http_packet, (addr, port))
    try:
        sock.settimeout(2)
        print(1)
        data = sock.recv(1024)
        print(data)
        if data == b'':
            signatures['HTTP'].append(port)
    except:
        pass


def SMTP_proto(answer, port):
    if answer and answer[:3] == b'220':
        signatures['SMTP'].append(port)


def POP3_proto(answer, port):
    if answer and (b'+OK' in answer or b'-ERR' in answer):
        signatures['POP3'].append(port)


def connectedTCP(sock, port, addr, list_result_ports):
    try:
        print(1)
        sock.settimeout(2)
        sock.connect((addr, int(port)))
        try:
            sock.settimeout(2)
            answer = sock.recv(1024)
            print(answer)
            SMTP_proto(answer, port)
            POP3_proto(answer, port)
        except socket.error:
            pass
        finally:
            list_result_ports.append(str(port))
            DNS_proto(sock, addr, int(port))
            HTTP_proto(sock, addr, int(port))
    except socket.error as e:
        pass
    finally:
        sock.close()


def NTP_proto(sock, addr, port):
    ntp_packet = struct.pack(NTP_HEADER_FORMAT,
                             0, 0, 0, 0, 0, 0, b'\x00' * 4, 0, 0, 0,
                             int((Decimal(time.time())) * (2 ** 32)))
    ntp_packet = b'#\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd9\x12\xce\xb0\xba\xec|\x00'
    # print(ntp_packet)
    code, data = send_recv_packets(sock, ntp_packet, addr, port)
    # print(code)
    # print(data)
    if code == 0:
        try:
            data = struct.unpack(NTP_HEADER_FORMAT, data)
            signatures['NTP'].append(port)
        except:
            # print(200000)
            pass


def DNS_proto(sock, addr, port):
    dns_packet = struct.pack(DNS_HEADER_FORMAT_START, 1, 256, 1, 0, 0, 0)
    dns_packet = b'\x00\x03\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    dns_packet = b'\x00\x08\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01'
    # print(dns_packet[13:19])

    # split_url = "google.com".split(".")
    # middle_header = ''
    # for part in split_url:
        # dns_packet += struct.pack("B", len(part))
        # middle_header += 'B'
        # for byte in bytes(part, encoding='utf-8'):
            # dns_packet += struct.pack("B", byte)
            # middle_header += 'c'
    # dns_packet += struct.pack(DNS_HEADER_FORMAT_END, 0, 1, 1)
    # print(dns_packet)
    code, data = send_recv_packets(sock, dns_packet, addr, port)
    # print(code)
    # print(data[13:19])
    if code == 0:
        # result_header = DNS_HEADER_FORMAT_START + middle_header + DNS_HEADER_FORMAT_END
        # print(result_header)
        try:
            if data[13:19] == dns_packet[13:19]:
            # temp_data = struct.unpack(result_header, data[43:43+17+len(middle_header)])
                signatures['DNS'].append(port)
        except:
            pass


def connectedUDP(sock, port, addr, list_result_ports):
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)
    recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_sock.bind(("", DEFAULT_PORT))
    # mess_UDP = struct.pack(">HHHH", DEFAULT_PORT, int(port), 0, 0)
    PACKET = bytearray(
    [8, 0, 247, 248, 0, 1, 0, 6] + 64 * [0])
    recv_sock.sendto(PACKET, (addr, int(port)))
    try:
        recv_sock.settimeout(2)
        data, addr = recv_sock.recvfrom(1024)
        # print(data)
        icmp_header = data[20:28]
        t, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmp_header
        )
        # print(t)
        # print(code)
        if int(t) != 3 or int(code) != 3:
            list_of_ports.append(str(port))
            # print(port)
            NTP_proto(sock, addr[0], port)
            DNS_proto(sock, addr[0], port)
    except socket.error as e:
        list_result_ports.append(str(port))
        # print(1)
        NTP_proto(sock, addr, port)
        DNS_proto(sock, addr, port)
    finally:
        sock.close()


def create_thread(pool, temp_thread):
    while len(pool) > 10:
        for thread in pool:
            if thread.isAlive():
                thread.join()
                pool.remove(thread)
    temp_thread.start()
    pool.append(temp_thread)


def main(addr, list_of_ports):
    opensTCPports = []
    opensUDPports = []
    addr_host = socket.gethostbyname(addr)
    threads_pool = []
    for port in list_of_ports:
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        create_thread(threads_pool,
                      threading.Thread(target=connectedTCP, args=[socketTCP, port, addr_host, opensTCPports]))

        socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        create_thread(threads_pool,
                      threading.Thread(target=connectedUDP, args=[socketUDP, int(port), addr_host, opensUDPports]))
    time.sleep(5)
    print("open TCP ports: " + " ".join(opensTCPports))
    print("open UDP ports: " + " ".join(opensUDPports))
    print(signatures)


def get_args():
    parser = argparse.ArgumentParser(description="PortScan")
    parser.add_argument("addr", nargs="?",
                        default=socket.gethostbyname(socket.gethostname()), help="address of host")
    parser.add_argument("start_port", nargs="?", default=1, help="start port")
    parser.add_argument("end_port", nargs="?", default=2, help="final port")
    args = parser.parse_args()
    ports = [port for port in range(int(args.start_port), int(args.end_port) + 1)]
    return args.addr, ports


if __name__ == "__main__":
    host, list_of_ports = get_args()
    main(host, list_of_ports)