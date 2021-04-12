import os
import time
import platform
from PIL import Image
import cv2
import numpy as np

class PyAutoPlay():
    """
    A class that handles most features of PyAutoPlay.

    Attributes
    ----------
    template_name: list
        A list containing all of the names of the pictures that required to be recognized, which all have their certain
         actions to be taken.
    precondition: list
        A list containing dict, each of which implies a 'precondition' is needed to be satisfied on a certain 'event'
         and if not the case, a 'warning' will be sent.

    """
    def __init__(self, template_name, precondition):
        self.img_type = 'PNG'
        self.std_height = 810
        self.hwnd = None
        self.title = ''
        self.platform_info = platform.system()
        self.tmp_path = '.\\adb\\tmp\\'
        self.ratio = 1
        self.template_path = '.\\adb\\template\\'
        self.template_name = template_name
        self.template_dict = dict()
        self.precondition = precondition
        self.precondition_dict = dict()

        os.system('adb devices')

        for template in self.template_name:
            template_full_path = self.template_path + template
            self.template_dict[template] = cv2.imread(template_full_path, cv2.IMREAD_COLOR)
            
        for bind in self.precondition:
            template_full_path = self.template_path + bind['precondition']
            if not bind['event'] in self.precondition_dict:
                self.precondition_dict[bind['event']] = [{"template": cv2.imread(template_full_path, 1),
                                                          "warning": bind["warning"]}]

            else:
                self.precondition_dict[bind["event"]] += {"template": cv2.imread(template_full_path, 1),
                                                          "warning": bind["warning"]}


    def get_all_hwnd_title(self) -> dict:
        hwnd_title = dict()
        device_list = []
        get_devices = os.popen('adb devices')
        cmd_output = get_devices.read()

        for line in cmd_output.splitlines():
            if line.endswith('device'):
                device_list.append(line[:line.find('\t')])

        for device in device_list:
            get_titles = os.popen('adb -s {} shell getprop ro.build.id'.format(device))
            title = get_titles.read().strip()
            hwnd_title[device] = title

        return hwnd_title

    def set_hwnd(self, hwnd):
        self.hwnd = hwnd

    def sleep(self, _time):
        time.sleep(_time)

    def get_screenshot(self) -> Image.Image:
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)

        screenshot_path = self.tmp_path + 'screenshot.' + self.img_type.lower()
        os.system('adb -s {} exec-out screencap -p > {}'.format(self.hwnd, screenshot_path))

        if self.platform_info == 'Windows':
            with open(screenshot_path, 'rb') as f:
                original_pic = f.read()
            converted_pic = original_pic.replace(b'\r\n', b'\n')
            with open(screenshot_path, 'wb') as f:
                f.write(converted_pic)
            f.close()

        im = Image.open(screenshot_path)
        original_size = im.size
        if original_size[1] == self.std_height:
            self.ratio = 1

        else:
            self.ratio = original_size[1] / self.std_height
            converted_size = (int(original_size[0] / self.ratio), int(original_size[1] / self.ratio))
            im = im.resize(converted_size)

            im.save(screenshot_path, self.img_type)

        return im


    def recognize(self, image) -> dict:

        im = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        image.close()
        recognition_res_dict = dict()
        
        for template_name in self.template_name:
            template = self.template_dict[template_name]
            width, height, _ = template.shape[::]
            
            tmp_recognition_res = cv2.matchTemplate(im, template, eval('cv2.TM_CCOEFF_NORMED'))
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(tmp_recognition_res)
            top_left = max_loc
            confidence = max_val
            
            if confidence < 0.9:
                continue
            
            else:
                if template_name in self.precondition_dict:
                    recognition_res_dict["precondition"] = True
                    recognition_res_dict["warning"] = []
                    for precondition in self.precondition_dict[template_name]:
                        tmp_precondition_res = cv2.matchTemplate(im, precondition["template"], eval("cv2.TM_CCOEFF_NORMED"))
                        _, max_val, _, _ = cv2.minMaxLoc(tmp_precondition_res)

                    if max_val > 0.9:
                        pass

                    else:
                        recognition_res_dict["precondition"] = False
                        recognition_res_dict["warning"].append(precondition["warning"])

                bottom_right = (top_left[0] + height, top_left[1] + width)
                recognition_res_dict["template"] = template_name
                recognition_res_dict["position"] = ((top_left[0] + bottom_right[0]) // 2,
                                                    (top_left[1] + bottom_right[1]) // 2)
                recognition_res_dict["confidence"] = confidence

            return recognition_res_dict

    def send_action(self, position, action=None, delay=0):

        if delay:
            self.sleep(delay)

        if action is None:
            os.system("adb -s {} shell input tap {} {}".format(self.hwnd, position[0], position[1]))

        else:
            if not action[0]:
                if action[1]:
                    self.sleep(action[1])

            elif action[0] == 'click':
                if action[1]:
                    self.sleep(action[1])

                position = [action[3][0], action[3][1]]
                for i in range(action[2]):
                    os.system("adb -s {} shell input tap {} {}".format(self.hwnd, position[0], position[1]))


