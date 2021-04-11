import os
import platform
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
from send_tap import SendTap
from screencap import Screencap
from devices import Devices
from recognition import Recognition

def main():

    status = {}
    status["recognizing"] = False
    status["captured"] = False
    status["recognized"] = False

    platform_info = platform.system()

    devices_broker = Devices()
    recognition_broker = Recognition()

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

    while True:
        time.sleep(3)
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
                status["recognized"] = True
                print(recognition_res)

            if status["recognized"] == True:
                recognized_position = recognition_res["position"]
                recognized_ratio = status["ratio"]

                if recognized_ratio != 1:
                    tap_position = (int(recognized_position[0] * recognized_ratio),
                                    int(recognized_position[1] * recognized_ratio))

                else:
                    tap_position = recognized_position

                print(tap_position)
                tap_broker.tap(tap_position)

                status["recognized"] = False
                status["captured"] = False


    input()
