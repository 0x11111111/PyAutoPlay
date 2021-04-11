import os
import time


class SendTap:
    """A broker for events like sending taps.

    Attribute:
        specific_device:

    """
    def __init__(self, specific_device):
        self.specific_device = specific_device

    def tap(self, position, delay=0):
        if delay:
            time.sleep(delay)

        os.system("adb -s {} shell input tap {} {}".format(self.specific_device, position[0], position[1]))
