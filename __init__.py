__version__ = "0.4.2"
import pyautogui
from pap_win32 import PyAutoPlay_windows
from pap_adb import PyAutoPlay_adb
import logging
from typing import Optional, Literal
from PIL import Image


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


def pyautoplay(platform:         Literal['windows', 'android'],
               template_name:    str = None,
               precondition:     dict = None,
               img_type:         str = 'PNG',
               template_path:    str = '',
               pre_read:         bool = False,
               ):
    prarms = dict()
    prarms['template_name'] = template_name
    prarms['precondition'] = precondition
    prarms['img_type'] = img_type
    prarms['template_path'] = template_path
    prarms['pre_read'] = pre_read
    if platform == 'windows':
        return PyAutoPlay_windows(prarms)
    elif platform == 'android':
        return PyAutoPlay_adb(prarms)


def main():
    app = pyautoplay(platform='windows')


if __name__ == '__main__':
    main()
