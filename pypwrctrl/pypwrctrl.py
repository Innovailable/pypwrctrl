#!/usr/bin/env python3
##############################################################################
##
##  pypwrctrl - Anel NET-PwrCtrl library and command line utility
##  Copyright 2013 Thammi
##
##  pypwrctrl is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  pypwrctrl is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with pypwrctrl.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

import time
import socket
import select
import struct

CHARSET="latin"

class Plug:

    def __init__(self, device, index, name, state=-1):
        self.device = device
        self.name = name
        self.index = index
        self.state = state

    def switch(self, state, timeout=1):
        cmd = 'on' if state else 'off'
        msg = "Sw_{}{}".format(cmd, self.index)

        self.device.master._drain_socket()

        self.device._send(msg, True)

        expected = "1" if state else "0"

        def check_switch(data):
            part = data.split(':')[5+self.index]
            new_state = part.rsplit(',', 1)[1]

            return new_state == expected

        return self.device._expect(check_switch, timeout)

    def timed_off(self, time, timeout=1):
        msg = 'St_off{}'.format(self.index).encode(CHARSET)
        msg += struct.pack('>h', time)

        self.device.master._drain_socket()

        self.device._send(msg, True)

        def check_response(data):
            return True

        return self.device._expect(check_response, timeout)


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

    def search_plug(self, needle):
        found = set()

        if needle.isdigit():
            index = int(needle)
            found.update(filter(lambda plug: plug.index == index, self.plugs))

        found.update(filter(lambda plug: plug.name == needle, self.plugs))

        return found

    def _send(self, data, secured=False):
        self.master._send(self.address, data, secured)

    def _expect(self, condition, timeout):
        return self.master._expect(self.address, condition, timeout)

    def _receive(self, until):
        return self.master._receive(self.address, until)

    def reset(self):
        self._send("Reset:", True)


class PlugMaster:

    def __init__(self, pin=77, pout=75, user="admin", password="anel",
                 iface=None):
        self.pin = pin
        self.pout = pout
        self.user = user
        self.password = password

        self.iface = iface
        self.devices = []

        self.sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.iface is not None:
                self.sin.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE,
                                    bytes(iface, 'UTF-8'))

        self._bind()

        self.sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sout.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if self.iface is not None:
                self.sout.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE,
                                     bytes(iface, 'UTF-8'))

    def _bind(self, retries=20):
        try:
            self.sin.bind(('0.0.0.0', self.pin))
        except PermissionError as err:
            # reraise as this is not going to change
            raise err from None
        except OSError as err:
            # probably address in use, can retry

            if retries <= 0:
                raise err from None

            time.sleep(0.1)
            self._bind(retries - 1)

    def search_device(self, needle):
        found = set()

        found.update(filter(lambda dev: dev.address == needle, self.devices))
        found.update(filter(lambda dev: dev.name == needle, self.devices))

        return found

    def search_plug(self, needle):
        found = set()

        for device in self.devices:
            found.update(device.search_plug(needle))

        return found

    def _send(self, address, data, secured=False):
        if isinstance(data, str):
            data = data.encode(CHARSET)

        if secured:
            auth = self.user + self.password
            data = data + auth.encode(CHARSET)

        self.sout.sendto(data, (address, self.pout))

    def _drain_socket(self):
        while self._receive(None, 0):
            pass

    def _expect(self, address, condition, timeout):
        until = time.time() + timeout

        while True:
            data = self._receive(address, until)

            if data == None:
                return False

            if condition(data):
                return True

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
            data, (sender, port) = self.sin.recvfrom(2048)

            # right sender?
            if address == None or sender == address:
                return data.decode(CHARSET)

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

                name = parts[1].strip()
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
                        pname, active = part.rsplit(',', 1)
                        plugs.append((index + 1, pname, int(active)))

                device = self.create_device(address, name, plugs)

                devices.append(device)
            else:
                break

        return devices

    def create_device(self, address, name, plugs):
        device = PlugDevice(self, address, name, plugs)
        self.devices.append(device)
        return device

