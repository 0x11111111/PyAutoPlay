import os
import time
import sys
import re
import logging
from arknights_assistant import Arknights
from pap_adb import PyAutoPlay_adb


__version__ = '0.4.2'


def main():
    print('初始化中。请稍等。')
    working_path = os.path.dirname(os.path.abspath(__file__))
    adb_path = working_path + '\\adb.exe'
    template_name = Arknights.template_name
    finish = Arknights.finish
    precondition = Arknights.precondition
    special_action = Arknights.special_action
    status = {
        "interval": 3,
        "captured": False,
        "recognized": False,
        "finish": finish,
        "times": 0,
        "rounds": 0
    }

    log_directory_path = working_path + '\\..\\log\\'
    if not os.path.exists(log_directory_path):
        os.mkdir(log_directory_path)
    log_path = log_directory_path + 'main_log_' + str(os.getpid()) + '.log'
    # Create logger
    logger = logging.getLogger('py_auto_play_adb_main')
    logger.setLevel(logging.DEBUG)
    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('Working path: {}'.format(working_path))
    logger.info('Adb path: {}'.format(adb_path))
    pap = PyAutoPlay_adb(template_name,
                         precondition,
                         adb_path=adb_path,
                         template_path=working_path+'\\..\\adb\\template\\',
                         tmp_path=working_path+'\\..\\adb\\tmp\\')
    specific_device = None
    while not specific_device:
        devices_dict = pap.get_all_title_id()

        if len(devices_dict) == 1:
            print('是该设备吗？回车继续，否则请输入模拟器adb调试端口号: ')
            for k, v in devices_dict.items():
                print('描述:{} 设备id:{}'.format(k, v))

            ans = input()
            if re.match('^\d+$', ans):
                port_number = int(ans)
                pap.set_port(port_number)

            else:
                for k, v in devices_dict.items():
                    specific_device = v

        elif len(devices_dict) > 1:
            for k, v in devices_dict.items():
                print('描述:{} 设备id:{}'.format(k, v))

            input_device = input('请指定一个设备id(允许缩写):')
            logger.info('Input device: {}'.format(input_device))
            for k, v in devices_dict.items():
                if v.startswith(input_device):
                    specific_device = v

            if not specific_device:
                print('未匹配到设备。请重试或直接输入模拟器adb调试端口号: ')
                ans = input()
                if re.match('^\d+$', ans):
                    port_number = int(ans)
                    pap.set_port(port_number)

        elif len(devices_dict) == 0:
            print('未匹配到设备。请重试或直接输入模拟器adb调试端口号: ')
            ans = input()
            if re.match('^\d+$', ans):
                port_number = int(ans)
                pap.set_port(port_number)

    pap.set_id(specific_device)

    rounds = None
    while not rounds:
        round_input = input('请输入轮数:')
        logger.info('Input rounds: {}'.format(round_input))
        number_pattern = re.compile('^\d+$')
        expression_pattern = re.compile('^\d+/{1,2}\d+$')
        if re.match(number_pattern, round_input):
            rounds = int(round_input)

        elif re.match(expression_pattern, round_input):
            rounds = int(eval(round_input))
    status['rounds'] = rounds

    while True:
        time.sleep(status['interval'])

        if (status['recognized'], status['captured']) == (False, False):
            captured = pap.get_screenshot()
            while not (captured):
                captured = pap.get_screenshot()
                continue

            status['captured'] = True
            status['ratio'] = pap.ratio

            recognition_res = pap.recognize(captured)
            if not recognition_res:
                status['recognized'] = False
                status['captured'] = False
                continue

            else:
                print(recognition_res)
                logger.info(recognition_res)

                if 'precondition' not in recognition_res or recognition_res['precondition']:
                    status['recognized'] = True

                else:
                    status['recognized'] = False
                    status['captured'] = False
                    print(recognition_res["warning"])

            if status['recognized']:
                recognized_position = recognition_res['position']
                recognized_ratio = status['ratio']
                if recognition_res['template'] == status['finish']:
                    status['times'] += 1
                    print('剩余轮数: {}'.format(status['times']))

                if recognized_ratio != 1:
                    tap_position = (int(recognized_position[0] * recognized_ratio),
                                    int(recognized_position[1] * recognized_ratio))

                else:
                    tap_position = recognized_position

                special = recognition_res['template']
                if special in special_action:
                    pap.send_action(tap_position, special_action[special])
                else:
                    pap.send_action(tap_position)

                status['recognized'] = False
                status['captured'] = False

                if status['rounds'] == status['times']:
                    break

    # Remove the log file.
    fh.close()
    ch.close()
    if os.path.exists(log_path):
        os.remove(log_path)

    input('Fin.')


if __name__ == '__main__':
    main()
