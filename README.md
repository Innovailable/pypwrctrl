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

Furthermore there is no feedback on the state changes in the protocol. Your
packages might get lost somewhere in your network and you would never know it.
I might implement resends and status checks after the commands to resolve this
issue in the future.

## Installation

Simply run

	./setup.py install --user

## Usage

For simple usage information type:

	pypwrctrl --help

This tutorial will give a more detailed introduction with examples.

First configure your NET-PwrCtrl to handle the UDP protocol (please note
*Security Notes* above) and set both ports to something above the privileged
ports. Both of these configuration options are in the *Lan* page of the
webinterface. I am going to assume a sending port of 4165, a receiving port of
4166, and the user 'ulf' with the password 'secret' in the following examples.

First let us try to discover the device:

	pypwrctrl -d -i 4165 -o 4166 -u ulf -p secret show

The *-d* is the switch which enables network discovery and the other two
switches tell the program which ports are used for communication.

Always typing the port options is tiresome. We should save them in the
configuration file:

	pypwrctrl -i 4165 -o 4166 -u ulf -p secret save

Now we can discover devices with a simpler command:

	pypwrctrl -d show

You can also save the discovered devices and plugs for faster access:

	pypwrctrl -d save

Every configuration item can be changed by setting it with its command line
switch and applying the 'save' command.

Now to the part you are actually here for: Controlling the power of the power
outlets. Turning a power outlet on is as simple as writing:

	pypwrctrl on 192.168.1.50 1

Turning it off again is just as easy:

	pypwrctrl off 192.168.1.50 1

Both commands change the state of the socket '1' of the device at
'192.168.1.50'. You can leave out the address if you have only one device or
want to affect all devices.

Did you know that you can assign names to the individual sockets? Set a
sensible name in the webinterface of your device and use it to select the
socket in *pypwrctrl*:

	pypwrctrl on fan

Devices can also be named.

