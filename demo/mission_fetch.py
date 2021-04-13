from adb import PyAutoPlay
import time

def main():

    template_name = ['fetch.png', 'weekly.png', 'fetched.png']
    finish = None
    precondition = [{'event': 'weekly.png', 'precondition': 'daily_cleared.png', 'warning': 'Fetching daily.'}]
    special_action = {}
    status = {
        "interval": 1,
        "captured": False,
        "recognized": False,
        "finish": finish,
        "times": 0,
        "rounds": 0
    }

    pap = PyAutoPlay(template_name, precondition, '..\\adb\\mission_fetch_template\\', '..\\adb\\tmp\\')
    specific_device = None
    while not specific_device:
        devices_dict = pap.get_all_hwnd_title()

        if len(devices_dict) == 1:
            for k, v in devices_dict.items():
                specific_device = k

        elif len(devices_dict) > 1:
            for k, v in devices_dict.items():
                print("Devices:{} Description:{}".format(k, v))

            input_device = input("Please specify a device(abbreviation allowed):")
            for k, v in devices_dict.items():
                if k.startswith(input_device):
                    specific_device = k

            if not specific_device:
                print("No devices matched.")

        elif len(devices_dict) == 0:
            print("No devices detected. Please retry.")
            input()

    pap.set_hwnd(specific_device)
    rounds = int(input("Input rounds:"))
    status["rounds"] = rounds

    while True:
        time.sleep(status["interval"])

        if (status["recognized"], status["captured"]) == (False, False):
            while not (captured := pap.get_screenshot()):
                continue

            status["captured"] = True
            status["ratio"] = pap.ratio

            recognition_res = pap.recognize(captured)
            if not recognition_res:
                status["recognized"] = False
                status["captured"] = False
                continue

            else:
                print(recognition_res)
                if "precondition" not in recognition_res or recognition_res["precondition"]:
                    status["recognized"] = True

                else:
                    status["recognized"] = False
                    status["captured"] = False
                    print(recognition_res["warning"])

            if status["recognized"]:
                recognized_position = recognition_res["position"]
                recognized_ratio = status["ratio"]
                if recognition_res["template"] == status["finish"]:
                    status["times"] += 1

                if recognized_ratio != 1:
                    tap_position = (int(recognized_position[0] * recognized_ratio),
                                    int(recognized_position[1] * recognized_ratio))

                else:
                    tap_position = recognized_position

                if (special := recognition_res['template']) in special_action:
                    pap.send_action((), special_action[special])
                else:
                    pap.send_action(tap_position)

                status["recognized"] = False
                status["captured"] = False

                if status["rounds"] == status["times"]:
                    break

    input("Fin.")


main()
