# -*- coding: utf-8 -*-
# @author: leesoar

"""Raspberry Pi"""

import os
import re


MAC_ADDR_PREFIX = [
    "B8:27:EB",
    "DC:A6:32",
    "E4:5F:01",
]


def get_raspberry_pi():
    command = f"""arp -na | grep -i -E '{"|".join(MAC_ADDR_PREFIX)}'"""
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
        net = re.search(r"on (.*?) ", r).group(1)
        device = {
            "ip": ip,
            "mac": mac,
            "net": net
        }
        devices.append(device)
    return devices
