# -*- coding: utf-8 -*-
# @author: leesoar

"""Raspberry Pi"""

import os
import platform
import re


MAC_ADDR_PREFIX = [
    "B8:27:EB",
    "DC:A6:32",
    "E4:5F:01",
    "B8-27-EB",
    "DC-A6-32",
    "E4-5F-01",
]


def get_raspberry_pi():
    cur_system = platform.system()
    command = f"""arp -na | grep -i -E '{"|".join(MAC_ADDR_PREFIX)}'"""

    if "window" in cur_system.lower():
        command = f'''arp -a | findstr -i "{' '.join(MAC_ADDR_PREFIX)}"'''

    res = os.popen(command).read()
    if not res:
        return

    devices = []
    for r in res.rstrip("\n").split("\n"):
        ip = re.search(r"(\d{1,3}\.){3}\d{1,3}", r).group()
        try:
            mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", r).group()
        except AttributeError:
            mac = "incomplete"
        try:
            net = re.search(r"on (.*?) ", r).group(1)
        except AttributeError:
            net = "unknown"
        device = {
            "ip": ip,
            "mac": mac,
            "net": net
        }
        devices.append(device)
    return devices
