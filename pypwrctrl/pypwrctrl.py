#!/usr/bin/env python3

import time
import socket
import select

class Plug:

    def __init__(self, device, index, name, state=-1):
        self.device = device
        self.name = name
        self.index = index
        self.state = state

    def switch(self, state):
        cmd = 'on' if state else 'off'
        msg = "Sw_{}{}".format(cmd, self.index)
        self.device._send(msg, True)

class PlugDevice:

    def __init__(self, master, address, name, plug_descs):
        self.master = master
        self.name = name
        self.address = address

        self.plugs = []

        for desc in plug_descs:
            index, name = desc[0:2]
            state = desc[2] if len(desc) > 2 else -1

            self.plugs.append(Plug(self, index, name, state))

    def _send(self, data, secured=False):
        self.master._send(self.address, data, secured)

    def _receive(self, until):
        return self.master._receive(until, self.address)

class PlugMaster:

    def __init__(self, pin=77, pout=74, user="admin", password="anel"):
        self.pin = pin
        self.pout = pout
        self.user = user
        self.password = password

        self.sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sout.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sin.bind(('0.0.0.0', pin))

    def _send(self, address, data, secured=False):
        if secured:
            data = data + self.user + self.password

        print(data)
        self.sout.sendto(data.encode('utf8'), (address, self.pout))

    def _receive(self, address, until):
        sin = self.sin

        while True:
            # what time is it?
            now = time.time()

            # are we done?
            if now >= until:
                return None

            # wait for incoming messages
            rl, _, _ = select.select([sin], [], [], until - now)

            # timeout?
            if len(rl) == 0:
                return None

            # receive
            data, sender = self.sin.recvfrom(2048)

            # right sender?
            if address == None or sender == address:
                return data.decode('utf8')

    def discover(self, timeout=1):
        known = set()
        devices = []

        # request the answers
        self._send('255.255.255.255', 'wer da?')

        until = time.time() + timeout

        while True:
            data = self._receive(None, until)

            if data:
                parts = data.strip().split(':')

                name = parts[1]
                address = parts[2]

                # add only once
                if address in known:
                    continue
                else:
                    known.add(address)

                # bit mask of blocked plugs
                blocked = int(parts[14])

                plugs = []

                # add unblocked plugs
                for index, part in enumerate(parts[6:14]):
                    if not blocked & 1 << index:
                        name, active = part.rsplit(',', 1)
                        plugs.append((index + 1, name, int(active)))

                device = self.create_device(address, name, plugs)

                devices.append(device)
            else:
                break

        return devices

    def create_device(self, address, name, plugs):
        return PlugDevice(self, address, name, plugs)

