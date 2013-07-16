# pypwrctrl

## Introduction

This is a library and command line utility for Anel NET-PwrCtrl network
controllable extension leads. It offers the functionality provided by the UDP
protocol. Devices can be found by network discovery and saved into a
configuration file for easy access.

The UDP protocol has to be enabled in the NET-PwrCtrl devices in order to
control them with this tool.

## Security Notes

Enabling the UDP protocol is quite insane from a security standpoint. The user
credentials are tranmitted as plaintext in the commands requiring
authentication. Never use this tool or this protocol if you cannot live with
the plugs being controlled by anyone having access to the network!

## Installation

The program was written on Linux but should also run on Windows, Mac OS X, and
every other operating system supported by Python 3.

Simply run:

	easy_install3 --user pypwrctrl

Or checkout the repository and run:

	./setup.py install --user

You can remove the '--user' in both methods to install for all users of your
system (requires root privileges).

*pypwrctrl* depends only on 'python3' and 'python3-setuptools' for
installation.

## Usage

For simple usage information type:

	pypwrctrl --help

This tutorial will give a more detailed introduction with examples.

First configure your NET-PwrCtrl to handle the UDP protocol (please note
*Security Notes* above) and set both ports to something above the privileged
ports (>1024). These configuration options are in the *Lan* page of the
webinterface. I am going to assume a sending port of 4165, a receiving port of
4166, and the user 'ulf' with the password 'secret' in the following examples.

First let us try to discover the device:

	pypwrctrl -d -i 4165 -o 4166 -u ulf -p secret show

If you do not see any devices please make sure that UDP is enabled, the right
ports are configured, and the device is reachable from the device you are
testing this on.

The *-d* is the switch which enables network discovery and the other switches
tell the program which ports and user credentials are used.

Always typing the port options is tiresome. We should save them in the
configuration file:

	pypwrctrl -i 4165 -o 4166 -u ulf -p secret save

Now we can discover devices with a simpler command:

	pypwrctrl -d show

You can also save the discovered devices and plugs for faster access:

	pypwrctrl -d save

Every configuration item can be changed by setting it with its command line
switch and applying the 'save' command.

Now to the part you are actually here for: Controlling the state of the power
outlets. Turning a power outlet on is as simple as writing:

	pypwrctrl on 192.168.1.50 1

Turning it off again is just as easy:

	pypwrctrl off 192.168.1.50 1

Both commands change the state of the socket '1' of the device at
'192.168.1.50'. You can leave out the address if you have only one device or
want to control all devices with one command.

Did you know that you can assign names to the individual sockets? Set a
sensible name in the webinterface of your device and use it to select the
socket in *pypwrctrl*:

	pypwrctrl on fan

Devices can also be named.

## TODO

* resend messages
* add ability to control devices without configuration and '-d'
* test with more than one device and other product versions (used
  NET-PwrCtrl HOME)
* support Temperature, IO, ...

## License

pypwrctrl is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

pypwrctrl is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
pypwrctrl.  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
