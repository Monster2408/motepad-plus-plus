from lib import settings

LANGUAGE_DIST = {
    "LANG": {
        "JP": "日本語",
        "US": "English"
    },
    "TEXT_FILES": {
        "JP": "テキスト文書",
        "US": "Text Files"
    },
    "FILE": {
        "JP": "ファイル",
        "US": "Files"
    },
    "OPEN_FILE": {
        "JP": "ファイルを開く",
        "US": "Open File..."
    },
    "SAVE_NEW_FILE": {
        "JP": "名前を受けて保存",
        "US": "Save"
    },
    "EXIT": {
        "JP": "閉じる",
        "US": "Exit"
    },
    "OPTIONS": {
        "JP": "設定",
        "US": "Options..."
    },
    "LANGUAGE_OPTION_MENU": {
        "JP": "言語設定",
        "US": "Language"
    },
    "SET_OPTIONS": {
        "JP": "設定反映",
        "US": "設定反映aaa"
    }
}


def get(key: str):
    global LANGUAGE_DIST
    lang = settings.getLang()
    if not LANGUAGE_DIST.get(key):
        return "null"
    dist = LANGUAGE_DIST.get(key)
    if not dist.get(lang.upper()):
        return "null"
    return dist.get(lang.upper())

def getLangDist():
    global LANGUAGE_DIST
    return LANGUAGE_DIST.get("LANG")