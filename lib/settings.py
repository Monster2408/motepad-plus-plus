from tkinter.filedialog import asksaveasfile
import yaml
import os
import shutil
import codecs
import sys

INITIAL_VALUE = "INITIAL_VALUE"

SETTINGS_VALUE = {
    "language": INITIAL_VALUE
}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("./resources/"), relative_path)

def checkUserFile(filename: str):
    if not os.path.exists("./user/"):
        os.mkdir("./user/")
    if not os.path.exists(f"./user/{filename}"):
        shutil.copyfile(resource_path(f"{filename}"), f"./user/{filename}")

def updateOption(key: str, value: str):
    checkUserFile('options.yml')
    with open('./user/options.yml', 'r') as file:
        obj = yaml.safe_load(file)
    obj[f'{key}'] = value
    SETTINGS_VALUE[f'{key}'] = value
    with codecs.open('./user/options.yml', 'w', 'utf-8') as file:
        yaml.dump(obj, file, encoding='utf-8', allow_unicode=True)

def get(key: str) -> str:
    checkUserFile('options.yml')
    global SETTINGS_VALUE
    if not SETTINGS_VALUE[f'{key}']:
        return None
    if SETTINGS_VALUE[f'{key}'] == INITIAL_VALUE:
        with open('./user/options.yml', 'r') as file:
            obj = yaml.safe_load(file)
            if not obj[f'{key}']:
                return None
            SETTINGS_VALUE[f'{key}'] = obj[f'{key}']
    return SETTINGS_VALUE[f'{key}']

def getLang() -> str:
    return get("language")