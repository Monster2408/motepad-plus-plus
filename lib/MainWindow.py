import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import sys
import os

from lib import language as LANG
from lib import Var
from lib import optionWindow as OpWin
from lib import MotePadPlusPlus as MPPP
from lib import settings
from lib import ShortCut

""" ここからが関数群 """
def open_text():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    filepath = askopenfilename(filetypes=typ)
    if not filepath:
        return
    add_tab(filepath)

def file_save():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    idx = Var.notebook.tabs().index(Var.notebook.select())
    tframe = Var.tframes[idx]
    fname = Var.fnames[idx]
    filepath = asksaveasfilename(defaultextension='txt', filetypes=typ, initialfile=fname)
    if not filepath:
        return
    with open(filepath, 'w') as save_file:
        text = tframe.text.get('1.0', tk.END)
        save_file.write(text)


def setFileMenu():
    """ファイルメニュー作成用関数
    """    
    # ファイルメニュー
    filemenu = tk.Menu(Var.menubar, tearoff=0)
    Var.menubar.add_cascade(
        label=f'{LANG.get("FILE")}', menu=filemenu)
    # ～内容
    filemenu.add_command(
        label=f'{LANG.get("CREATE_NEW_FILE")}', command=add_tab)
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
    
    iconfile = settings.resource_path("MotePad++_icon.ico")
    Var.root.iconbitmap(default=iconfile)
    
    Var.root.geometry('400x300')
    Var.notebook = MPPP.CustomNotebook(width=400, height=300)
    Var.notebook.pack(side="top", fill="both", expand=True)
    Var.tframes = []
    Var.fnames = []
    add_tab()
    
    # メニューバーの作成
    Var.menubar = tk.Menu(Var.root)
    Var.root.configure(menu = Var.menubar)
    
    setFileMenu()
    setOptionMenu()
    
    ShortCut.binds()

    Var.root.mainloop()

def restart(): 
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
        
def add_tab(fname = None): 
    """新規作成用

    Args:
        fname (string): [description]. ファイル名またはファイルパス
    """
    if fname == None:
        new_file_num = 1
        if len(Var.fnames) > 0:
            while True:
                if f'{LANG.get("NEW_FILE_NAME")}{str(new_file_num)}' not in Var.fnames:
                    break
                new_file_num += 1
        fname = f'{LANG.get("NEW_FILE_NAME")}{str(new_file_num)}'
    tframe=MPPP.CustomFrame(Var.notebook)
    Var.tframes.append(tframe)
    if os.path.isfile(fname):
        f=open(fname,'r')
        lines=f.readlines()
        f.close()
        for line in lines:
            tframe.text.insert('end',line)
    Var.fnames.append(fname)
    title=os.path.basename(fname)
    Var.notebook.add(tframe,text=title)
    Var.notebook.select(Var.notebook.tabs()[Var.notebook.index('end')-1])