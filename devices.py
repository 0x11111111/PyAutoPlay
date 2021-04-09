import os


class Devices:
    def get_devices(self):
        device_list = []
        adb_devices = os.popen("adb devices")
        cmd_output = adb_devices.read()

        raw_devices_list = []
        for line in cmd_output.splitlines():
            raw_devices_list.append(line)

        for device_index in range(1, len(raw_devices_list) - 1):
            device = raw_devices_list[device_index]
            device_list.append(device[0:device.find('\t')])

        return device_list
