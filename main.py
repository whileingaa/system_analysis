import psutil
import os
import json

_history_path = 'C:/Users/Public/assistent'

def get_status():
    ret = {'cpu_percent': psutil.cpu_percent()}
    return ret


###############################################################################
# history_list should be stored as:
# [
#   'id':'uuid'                       //uuid is generated bhy timestamp
# ]
# 
###############################################################################
def get_history_list():
    with open(os.path.join(_history_path, "list"), 'r') as f:
        ret = json.load(f)
    return ret


###############################################################################
# history should be stored as:
# {
#   'id':'uuid'                       //uuid is generated bhy timestamp
#   'content':json_content            //refer model we choose to define its format
# }
# 
###############################################################################
def get_history(id):
    with open(os.path.join(_history_path, id), 'r') as f:
        ret = json.load(f)
    return ret

def save_history(id, history):
    with open(os.path.join(_history_path, id), 'w') as f:
        json.dump(history, f)
    pass

def auto_advise(status):
    api = "exmaple"
    def model():
        pass
    prompt = "prompt"
    json_respone = model(api, prompt, format(status))
    return json_respone

def user_advise(status, user_input):
    api = "exmaple"
    def model():
        pass
    prompt = "prompt"
    json_respone = model(api, prompt, format(status, user_input))
    return json_respone

if __name__ == "__main__":
    print(get_status())