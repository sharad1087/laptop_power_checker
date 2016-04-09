import json
import pyudev

# Initialize a list to capture power devices
powerDevices = []

# Initialize a udev context
context = pyudev.Context()

# Get all power supply devices
for powerDevice in context.list_devices(subsystem='power_supply'):
    powerDevices.append(powerDevice)

# Initialize a variable to store information about main and battery, as power supply sources
powerDeviceInfo = {
                   'mains':
                      {
                       'attributes': ['online'],
                       'devices': {}
                      }, 
                   'battery':
                      {
                       'attributes': ['status'],
                       'devices': {}
                      } 
                  }

for powerDevice in powerDevices:
    powerDeviceType = powerDevice.attributes.get('type')
    if powerDeviceType is None:
        continue
    powerDeviceType = powerDeviceType.decode().lower()
    if powerDeviceType not in powerDeviceInfo:
        continue
    attributes = powerDeviceInfo.get(powerDeviceType).get('attributes')
    powerInfo = []
    for attribute in attributes:
        attributeValue = powerDevice.attributes.get(attribute)
        if attributeValue:
            powerInfo.append(attributeValue.decode())
    deviceIndex = len(powerDeviceInfo.get(powerDeviceType).get('devices')) + 1
    powerDeviceInfo.get(powerDeviceType).get('devices')['{}'.format(deviceIndex)] = powerInfo
print(json.dumps(powerDeviceInfo, indent=2))
