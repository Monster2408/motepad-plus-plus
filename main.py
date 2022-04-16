# !C:\Users\enjoy\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-
import sys

import PySimpleGUI as sg
from pyparsing import White
from lib import languages as LANG

import Var
import function as func

# textはMultiline.Widgetを指す
def redo(event, text):
    try:
        text.edit_redo()
    except:
        pass

def main():
    func.makeResouceFiles()

    # This bit gets the taskbar icon working properly in Windows
    if sys.platform.startswith('win'):
        import ctypes
        # Make sure Pyinstaller icons are still grouped
        if sys.argv[0].endswith('.exe') == False:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string

    menu_layout = [
        [f'{LANG.get("FILE")}',[f'{LANG.get("CREATE_NEW_FILE")}',f'{LANG.get("OPEN_FILE")}',f'{LANG.get("SAVE_FILE")}',f'{LANG.get("SAVE_NEW_FILE")}','---',f'{LANG.get("EXIT")}']],
        ['Edit',['Undo','---','Cut','Copy','Paste','Delete','---','Find...','Replace...','---','Select All','Date/Time']],
        ['Format',['Theme','Font','Tab Size','Show Settings']],
        ['Run',['Run Module']],
        ['Help',['View Help','---',f'{LANG.get("ABOUT_ME")}']]
    ]
    
    right_click_menu = ['&Right', [f'{LANG.get("UNDO")}', f'{LANG.get("REDO")}', '切り取り', 'コピー', '貼り付け']]
    
    toolbar_buttons = [[
        sg.Button('', image_data=Var.NEW_FILE64[22:], button_color=('white', sg.COLOR_SYSTEM_DEFAULT), key=f'{LANG.get("CREATE_NEW_FILE")}', pad=(0,0)),
        sg.Button('', image_data=Var.OPEN_FILE64[22:], button_color=('white', sg.COLOR_SYSTEM_DEFAULT), key=f'{LANG.get("OPEN_FILE")}', pad=(0,0))
    ]]
    
    layout = [
        [sg.Frame('', toolbar_buttons,title_color='white', pad=(0,0), background_color="#FFFFFF")],
        [sg.Menu(menu_layout, key='menu1')],
        [sg.Multiline(key="note", pad=(0,0), size=(None, 50), expand_x=True, expand_y=True, right_click_menu=right_click_menu)],
        [sg.StatusBar("行:1 列:1", key="status_bar", expand_y=True, pad=(0,0), background_color="#FFFFFF", text_color="#000000")]
    ]

    window = sg.Window(Var.TITLE, layout, icon=icon, resizable=True, finalize=True, margins=(0,0), background_color="#FFFFFF")
    text = window["note"].Widget
    text.configure(undo=True) # Undo機能追加
    text.bind("<Control-Key-Y>", lambda event, text=text:redo(event, text)) #Redo機能追加

    while True:
        event, value = window.Read()
        print(event, value)

        if event in ('_close_', 'Exit', f'{LANG.get("EXIT")}') or event is None:
            break
        
        elif event in (f'{LANG.get("REDO")}'):
            try:
                window["note"].Widget.edit_redo()
            except:
                pass

        elif event in (f'{LANG.get("UNDO")}'):
            try:
                window["note"].Widget.edit_undo()
            except:
                pass
        elif event in ("バージョン情報"):
            sg.popup_ok("PySimpleNotePad \nver. 1.0.0", font=("Meiryo UI", 10), icon=icon)

        # マウスクリックでカーソルが移動した場合も表示変更されるようにしたい
        insert_pos = window["note"].Widget.index("insert")
        insert_pos = insert_pos.split(".")
        print("行:{} 列:{}".format(insert_pos[0], int(insert_pos[1])+1))
        window["status_bar"].update("行:{} 列:{}".format(insert_pos[0], int(insert_pos[1])+1))

    window.close()


if __name__ == '__main__':
    icon = func.resourcePath("resources/MotePad++_icon.ico")
    main()