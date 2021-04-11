import cv2


class Recognition:

    def __init__(self, template_name):

        self.template_path = ".\\template\\"
        self.template_name = template_name
        self.template_dict = {}

        for template in self.template_name:
            template_full_path = self.template_path + template
            self.template_dict[template] = cv2.imread(template_full_path, 1)

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

            # print("confidence = {}".format(confidence))

            if confidence < 0.8:
                continue

            else:
                bottom_right = (top_left[0] + height, top_left[1] + width)
                recognition_res_dict["template"] = template_name
                recognition_res_dict["position"] = ((top_left[0] + bottom_right[0]) // 2,
                                                    (top_left[1] + bottom_right[1]) // 2)
                recognition_res_dict["confidence"] = confidence

        return recognition_res_dict
