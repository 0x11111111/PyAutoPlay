import os
import time
import platform
from PIL import Image
import cv2
import numpy as np
from typing import Union, Optional


class PyAutoPlay_adb():
    """This is the main class of PyAutoPlay containing most of the utilities interacting with window content and user.

    The instance of this class serves as a broker to handle screenshot, resize, conversion, recognition and
        implementation of actions.

    Attributes:
        hwnd (str): A str indicating the device identity.
        title (str): The title of window.
        platform_info (str): Differentiate from Windows and Linux platforms.
        ratio (double): Ratio is set to height of original picture to standard one's. It is used to resize and
            relocation.
        template_name (list): A list containing the pictures to be recognized. The pictures are provided in str of their
            file name and will be called by cv2.imread() to form templates.
        template_path (str): A str indicating the path of template pictures.
        tmp_path (str): A str indicating the path of temporary directory, which stores the temporary pictures captured.
        img_type (str): A str indicating the format of pictures processed. Default and recommendation is 'PNG'.
        std_height (int): A int representing the standard height of picture to be processed. The value is related with
            the height of template original picture's full size. Because this program can handle with pictures from
            different devices with unique size, it need a height as a standard in which all the pictures processed are
            resized to it. We recommend the height of the picture which the templates are cropped from.
        precondition (list): A list storing the preconditions required to be satisfied when an event is detected.
            The records are stored in an individual dict.
            [
                {
                    'event': (str): If the event is detected and needs to perform an action before its precondition is
                        satisfied. For example, we need to check an agreement before we continue to perform actions.
                        The check of agreement is the precondition of the actions performing. The 'event' is given by
                        its file name and should be included in template_name list and located in template_path.
                    'precondition': (str): The precondition to be satisfied initially. Given by its file name and
                        required to be located in template_path.
                    'warning': (str): If the precondition failed to be satisfied, a warning will be issued and uttered
                        via the result of recognition.
                }
            ]
    """
    def __init__(self, template_name, precondition, template_path='..\\adb\\template\\', tmp_path='..\\adb\\tmp\\',
                 img_type='PNG', std_height=810):
        self.hwnd = None
        self.title = ''
        self.platform_info = platform.system()
        self.ratio = 1
        self.template_name = template_name
        self.template_path = template_path
        self.tmp_path = tmp_path
        self.img_type = img_type
        self.std_height = std_height
        self.precondition = precondition

        self.__template_dict = dict()
        self.__precondition_dict = dict()

        os.system('adb devices')

        # Generate the templates stored in __template_dict.
        for template in self.template_name:
            template_full_path = self.template_path + template
            self.__template_dict[template] = cv2.imread(template_full_path, cv2.IMREAD_COLOR)

        # Traverse the list of precondition and fetch the record dict. Then generate the binding information in
        # __precondition_dict.
        for record in self.precondition:
            template_full_path = self.template_path + record['precondition']
            if not record['event'] in self.__precondition_dict:
                self.__precondition_dict[record['event']] = [{'template': cv2.imread(template_full_path, 1),
                                                          'warning': record['warning']}]

            else:
                self.__precondition_dict[record['event']] += {'template': cv2.imread(template_full_path, 1),
                                                          'warning': record['warning']}

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

        # Pid is used to distinguish from different threads.
        screenshot_path = self.tmp_path + 'screenshot_' + str(os.getpid()) + '.' + self.img_type.lower()
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
                    'precondition': (bool): Only occurs when the image in template is also included in
                        precondition['event']. True if the condition is satisfied and false otherwise.
                    'warning': (list): Only occurs when the image in template is also included in precondition['event'].
                        If satisfied, value is a an empty list and if not, a list including warning information in
                        precondition['warning'] is provided.
                    'template': (str): The name of the template detected.
                    'position': (tuple):((int, int), (int, int)) A rectangular area defined by its left top and bottom
                        right coordination. Mind that the coordination is matched to the resized picture and need to be
                        relocated according to self.ratio.
                    'confidence': (double): The extent to which the template matches the certain target in screenshot.
                        Usually values over 0.97 if a match is detected.
                }
        """
        im = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        image.close()
        recognition_res_dict = dict()
        
        for template_name in self.template_name:
            template = self.__template_dict[template_name]
            width, height, _ = template.shape[::]
            
            tmp_recognition_res = cv2.matchTemplate(im, template, eval('cv2.TM_CCOEFF_NORMED'))
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(tmp_recognition_res)
            top_left = max_loc
            confidence = max_val

            # confidence is used to identify if the a certain picture in templates is recognized.
            if confidence < 0.9:
                continue
            
            else:
                if template_name in self.__precondition_dict:
                    recognition_res_dict['precondition'] = True
                    recognition_res_dict['warning'] = []
                    for precondition in self.__precondition_dict[template_name]:
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

