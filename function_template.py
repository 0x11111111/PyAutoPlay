# 测试用函数模板
from PIL import Image
from typing import Union, Optional, Any, Tuple


# windows only!
def position(x: Union[int, None] = None, y: Optional[int, None] = None) -> tuple:
    """返回当前指针的坐标.
    如果指定坐标(可选), 则会覆盖返回的坐标.

    Args:
        x: x的坐标(可选)
        y: y的坐标(可选)
    Returns:
        (x,y) (tuple) :坐标
    """
    return (x, y)


def get_screen_size() -> Tuple:
    """返回屏幕大小

    Returns:
        (x,y) (tuple) :屏幕大小
    """
    return


def get_screenshot(x1=None, y1=None, x2=None, y2=None, id=self.id) -> Image.Image:
    """获得指定区域的截图, windows下默认返回应用截图, adb下默认返回全屏截图

    Args:
        x1 (int): 起始点x轴坐标
        y1 (int): 起始点y轴坐标
        x2 (int): 终止点y轴坐标
        y2 (int): 终止点y轴坐标
        id (adb: str): 默认为set_id函数指定的设备号/句柄号, 如给定则试图对指定设备/进程截图.


    Returns:
        Image.Image: 指定区域内的截图
    """
    return 

# windows only!
def get_full_screenshot() -> Image.Image:
    """返回全屏截图。

    Returns:
        Image.Image: 对adb来说即为设备显示画面全屏截图
    """
    return


def get_all_title_id() -> dict:
    """获取进程句柄/设备序列号与标题。
    windows: 获取所有非空的句柄标题(str)与句柄(int)和的键值对.
    adb: 获取所有连接的设备属性名(str)与安卓设备的序列号(str). 属性名位于ro.build.id词条下.

    Returns:
        adb (dict): 包含设备名称和设备序列号的字典, 分别为一对键值对.
        windows (dict): 包含句柄标题与句柄的字典, 分别为一对键值对.
    """
    return 114514


def set_id(id) -> bool:
    """将该进程进行操作的id指定为给定id.

    Args:
        id (adb: str): 给定的设备序列号.
        id (windows: int): 给定进程的句柄号.

    Returns:
        bool: 是否指定成功

    """
    return 114514


def sleep(_time):
    """封装time.sleep()函数。

    Args:
        _time (int): 休眠的秒数
    """

    return


def recognize(self, image) -> dict:
    """识别给定image中模板是否出现，将结果保存在字典中返回。

    Args:
        image (Image.Image): 待识别程序截图。

    Returns:
        dict: 识别结果。
            {
                'precondition': (bool): 只有模板出现在字典项precondition['event']中才会出现该键。 条件满足则为True，否则为False。
                'warning': (list): 只有模板出现在字典项precondition['event']中才会出现该键。如果先决条件满足，值为空列表，否则值为precondition['warning']字典项warning信息的列表.
                'template': (str): 识别到的模板名称.
                'position': (tuple): ((int, int), (int, int)) 由左上坐标与右下坐标确定的一块矩形区域。 注意坐标值与调整大小后的图片中位置相对应，若要确定程序源位置要依据self.ratio做调整。
                adb: 'confidence': (double): 截屏中识别到模板的置信程度。通常大于0.97。
            }
    """
    return


def click(position_) ->None:
    """


key_dict = {
    
    "action": {
    "x": "1024", "y": "1024",
    }
}

def send_key(x, y, key, interval, times, **k) -> None:
    """对指定位置发送按键.
    """

    return 0