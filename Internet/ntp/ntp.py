from ipaddress import IPv4Address
from time import time, strftime, gmtime
from struct import pack, unpack
from decimal import Decimal
import socketserver
import threading


NTP_PORT = 123
DEFAULT_BUFFER_SIZE = 64 * 1024

NTP_CURRENT_VERSION = 4

NTP_HEADER_FORMAT = ">BBBBII4sQQQQ"
NTP_HEADER_LENGTH = 48
NTP_UTC_OFFSET = 2208988800

LEAP_STRING_VALUE = ["No warning",
               "Last minute of the day has 61 seconds",
               "Last minute of the day has 59 seconds",
               "Unknown (clock unsynchronized)"]

MODE_STRING_VALUE = ["Reserved",
               "Symmetric active",
               "Symmetric passive",
               "Client",
               "Server",
               "Broadcast",
               "NTP control message",
               "Reserved for private use"]


def utc_to_ntp_bytes(time):
    return int((Decimal(time) + NTP_UTC_OFFSET) * (2 ** 32))


def ntp_bytes_to_utc(value):
    return Decimal(value) / (2 ** 32) - NTP_UTC_OFFSET


def utc_to_string(value):
    return strftime("%a, %d %b %Y %H:%M:%S UTC", gmtime(value))


def from_ntp_short_bytes(value):
    return Decimal(value) / (2 ** 16)


def from_ntp_time_bytes(value):
    return Decimal(value) / (2 ** 32)


def get_bytes(value, size=None):
    if isinstance(value, bytes):
        return " ".join(["%02X" % e for e in value])
    if isinstance(value, int):
        if size == 1:
            return get_bytes(pack('>B', value))
        if size == 2:
            return get_bytes(pack('>H', value))
        if size == 4:
            return get_bytes(pack('>I', value))
        if size == 8:
            return get_bytes(pack('>Q', value))


def get_bits(size, bits_count, bits_offset, value):
    bytes = pack('>I', value)
    binary_string = ''.join(['{0:08b}'.format(byte) for byte in bytes])
    return '.' * bits_offset + binary_string[-bits_count:] + '.' * (size * 8 - bits_count - bits_offset)


def hexdump(series):
    offset = 0
    result = ''
    for row in series:
        if len(row) == 4:
            size, title, binary_value, value = row
            result += '%04X: %-30s %s: %s\n' % (offset, get_bytes(binary_value, size), title, str(value))
            offset += size
        else:
            size, pieces = row
            local_result = ''
            bits_offset = 0
            for piece in pieces:
                bits_count, title, binary_value, value = piece
                local_result += '      %-30s %s: %s\n' \
                                % (get_bits(size, bits_count, bits_offset, binary_value), title, str(value))
                bits_offset += bits_count
            result += ('%04X:' % offset) + local_result[5:]
            offset += size
    return result


class Packet(object):
    def __init__(self, leap=0, version=NTP_CURRENT_VERSION, mode=3, stratum=16, poll=0, precision=0, root_delay=0,
                 root_dispersion=0, ref_id=b'\x00' * 4, ref_time=0, origin=0, receive=0,
                 transmit=0):
        self.leap = leap
        self.version = version
        self.mode = mode
        self.options = (self.leap << 6) | (self.version << 3) | self.mode
        self.stratum = stratum
        self.poll_binary = poll
        self.poll = 2 ** (-poll)
        self.precision_binary = precision
        self.precision = 2 ** (-precision)
        self.root_delay_binary = root_delay
        self.root_delay = from_ntp_short_bytes(root_delay)
        self.root_dispersion_binary = root_dispersion
        self.root_dispersion = from_ntp_short_bytes(root_dispersion)
        self.ref_id_binary = ref_id
        self.ref_id = str(IPv4Address(ref_id))
        self.ref_time_binary = ref_time
        self.ref_time = from_ntp_time_bytes(ref_time)
        self.origin_binary = origin
        self.origin = from_ntp_time_bytes(origin)
        self.receive_binary = receive
        self.receive = from_ntp_time_bytes(receive)
        self.transmit_binary = transmit
        self.transmit = from_ntp_time_bytes(transmit)

    @classmethod
    def from_binary(cls, data):
        options, stratum, poll, precision, root_delay, root_dispersion, \
        ref_id, ref_time, origin, receive, transmit \
            = unpack(NTP_HEADER_FORMAT, data[:NTP_HEADER_LENGTH])
        leap, version, mode = options >> 6, ((options >> 3) & 0x7), options & 0x7
        return Packet(leap, version, mode, stratum, poll, precision, root_delay, root_dispersion, ref_id, ref_time,
                      origin, receive, transmit)

    def to_binary(self):
        return pack(NTP_HEADER_FORMAT,
                    self.options,
                    self.stratum,
                    self.poll_binary,
                    self.precision_binary,
                    self.root_delay_binary,
                    self.root_dispersion_binary,
                    self.ref_id_binary,
                    self.ref_time_binary,
                    self.origin_binary,
                    self.receive_binary,
                    self.transmit_binary)


def get_time_string(time, show_utc):
    return str(time) + (' [%s]' % utc_to_string(max(time - NTP_UTC_OFFSET, 0)) if show_utc else '')


def get_packet_hexdump(packet, show_utc='store_true'):
    return hexdump((
        (1,
         ((2, 'Leap', packet.leap, LEAP_STRING_VALUE[packet.leap]),
          (3, 'Version', packet.version, packet.version),
          (3, 'Mode', packet.mode, MODE_STRING_VALUE[packet.mode]))),
        (1, 'Stratum', packet.stratum, packet.stratum),
        (1, 'Poll', packet.poll_binary, packet.poll),
        (1, 'Precision', packet.precision_binary, packet.precision),
        (4, 'Root delay', packet.root_delay_binary, packet.root_delay),
        (4, 'Root dispersion', packet.root_dispersion_binary, packet.root_dispersion),
        (4, 'Reference ID', packet.ref_id_binary, packet.ref_id),
        (8, 'Reference timestamp', packet.ref_time_binary, get_time_string(packet.ref_time, show_utc)),
        (8, 'Origin timestamp', packet.origin_binary, get_time_string(packet.origin, show_utc)),
        (8, 'Receive timestamp', packet.receive_binary, get_time_string(packet.receive, show_utc)),
        (8, 'Transmit timestamp', packet.transmit_binary, get_time_string(packet.transmit, show_utc))
    ))


class ThreadedUDPServer(socketserver.ThreadingMixIn,socketserver.UDPServer):
    pass

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        packet = Packet.from_binary(data)
        print(get_packet_hexdump(packet))

if __name__ == "__main__":
    udp_server = ThreadedUDPServer(('',NTP_PORT),ThreadedUDPRequestHandler)
    udp_thread = threading.Thread(target=udp_server.serve_forever)
    udp_thread.start()
    print('NTP working at port ', str(NTP_PORT))