

class Arknights:
    template_name = ['start.png', 'mission_start.png', 'under_control.png', 'brief.png', 'results.png']
    precondition = [{'event': 'start.png', 'precondition': 'auto_deploy_on.png', 'warning': 'Auto deployed is '
                                                                                      'unchecked.'}]
    special_action = {'under_control.png': ['', 0, 0, (0, 0)]}  # action, delay, repeat, position
    finish = 'results.png'

