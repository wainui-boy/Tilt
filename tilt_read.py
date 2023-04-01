#!/usr/bin/env python3

import subprocess

# Set the MAC address of your Tilt hydrometer
tilt_mac_address = "XX:XX:XX:XX:XX:XX"

# Turn on Bluetooth
subprocess.call("sudo hciconfig hci0 up", shell=True)

# Start scanning for nearby Bluetooth LE devices in the background
subprocess.Popen("sudo hcitool lescan > /dev/null 2>&1 &", shell=True)

# Listen for broadcasts from the Tilt hydrometer
subprocess.call(f"sudo hcitool lecc {tilt_mac_address}", shell=True)
subprocess.call(f"sudo hcitool ledc {tilt_mac_address} 0x0000", shell=True)
tilt_output = subprocess.Popen("sudo hcidump --raw", stdout=subprocess.PIPE)

# Parse the Tilt hydrometer's data from the broadcast output
for line in iter(tilt_output.stdout.readline, b''):
    line = line.decode("utf-8").strip()
    if "handle" in line and "value" in line:
        handle, value = line.split(": ")
        if handle == "handle 0x0014,":
            # Extract the color, temperature, and gravity values from the broadcast data
            color = int(value[6:8], 16)
            temperature = int(value[10:14], 16) / 100.0
            gravity = int(value[14:18], 16) / 1000.0
            
            # Do something with the data (e.g., print it to the console)
            print(f"Color: {color}, Temperature: {temperature}, Gravity: {gravity}")

