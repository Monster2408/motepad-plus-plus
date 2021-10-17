import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk
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
    
def setToolBar():
    #---------------------------------------
    #  ツールバー
    #---------------------------------------
    # ツールバー用Frame
    frame_toolbar = tk.Frame(Var.root, relief = tk.FLAT, bd = 2)
    # ツールバーをウィンドの上に配置
    frame_toolbar.pack(side = tk.TOP, fill = tk.X)
    
    # ボタン
    # ファイルを開く
    ico_open_file = ImageTk.PhotoImage(file = settings.resource_path("icon_openFile.bmp"))
    btn_open_file = tk.Button(frame_toolbar, command = open_text, image = ico_open_file)
    btn_open_file.image = ico_open_file
    # 保存
    ico_save = ImageTk.PhotoImage(file = settings.resource_path("icon_saveFile.bmp"))
    btn_save = tk.Button(frame_toolbar, command = file_save, image = ico_save)
    btn_save.image = ico_save
    
    #-------------------------
    # ボタンをフレームに配置
    btn_open_file.pack(side = tk.LEFT, padx = (5, 0)) # 左側だけ隙間を空ける
    btn_save.pack(side = tk.LEFT)
    
def setStatusBar():
    #---------------------------------------
    #  ステータスバー
    #---------------------------------------
    # ステータスバー用Frame
    frame_statusbar = tk.Frame(Var.root, relief = tk.SUNKEN, bd = 2)
    # ステータスラベル
    label = tk.Label(frame_statusbar, text = "StatusLabel")
    # ラベルをフレームに配置
    label.pack(side = tk.LEFT)
    # ステータスバーをウィンドの下に配置
    frame_statusbar.pack(side = tk.BOTTOM, fill = tk.X)
    
def start():
    """メインウインドウ作成用関数
    
    設定繁栄が面倒なため設定後は一度全ウインドウをキルして再度この関数を実行すること。
    """    
    Var.root = tk.Tk()
    Var.root.title(f'{Var.EDITORDISPLAYNAME}')
    
    iconfile = settings.resource_path("MotePad++_icon.ico")
    Var.root.iconbitmap(default=iconfile)
    
    Var.root.geometry(f'{Var.DEFAULT_WIDTH}x{Var.DEFAULT_HEIGHT}')
    
    setToolBar()
    setStatusBar()
    
    Var.notebook = MPPP.CustomNotebook(height=Var.DEFAULT_HEIGHT, width=Var.DEFAULT_WIDTH)
    Var.notebook.pack(fill="both", expand=True)
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