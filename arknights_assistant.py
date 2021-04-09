import os
import platform
import cv2
import numpy as np
from matplotlib import pyplot as plt

from screencap import Screencap
from devices import Devices


def main():

    platform_info = platform.system()

    template_path = ".\\template\\"
    test = "mission_start.png"
    template_name = [test]
    template_dict = {}

    for template in template_name:
        template_full_path = template_path + template_name[0]
        template_dict[template] = cv2.imread(template_full_path, 1)

    devices_broker = Devices()
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

    cap = Screencap(platform_info, specific_device)
    captured = cap.screencap()

    if captured:
        print(captured)
        img = cv2.imread(captured, 1)
        width, height, _= template_dict[test].shape[::]

        recognition_res = cv2.matchTemplate(img, template_dict[test], eval("cv2.TM_CCOEFF_NORMED"))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(recognition_res)

        top_left = max_loc
        confidence = max_val
        bottom_right = (top_left[0] + height, top_left[1] + width)

        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        plt.imshow(img, cmap = 'gray')

        plt.show()

        print(top_left)
        print(bottom_right)
        print("confidence = {}".format(confidence))

    input()
