import os
import time
import platform
from PIL import Image
import cv2
import numpy as np


class PyAutoPlay():

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
                self.precondition_dict[bind['event']] = [{'template': cv2.imread(template_full_path, 1),
                                                          'warning': bind['warning']}]

            else:
                self.precondition_dict[bind['event']] += {'template': cv2.imread(template_full_path, 1),
                                                          'warning': bind['warning']}

    def get_all_hwnd_title(self) -> dict:
        """Obtain all the serial number and its name of devices.

        Returns:
            dict: A dict that holds both the serial number(str) and its name of devices.
        """
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
        """Set the Attribute self.hwnd to hwmd.

        Args:
            hwnd (str): a serial number of a device.

        Returns:
            None
        """
        self.hwnd = hwnd

    def sleep(self, _time):
        """Encapsulation of time.sleep().

        Args:
            _time (int): time to sleep in seconds.

        Returns:
            None
        """
        time.sleep(_time)

    def get_screenshot(self) -> Image.Image:
        """Get a screenshot from self.hwnd device and adapt it.

        The method will place the temporary image into self.tmp_path.
        The temporary image is converted if the platform is because of the nuances of '\r\n' and '\r'.
        After that, the image is resized according to self.std_height, by default, 810. Meanwhile self.ratio is set to
            height of original picture to standard one's.

        Returns:
            Image.Image: a image object to be recognized.
        """
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
        """A function that serves as recognizer between screenshots and template pictures.

        Args:
            image (Image.Image):

        Returns:
            dict: A result of recognition.
                {
                    'precondition': bool: Only occurs when the image in template is also included in
                        precondition['event']. True if the condition is satisfied and false otherwise.
                    'warning': list: Only occurs when the image in template is also included in precondition['event'].
                        If satisfied, value is a an empty list and if not, a list including warning information in
                        precondition['warning'] is provided.
                    'template': str: The name of the template detected.
                    'position': tuple:((int, int), (int, int)) A rectangular area defined by its left top and bottom
                        right coordination. Mind that the coordination is matched to the resized picture and need to be
                        relocated according to self.ratio.
                    'confidence': The extent to which the template matches the certain target in screenshot. Usually
                        values over 0.98 if a match is detected.
                }
        """
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

            # confidence is used to identify if the a certain picture in templates is recognized.
            if confidence < 0.9:
                continue
            
            else:
                if template_name in self.precondition_dict:
                    recognition_res_dict['precondition'] = True
                    recognition_res_dict['warning'] = []
                    for precondition in self.precondition_dict[template_name]:
                        tmp_precondition_res = cv2.matchTemplate(im, precondition['template'], 
                                                                 eval('cv2.TM_CCOEFF_NORMED'))
                        _, max_val, _, _ = cv2.minMaxLoc(tmp_precondition_res)

                    if max_val > 0.9:
                        pass

                    else:
                        recognition_res_dict['precondition'] = False
                        recognition_res_dict['warning'].append(precondition['warning'])

                bottom_right = (top_left[0] + height, top_left[1] + width)
                recognition_res_dict['template'] = template_name
                recognition_res_dict['position'] = ((top_left[0] + bottom_right[0]) // 2,
                                                    (top_left[1] + bottom_right[1]) // 2)
                recognition_res_dict['confidence'] = confidence

            return recognition_res_dict

    def send_action(self, position, action=None, delay=0):
        """Action to perform, by default a click on position after delay.

        Args:
            position (tuple): A coordination indicating the position to be tapped. Will be masked if position in
                action[3] is given.
            action (list): Special action(s) to be performed.
            delay (int): Time to sleep (now).

        Returns:
            None
        """
        if delay:
            self.sleep(delay)

        # Special action is by default None and only in this case a tap on position is sent directly.
        if action is None:
            os.system('adb -s {} shell input tap {} {}'.format(self.hwnd, position[0], position[1]))

        else:
            # If action[3](position) is especially designated and not equal to (0, 0),
            # the given position in parameter list will be shaded.
            if action[3] and not (action[3][0], action[3][1]) == (0, 0):
                position = action[3]

            # If action[0](key) is empty str, nothing will happen except for sleep delay.
            if not action[0]:
                if action[1]:
                    self.sleep(action[1])

            # If action[0](key) is 'click', a click will be sent following given action[1](delay) seconds.
            # The click
            elif action[0] == 'click':
                if action[1]:
                    self.sleep(action[1])

                for i in range(action[2]):
                    os.system('adb -s {} shell input tap {} {}'.format(self.hwnd, position[0], position[1]))
            # Completion in future.
            else:
                pass

