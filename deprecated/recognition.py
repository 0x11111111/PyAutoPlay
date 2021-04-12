import cv2
from deprecated import deprecated


@deprecated(version='0.2.1', reason='The class is merged into adb.py_auto_play')
class Recognition:
    """A broker for game status recognition.

    Attribute:
        template_name:
        precondition:

    """
    def __init__(self, template_name, precondition):

        self.template_path = "../adb/template\\"
        self.template_name = template_name
        self.template_dict = {}
        self.precondition_dict = {}

        for template in self.template_name:
            template_full_path = self.template_path + template
            self.template_dict[template] = cv2.imread(template_full_path, 1)

        for bind in precondition:
            template_full_path = self.template_path + bind["precondition"]
            if not bind["event"] in self.precondition_dict:
                self.precondition_dict[bind["event"]] = [{"template": cv2.imread(template_full_path, 1),
                                                          "warning": bind["warning"]}]

            else:
                self.precondition_dict[bind["event"]] += {"template": cv2.imread(template_full_path, 1),
                                                          "warning": bind["warning"]}

    def recognize(self, pic_path):

        img = cv2.imread(pic_path, 1)
        recognition_res_dict = {}

        for template_name in self.template_name:
            template = self.template_dict[template_name]
            width, height, _ = template.shape[::]

            tmp_recognition_res = cv2.matchTemplate(img, template, eval("cv2.TM_CCOEFF_NORMED"))
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(tmp_recognition_res)
            top_left = max_loc
            confidence = max_val

            if confidence < 0.8:
                continue

            else:
                if template_name in self.precondition_dict:
                    recognition_res_dict["precondition"] = True
                    recognition_res_dict["warning"] = []
                    for precondition in self.precondition_dict[template_name]:
                        tmp_precondition_res = cv2.matchTemplate(img, precondition["template"], eval("cv2.TM_CCOEFF_NORMED"))
                        _, max_val, _, _ = cv2.minMaxLoc(tmp_precondition_res)

                    if max_val > 0.8:
                        recognition_res_dict["precondition"] = recognition_res_dict["precondition"]

                    else:
                        recognition_res_dict["precondition"] = False
                        recognition_res_dict["warning"].append(precondition["warning"])

                bottom_right = (top_left[0] + height, top_left[1] + width)
                recognition_res_dict["template"] = template_name
                recognition_res_dict["position"] = ((top_left[0] + bottom_right[0]) // 2,
                                                    (top_left[1] + bottom_right[1]) // 2)
                recognition_res_dict["confidence"] = confidence

        return recognition_res_dict
