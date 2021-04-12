import os
from deprecated import deprecated

@deprecated(version='0.2.1', reason='The class is merged into adb.py_auto_play')
class Devices:
    """A broker for devices.

    Attributes:

    """
    def get_devices(self):
        device_list = []
        adb_devices = os.popen("adb devices")
        cmd_output = adb_devices.read()

        print(cmd_output)

        raw_devices_list = []
        for line in cmd_output.splitlines():
            if line.endswith("device"):
                raw_devices_list.append(line)

        for device_index in range(len(raw_devices_list)):
            device = raw_devices_list[device_index]
            device_list.append(device[0:device.find('\t')])

        return device_list
