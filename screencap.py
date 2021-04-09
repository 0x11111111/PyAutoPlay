import os
import cv2
import numpy as np


class Screencap:

    def __init__(self, platform_info, specific_device):
        self.platform_info = platform_info
        self.specific_device = specific_device
        self.tmp_path = ".\\tmp\\"
        self.pic_name = "screencap.png"

        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)

    def screencap(self):

        os.system("adb -s {} exec-out screencap -p > {}".format(self.specific_device, self.tmp_path + self.pic_name))

        if self.platform_info == "Windows":
            self.__convert_img()

        if os.path.exists(self.tmp_path + self.pic_name):
            return self.tmp_path + self.pic_name

        else:
            return None

    def __convert_img(self):

        with open(self.tmp_path + self.pic_name, "rb") as f:
            original_pic = f.read()

        converted_pic = original_pic.replace(b"\r\n", b"\n")

        with open(self.tmp_path + self.pic_name, "wb") as f:
            f.write(converted_pic)

        f.close()
