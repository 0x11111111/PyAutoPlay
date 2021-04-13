__version__ = '0.2.1'
from deprecated import deprecated

import platform
import time
# from matplotlib import pyplot as plt


from demo.arknights_assistant import Arknights


@deprecated(version='0.2.1', reason='The classes used have been merged into adb.py_auto_play')
def main():

    template_name = Arknights.template_name
    finish = Arknights.finish
    precondition = Arknights.precondition
    status = {
        "interval": 3,
        "captured": False,
        "recognized": False,
        "finish": finish,
        "times": 0,
        "rounds": 0
    }

    platform_info = platform.system()

    devices_broker = Devices()
    recognition_broker = Recognition(template_name, precondition)

    specific_device = None
    while not specific_device:
        devices_list = devices_broker.get_devices()

        if len(devices_list) == 1:
            specific_device = devices_list[0]

        elif len(devices_list) > 1:
            for device in devices_list:
                print(device)

            input_device = input("Please specify a device(abbreviation allowed):")
            for device in devices_list:
                if device.startswith(input_device):
                    specific_device = device

            if not specific_device:
                print("No devices matched.")

        elif len(devices_list) == 0:
            print("No devices detected. Please retry.")
            input()

    rounds = int(input("Input rounds:"))
    status["rounds"] = rounds

    while True:
        time.sleep(status["interval"])
        screencap_broker = Screencap(platform_info, specific_device)
        tap_broker = SendTap(specific_device)
        if (status["recognized"], status["captured"]) == (False, False):
            while not (captured := screencap_broker.screencap()):
                continue

            status["captured"] = True
            status["ratio"] = captured["ratio"]

            recognition_res = recognition_broker.recognize(captured["path"])
            if not recognition_res:
                status["recognized"] = False
                status["captured"] = False
                continue

            else:
                print(recognition_res)
                if "precondition" not in recognition_res or recognition_res["precondition"]:
                    status["recognized"] = True

                else:
                    status["recognized"] = False
                    status["captured"] = False
                    print(recognition_res["warning"])

            if status["recognized"]:
                recognized_position = recognition_res["position"]
                recognized_ratio = status["ratio"]
                if recognition_res["template"] == status["finish"]:
                    status["times"] += 1

                if recognized_ratio != 1:
                    tap_position = (int(recognized_position[0] * recognized_ratio),
                                    int(recognized_position[1] * recognized_ratio))

                else:
                    tap_position = recognized_position

                print(tap_position)
                tap_broker.tap(tap_position)

                status["recognized"] = False
                status["captured"] = False

                if status["rounds"] == status["times"]:
                    break

    input("Fin.")


if __name__ == '__main__':
    main()
