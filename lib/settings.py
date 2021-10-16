from tkinter.filedialog import asksaveasfile
import yaml
import os
import shutil
import codecs

INITIAL_VALUE = "INITIAL_VALUE"

SETTINGS_LANG_KEY = "LANG"
SETTINGS_LANG = INITIAL_VALUE

def updateOption(key: str, value: str):

    if not os.path.exists('./user/options.yml'):
        shutil.copyfile("./resources/options.yml", "./user/options.yml")
    with open('./user/options.yml', 'r') as file:
        obj = yaml.safe_load(file)
    obj[f'{key}'] = value
    with codecs.open('./user/options.yml', 'w', 'utf-8') as file:
        yaml.dump(obj, file, encoding='utf-8', allow_unicode=True)

def get(key: str):
    if not os.path.exists('./user/options.yml'):
        shutil.copyfile("./resources/options.yml", "./user/options.yml")
    with open('./user/options.yml', 'r') as file:
        obj = yaml.safe_load(file)
        if not obj[f'{key}']:
            return 'null'
        return obj[f'{key}']