import base64
import getpass
import socket
import ssl
import os
import sys
import argparse

class SMTP:
    def __init__(self, mail_server='', mailport=465, mailfrom='', mailrcpt='',
                 wd=os.getcwd(), username = '', password = ''):
        self.mail_server = mail_server
        self.mail_port = mailport
        self.mail_from = mailfrom
        self.mail_rcpt = mailrcpt
        self.mail_mess = self.make_mess(wd)
        self.username = username
        self.password = password

    # Function - getSSLSocket
    # Description - creates a new socket, wraps it in an SSL context, and returns it
    def getSSLSocket(self):
        return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)

    # Function - getTLSSocket
    # Description - creates a new socket, wraps it in a TLS context, and returns it
    def getTLSSocket(self):
        return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_TLSv1)

    # Function - getPlainSocket
    # Description - creates a new vanilla socket and returns it
    def getPlainSocket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def session(self):
        # if cryptmethod == 'SSL':
        sock = self.getSSLSocket()
        # elif cryptmethod == 'TLS':
        #     sock = getTLSSocket()
        # else:
        # Attempt to connect to the SMTP server
        sock.connect((self.mail_server, self.mail_port))
        # Receive response from server and print it
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))

        heloMesg = 'EHLO {0}\r\n'.format(self.username.split('@')[0])
        print(heloMesg)
        sock.send(heloMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))

        authMesg = 'AUTH LOGIN\r\n'
        crlfMesg = '\r\n'
        print(authMesg)
        sock.send(authMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        user64 = base64.b64encode(self.username.encode('utf-8'))
        pass64 = base64.b64encode(self.password.encode('utf-8'))
        print(user64)
        sock.send(user64)
        sock.send(crlfMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        print(pass64)
        sock.send(pass64)
        sock.send(crlfMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        # Tell server the message's sender
        fromMesg = 'MAIL FROM: <' + self.mail_from + '>\r\n'
        print(fromMesg)
        sock.send(fromMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        # Tell server the message's recipient
        rcptMesg = 'RCPT TO: <' + self.mail_rcpt + '>\r\n'
        print(rcptMesg)
        sock.send(rcptMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        # Give server the message
        dataMesg = 'DATA\r\n'
        print(dataMesg)
        sock.send(dataMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        mailbody = self.mail_mess + b'\r\n'
        print(mailbody)
        sock.send(mailbody)
        fullStop = '\r\n.\r\n'
        print(fullStop)
        sock.send(fullStop.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        # Signal the server to quit
        quitMesg = 'QUIT\r\n'
        print(quitMesg)
        sock.send(quitMesg.encode('utf-8'))
        respon = sock.recv(2048)
        print(str(respon, 'utf-8'))
        # Close the socket to finish
        sock.close()

    def make_mess(self, wd=os.getcwd()):
        types = ["jpg", "png", "jpeg", "bmp"]
        f = []
        text = b""
        for root, dirs, files in os.walk(wd):
            for name in files:
                if name.split('.')[1] in types:
                    f.append((os.path.join(root, name), name))
        text += b"From: " + self.mail_from.encode('utf-8') + b"\r\n"
        text += b"To: " + self.mail_rcpt.encode('utf-8') + b"\r\n"
        text += b"Subject: NET-PIC\r\n"
        text += b'Content-type: multipart/mixed; boundary="bound"\r\n\r\n'
        text += b"--bound\r\ncontent-type: text/plain;\r\n\r\n"
        text += b"\t\tNET pictures\r\n"
        for i in f:
            text += ('--bound\r\nContent-type: image/jpeg; name="{0}"\r\n'
                    'Content-ID: <{0}>\r\n'
                    'X-Attachment-Id: {0}\r\n'
                    'Content-Disposition: inline; filename="{0}"\r\n'
                    'Content-Transfer-Encoding: base64\r\n\r\n'.format(i[1])).encode('utf-8')
            with open(i[0], "rb") as txt:
                enc = base64.b64encode(txt.read())
            text += enc + b'\r\n'
        text += b'--bound--'
        return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SMTP Port')
    parser.add_argument('smtpserver',help = 'address of smtp server')
    parser.add_argument('rcpt', help='to')
    parser.add_argument('user', help='user login')
    parser.add_argument('password', help='user password')
    args = parser.parse_args()
    s = SMTP(args.smtpserver, 465, args.user, args.rcpt, os.getcwd(), args.user, args.password)
    s.session()
