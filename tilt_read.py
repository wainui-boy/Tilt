#!/usr/bin/env python3

from bluepy.btle import Scanner, DefaultDelegate
import argparse


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == args.mac and isNewData:
            for (adtype, desc, value) in dev.getScanData():
                if desc == 'Manufacturer':
                    temp = int(value[6:10], 16) / 100
                    gravity = int(value[10:14], 16) / 1000
                    print("Temperature: %.2f C" % temp)
                    print("Gravity: %.3f" % gravity)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mac", type=str, help="MAC address of Tilt Hydrometer")
    parser.add_argument("-t", "--timeout", type=int, default=10,
                        help="scan timeout in seconds (default: 10)")
    args = parser.parse_args()

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(args.timeout)