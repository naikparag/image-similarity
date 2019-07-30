import json
import config
import pickle


# JSON PERSIST
# --------------------

def save_as_json(path, obj):
    with open(config.MODEL_DIR + path, 'w') as f:
        json.dump(obj, f, ensure_ascii=False)


def get_from_json(path):
    return open(config.MODEL_DIR + path, 'r').read()


# PICKLE PERSIST
# --------------------

def save_to_file(path, obj):
    pickle.dump(obj, open(config.MODEL_DIR + path, 'wb'))


def get_from_file(path):
    return pickle.load(open(config.MODEL_DIR + path, 'rb'))
