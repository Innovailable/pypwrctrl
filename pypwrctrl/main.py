from pypwrctrl import PlugMaster

import sys
from optparse import OptionParser

def switch(master, args, state):
    if len(args) == 0:
        print("Not enough arguments. Please add at least a plug name.")
        return 1
    elif len(args) == 1:
        plugs = master.search_plug(args[0])
    elif len(args) == 2:
        plugs = set()
        devices = master.search_device(args[0])

        for device in devices:
            plugs.update(device.search_plug(args[1]))
    else:
        print("Too many arguments. Only plug name and optionally device name expected.")
        return 1

    if len(plugs) == 0:
        print("No matching plugs found, sorry")
        return 1
    elif len(plugs) > 1:
        print("Warning: Setting multiple matching plugs")

    for plug in plugs:
        plug.switch(state)

def reset(master, args):
    if len(args) == 0:
        print("Not enough arguments. Please add the device name.")
        return 1
    elif len(args) == 1:
        devices = master.search_device(args[0])
    else:
        print("Too many arguments. Only device name expected.")
        return 1

    if len(devices) == 0:
        print("No matching devices found, sorry")
        return 1
    elif len(devices) > 1:
        print("Warning: Resetting multiple matching devices")

    for device in devices:
        device.reset()

def save(master, args):
    raise NotImplemented("Configuration saving")

def show(master, args):
    device_count = len(master.devices)
    plug_count = 0

    for device in master.devices:
        print("{} ({}):".format(device.name, device.address))

        for plug in device.plugs:
            print("- {}".format(plug.name), end="")
            if plug.state >= 0:
                print(" ({})".format("on" if plug.state else "off"), end="")
            print()

        print()

        plug_count += len(device.plugs)

    print("There are {} device(s) with {} plug(s)".format(device_count, plug_count))

def main():
    commands = {
            'on': (
                lambda master, args: switch(master, args, True),
                "[device] plug",
                "switch plug on",
                ),
            'off': (
                lambda master, args: switch(master, args, False),
                "[device] plug",
                "switch plug off",
                ),
            'save': (
                save,
                "",
                "save options and discovered devices",
                ),
            'show': (
                show,
                "",
                "show all discovered or saved devices",
                ),
            'reset': (
                reset,
                "",
                "save options and discovered devices",
                ),
            }

    usage = "usage: %prog [options] command [comand options]"

    parser = OptionParser(usage=usage)

    parser.add_option("-l", "--list",
            action="store_true", dest="list",
            help="List available commands and options")

    parser.add_option("-d", "--discover",
            action="store_true", dest="discover",
            help="Discover devices on network")

    parser.add_option("-u", "--user", dest="user", default="admin",
            help="Username on device (default from config or 'admin')", metavar="USER")
    parser.add_option("-p", "--password", dest="password", default="anel",
            help="Password on device (default from config or  'anel')", metavar="PASSWORD")

    parser.add_option("-i", "--in", dest="pin", default=75, type="int",
            help="Port to use for receiving (sending from device perspective, default from config or 75)", metavar="PORT")
    parser.add_option("-o", "--out", dest="pout", default=77, type="int",
            help="Port to use for sending (sending from device perspective, default from config or 77)", metavar="PORT")

    (options, args) = parser.parse_args()

    # print command list
    if options.list:
        print("The following commands are available:")

        for name, (fun, usage, desc) in sorted(commands.items(), key=lambda a: a[0]):
            print("- {} {} ({})".format(name, usage, desc))

        return 0

    # command given?
    if len(args) == 0:
        print("Command missing, please add one")
        return 1

    # split arguments
    command = args[0]
    rest = args[1:]

    # valid command?
    if command not in commands:
        print("Unknown command, sorry")
        return 1

    # do we have to load the configuration?
    if not options.discover and command != 'save':
        raise NotImplemented("Configuration loading")

    master = PlugMaster(options.pin, options.pout, options.user, options.password)

    if options.discover:
        master.discover()

    return commands[command][0](master, rest)

if __name__ == '__main__':
    sys.exit(main())
