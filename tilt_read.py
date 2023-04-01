#!/usr/bin/env python3

import pydbus
import time

# Set the MAC address of your Tilt hydrometer
tilt_mac_address = "D0:73:3D:6A:48:C5"

# Create a D-Bus proxy object for the Tilt hydrometer's BLE device
bus = pydbus.SystemBus()
tilt_device = bus.get("org.bluez", f"/org/bluez/hci0/dev_{tilt_mac_address.replace(':', '_')}")

# Enable notifications for the Tilt hydrometer's characteristic value changes
tilt_service_uuid = "A495BB50C5B14B44B5121370F02D74DE"
tilt_characteristic_uuid = "A495BB50C5B14B44B5121370F02D74DE"
tilt_service = tilt_device.GetService(tilt_service_uuid)
tilt_characteristic = tilt_service.GetCharacteristic(tilt_characteristic_uuid)
tilt_characteristic.StartNotify()

# Listen for broadcasts from the Tilt hydrometer and print the characteristic values
while True:
    value = bytearray(tilt_characteristic.ReadValue({}))
    color = value[2]
    temperature = int.from_bytes(value[4:6], byteorder="little") / 100.0
    gravity = int.from_bytes(value[6:8], byteorder="little") / 1000.0
    print(f"Color: {color}, Temperature: {temperature}, Gravity: {gravity}")
    time.sleep(1)
