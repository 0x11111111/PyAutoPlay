# PyAutoPlay
# https://github.com/0x11111111/PyAutoPlay

__version__ = "0.4.2"
import pyautogui
import pixivpy3
import sys
from pap_win import PyAutoPlay_windows
from pap_adb import PyAutoPlay_adb
from utils import PAPException
import logging
from typing import Optional, Literal

if sys.platform not in ("win32", "Linux"):
    raise NotImplementedError("Your platform %s is not supported." % sys.platform)

try:
    import numpy
except ImportError:
    def _could_not_import_numpy():
        raise PAPException(
            "Can`t import numpy, please install numpy.")
    numpy = _could_not_import_numpy()

try:
    import cv2
except ImportError:
    def _could_not_import_cv2():   
        raise PAPException(
            "Can`t import opencv-python, please install opencv-python."
        )
    cv2 = _could_not_import_cv2()

def logger():
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
    return logger


logger = logger()

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    raise PAPException("PyAutoPlay doesn't support python version less than 3.5,\
 consider upgrading your python version.")


def pyautoplay(platform:         Literal['windows', 'android'],
               template_name:    str = None,
               template_path:    str = '',
               precondition:     dict = None,
               img_type:         str = 'PNG',
               pre_read:         bool = False,
               adb_path:         str = '',
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
        prarms['adb_path'] = adb_path
        return PyAutoPlay_adb(prarms)

def main():
    app = pyautoplay(platform='windows')
    print(app.img_type)


if __name__ == '__main__':
    main()
