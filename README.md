# pypwrctr

## Introduction

This is a library and command line utility for Anel NET-PwrCtrl network
controllable extension leads. It offers the functionality provided by the UDP
protocol. Devices can be found by network discovery and saved into a
configuration file for easy access.

The UDP protocol has to be enabled in the NET-PwrCtrl devices in order to
control them with this tool.

## Installation

Simply run

	./setup.py install --user

## Usage

TODO

## Security Notes

Enabling the UDP protocol is quite insane from a security standpoint. The user
credentials are tranmitted as plaintext in the commands requiring
authentication. Never use this tool or this protocol if you cannot live with
the plugs being controlled by anyone having access to the network!

