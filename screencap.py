import os
from PIL import Image
import cv2
import numpy as np


class Screencap:

    def __init__(self, platform_info, specific_device, std_height = 810):
        self.platform_info = platform_info
        self.specific_device = specific_device
        self.std_height = std_height
        self.captured_info = {}
        self.tmp_path = ".\\tmp\\"
        self.pic_name = "screencap.png"

        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)

    def screencap(self):

        os.system("adb -s {} exec-out screencap -p > {}".format(self.specific_device, self.tmp_path + self.pic_name))

        if self.platform_info == "Windows":
            self.__convert_img()

        size = self.__resize_img(self.std_height)
        if os.path.exists(self.tmp_path + self.pic_name):
            self.captured_info["path"] = self.tmp_path + self.pic_name

            return self.captured_info

        else:
            return None

    def __convert_img(self):

        with open(self.tmp_path + self.pic_name, "rb") as f:
            original_pic = f.read()

        converted_pic = original_pic.replace(b"\r\n", b"\n")

        with open(self.tmp_path + self.pic_name, "wb") as f:
            f.write(converted_pic)

        f.close()

    def __resize_img(self, std_height):

        img = Image.open(self.tmp_path + self.pic_name)
        current_size = img.size
        if current_size[1] == std_height:
            img.close()
            self.captured_info["ratio"] = 1
            self.captured_info["size"] = current_size

            return current_size

        ratio = current_size[1] / std_height
        self.captured_info["ratio"] = ratio
        modified_size = (int(current_size[0] / ratio), std_height)
        self.captured_info["size"] = modified_size
        img = img.resize(modified_size)

        img.save(self.tmp_path + self.pic_name, "PNG")
        img.close()

        return modified_size



