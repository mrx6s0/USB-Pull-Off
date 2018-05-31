#!/usr/bin python
# -*- coding: utf-8 -*-


"""
Wait until an usb is plugged on machine, and then do something. 
What? Oh...

import os
import re
import shutil
import yaml
from getpass import getuser
from platform import node
from pprint import pprint
from jinja2 import Template

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from threading import Thread
from os.path import basename
from string import digits
import time
import dbus
import future



"""

import os
import re
import shutil
import yaml
from getpass import getuser
from platform import node
from pprint import pprint
from jinja2 import Template

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from threading import Thread
from os.path import basename
from string import digits
import time
import dbus
import future

class ListenTo(Thread):
    def __init__(self, callback_function):
        super(ListenTo, self).__init__()

        if not callable(callback_function):
            raise TypeError("Object is not callabble...")

        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()

        self.signal = "InterfacesAdded"
        self.interface = "org.freedesktop.DBus.ObjectManager"
        self.bus.add_signal_receiver(callback_function, self.signal, self.interface)

    def run(self):
        loop = GLib.MainLoop()
        loop.run()


def get_mount_point(device):
    with open("/proc/mounts", "r") as partitions:
        for info in partitions:
            for path in info.split():
                if device in basename(path):
                    properties = info.split()
                    return properties[1]


def signal_receive(path=None, properties=None):
    if "org.freedesktop.UDisks2.Drive" in properties:
        info = properties["org.freedesktop.UDisks2.Drive"]
        print("\nDispositivo Encontrado:", info["Id"])
    if "org.freedesktop.UDisks2.Block" in properties:
        time.sleep(1)
        device = basename(path)

        for char in device:
            if char in digits:
                print("---------------")
                print("Nova Partição Encontrada:", device)
                print("Ponto de Montagem:", get_mount_point(device))

if __name__ == '__main__':


    listener = ListenTo(signal_receive)
    listener.start()
    print("Esperando dispositivo ser inserido...\n")
