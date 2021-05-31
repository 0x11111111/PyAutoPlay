import platform
from PIL import Image
from typing import Optional, Literal
import logging

logger = logging.getLogger()
logger.setLevel('INFO')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('INFO')
logger.addHandler(chlr)
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

logger.info('py_auto_play_base_class')

import pyautogui

class BasePAP(object):
    def __init__(self,
                 platform:         Literal['windows', 'android'],
                 template_name:    str = None,
                 precondition:     dict = None,
                 img_type:         str = 'PNG',
                 template_path:    str = '',
                 std_height:       int = 810,
                 pre_read:         bool = False,
                 ):
        self.id = None
        self.title = ''
        self.radio = 1 
        self.template_name = template_name
        self.template_path = template_path
        self.img_type = img_type
        self.std_height = std_height
        
        self.__template_dict =dict()
        self.__precondition_dict = dict()

        logger.info('Initializing')

    def get_all_id_title(self) -> dict: ...
    def set_id(self, id: str) -> None: ...
    def sleep(self, time: float) -> None: ...
    def get_screenshot(self) -> Image.Image: ...
    def recongnize(self, image) -> dict: ...
    def send_action(self, position: tuple, action: str, delay=0): ...


def main():
    app = BasePAP(platform='windows')
    logger.info('main')


if __name__ == '__main__':
    main()
