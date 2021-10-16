LANGUAGE_DIST = {
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
    }
}


def get(key: str, lang: str):
    global LANGUAGE_DIST
    if not LANGUAGE_DIST.get(key):
        return "null"
    dist = LANGUAGE_DIST.get(key)
    if not dist.get(lang.upper()):
        return "null"
    return dist.get(lang.upper())