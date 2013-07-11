#!/usr/bin/env python3

import time
import socket
import select

class PlugMaster:

    def __init__(self, pin=77, pout=74, user="admin", password="anel"):
        self.pin = pin
        self.pout = pout
        self.user = user
        self.password = password

        self.sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sin.bind(('0.0.0.0', pin))

    def _send(self, data, address):
        self.sout.sendto(data, (address, self.pout))

    def _receive(self, until, address=None):
        sin = self.sin

        while True:
            now = time.time()

            if now >= until:
                return None

            rl, _, _ = select.select([sin], [], [], until - now)

            if len(rl) == 0:
                return None

            data, sender = self.sin.recvfrom(1024)

            if address == None or sender == address:
                return data

    def discover(self, timeout):
        plugs = []

        self._send('wer da?', '0.0.0.0')

        until = time.time() + timeout

        while True:
            data = self._receive(until)

            if data:
                plugs += data
            else:
                break

        return plugs

