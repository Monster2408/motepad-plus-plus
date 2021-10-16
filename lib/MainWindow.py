import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import StringVar
import sys

from lib import language as LANG
from lib import Var
from lib import optionWindow as OpWin

""" ここからが関数群 """
def open_text():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    filepath = askopenfilename(filetypes=typ)
    if not filepath:
        return
    Var.text_editor.delete('1.0', tk.END)
    with open(filepath, "r", encoding="utf-8") as open_file:
        text = open_file.read()
        Var.text_editor.insert(tk.END, text)
    Var.root.title(
        f'{LANG.get("TEXT_FILES")} - {filepath}')

def file_save():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    filepath = asksaveasfilename(defaultextension='txt', filetypes=typ)
    if not filepath:
        return
    with open(filepath, 'w') as save_file:
        text = Var.text_editor.get('1.0', tk.END)
        save_file.write(text)
    Var.root.title(f"{Var.EDITORDISPLAYNAME} - {filepath}")


def setFileMenu():
    """ファイルメニュー作成用関数
    """    
    # ファイルメニュー
    filemenu = tk.Menu(Var.menubar, tearoff=0)
    Var.menubar.add_cascade(
        label=f'{LANG.get("FILE")}', menu=filemenu)
    # ～内容
    filemenu.add_command(
        label=f'{LANG.get("OPEN_FILE")}', command=open_text)
    filemenu.add_command(
        label=f'{LANG.get("SAVE_NEW_FILE")}', command=file_save)
    # セパレーター
    filemenu.add_separator()
    filemenu.add_command(
        label=f'{LANG.get("EXIT")}', command=lambda: Var.root.destroy())


def setOptionMenu():
    """設定メニュー作成用関数
    """    
    # 設定メニュー
    filemenu = tk.Menu(Var.menubar, tearoff=0)
    Var.menubar.add_cascade(
        label=f'{LANG.get("OPTIONS")}', menu=filemenu)
    # ～内容
    filemenu.add_command(
        label=f'{LANG.get("OPTIONS")}', command=OpWin.createOptionWindow)



def start():
    """メインウインドウ作成用関数
    設定繁栄が面倒なため設定後は一度全ウインドウをキルして再度この関数を実行すること。
    """    
    Var.root = tk.Tk()
    Var.root.title(f'{Var.EDITORDISPLAYNAME}')

    Var.root.rowconfigure(0, minsize=500, weight=1)
    Var.root.columnconfigure(1, minsize=500, weight=1)

    Var.text_editor = tk.Text(Var.root)
    Var.linenumber_frame = tk.Frame(Var.root, relief=tk.FLAT, bd=2, width=40)

    Var.scrollbar = tk.Scrollbar(Var.root, orient=tk.VERTICAL, command=Var.text_editor.yview)
    Var.text_editor["yscrollcommand"] = Var.scrollbar.set

    Var.scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.E))
    Var.linenumber_frame.grid(row=0, column=0, sticky="ns")
    Var.text_editor.grid(row=0, column=1, sticky='nsew')

    # メニューバーの作成
    Var.menubar = tk.Menu(Var.root)
    Var.root.configure(menu = Var.menubar)

    setFileMenu()
    setOptionMenu()

    Var.root.mainloop()

def restart(): # // TODO いいえを選択すると再設定不可になる
    # メッセージボックス（はい・いいえ） 
    ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
    if ret == True:
        OpWin.clearVariables()
        OpWin.setVariables()
        Var.root.destroy()
        start()
    else:
        Var.optionWindow.destroy()
        OpWin.clearVariables()