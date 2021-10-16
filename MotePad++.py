import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from lib import language as LANG
from lib import settings

# defaultWidth = 1280
# defaultHeight = 720

EDITORDISPLAYNAME = "MotePad++"

def open_text():
    global EDITORDISPLAYNAME
    typ = [(f'{LANG.get("TEXT_FILES", settings.get("language"))}', '*.txt')]
    filepath = askopenfilename(filetypes=typ)
    if not filepath:
        return
    text_editor.delete('1.0', tk.END)
    with open(filepath, "r", encoding="utf-8") as open_file:
        text = open_file.read()
        text_editor.insert(tk.END, text)
    root.title(f'{LANG.get("TEXT_FILES", settings.get("language"))} - {filepath}')

def file_save():
    global EDITORDISPLAYNAME
    typ = [(f'{LANG.get("TEXT_FILES", settings.get("language"))}', '*.txt')]
    filepath = asksaveasfilename(defaultextension='txt',filetypes=typ)
    if not filepath:
        return
    with open(filepath, 'w') as save_file:
        text = text_editor.get('1.0', tk.END)
        save_file.write(text)
    root.title(f"{EDITORDISPLAYNAME} - {filepath}")

def setFileMenu():
    # ファイルメニュー
    filemenu = tk.Menu(menubar, tearoff = 0)
    menubar.add_cascade(label = f'{LANG.get("FILE", settings.get("language"))}', menu = filemenu)
    # ～内容
    filemenu.add_command(label = f'{LANG.get("OPEN_FILE", settings.get("language"))}', command=open_text)
    filemenu.add_command(label = f'{LANG.get("SAVE_NEW_FILE", settings.get("language"))}', command=file_save)
    # セパレーター
    filemenu.add_separator()
    filemenu.add_command(label = f'{LANG.get("EXIT", settings.get("language"))}', command = lambda: root.destroy())

root = tk.Tk()
root.title(f'{EDITORDISPLAYNAME}')

root.rowconfigure(0, minsize=500, weight=1)
root.columnconfigure(1, minsize=500, weight=1)

text_editor = tk.Text(root)

text_editor.grid(row=0, column=1, sticky='nsew')

# メニューバーの作成
menubar = tk.Menu(root)
root.configure(menu = menubar)

setFileMenu()



root.mainloop()