"""
# bluetooth low energy scan
from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
"""

from __future__ import print_function
import pygatt.backends

# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.BGAPIBackend()

try:
    adapter.start()
    device = adapter.connect('FF:3C:8F:22:C9:C8')
    value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b")
finally:
    adapter.stop()

"""
from bluepy import btle

print("Connecting...")
dev = btle.Peripheral("FF:3C:8F:22:C9:C8", "random")

for svc in dev.services:
    print(str(svc))
"""
