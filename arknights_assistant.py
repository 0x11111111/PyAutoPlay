
class Arknights:
    template_name = ["start.png", "mission_start.png", "brief.png", "results.png"]
    precondition = [{"event": "start.png", "precondition": "auto_deploy_on.png", "warning": "Auto deployed is "
                                                                                            "unchecked."}]
    finish = "results.png"
    status = {
        "interval": 3,
        "captured": False,
        "recognized": False,
        "finish": finish,
        "times": 0,
        "rounds": 0
    }
