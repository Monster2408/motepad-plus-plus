import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter.ttk import Notebook
from PIL import ImageTk
import os

from lib import language as LANG
from lib import Var
from lib import optionWindow as OpWin
from lib import MotePadPlusPlus as MPPP
from lib import settings
from lib import ShortCut

""" ここからが関数群 """
def setFileMenu():
    """ファイルメニュー作成用関数
    """    
    # ファイルメニュー
    filemenu = tk.Menu(Var.menubar, tearoff=0)
    Var.menubar.add_cascade(
        label=f'{LANG.get("FILE")}', menu=filemenu)
    # ～内容
    filemenu.add_command(
        label=f'{LANG.get("CREATE_NEW_FILE")}', command=MPPP.add_tab)
    filemenu.add_command(
        label=f'{LANG.get("OPEN_FILE")}', command=MPPP.open_text)
    filemenu.add_command(
        label=f'{LANG.get("SAVE_NEW_FILE")}', command=MPPP.file_save)
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
    # 新規作成
    ico_new_file = ImageTk.PhotoImage(file = settings.resource_path("icon/newFile.bmp"))
    btn_new_file = tk.Button(frame_toolbar, command = MPPP.add_tab, image = ico_new_file)
    btn_new_file.image = ico_new_file
    MPPP.CreateToolTip(btn_new_file, LANG.get("CREATE_NEW_FILE"))
    # ファイルを開く
    ico_open_file = ImageTk.PhotoImage(file = settings.resource_path("icon/openFile.bmp"))
    btn_open_file = tk.Button(frame_toolbar, command = MPPP.open_text, image = ico_open_file)
    btn_open_file.image = ico_open_file
    MPPP.CreateToolTip(btn_open_file, LANG.get("OPEN_FILE"))
    # 保存
    ico_save = ImageTk.PhotoImage(file = settings.resource_path("icon/saveFile.bmp"))
    btn_save = tk.Button(frame_toolbar, command = MPPP.file_save, image = ico_save)
    btn_save.image = ico_save
    MPPP.CreateToolTip(btn_save, LANG.get("SAVE_FILE"))
    # ファイル閉じる(留意事項README.mdにありんす)
    ico_close = ImageTk.PhotoImage(file = settings.resource_path("icon/closeFile.bmp"))
    btn_close = tk.Button(frame_toolbar, command = MPPP.close_file, image = ico_close)
    btn_close.image = ico_close
    MPPP.CreateToolTip(btn_close, LANG.get("CLOSE"))
    # ズームイン(拡大表示)
    ico_zoom_in = ImageTk.PhotoImage(file = settings.resource_path("icon/zoomIn.bmp"))
    btn_zoom_in = tk.Button(frame_toolbar, image = ico_zoom_in, command=MPPP.zoomIn)
    btn_zoom_in.image = ico_zoom_in
    MPPP.CreateToolTip(btn_zoom_in, LANG.get("ZOOM_IN"))
    # ズームアウト(縮小表示)
    ico_zoom_out = ImageTk.PhotoImage(file = settings.resource_path("icon/zoomOut.bmp"))
    btn_zoom_out = tk.Button(frame_toolbar, image = ico_zoom_out, command=MPPP.zoomOut)
    btn_zoom_out.image = ico_zoom_out
    MPPP.CreateToolTip(btn_zoom_out, LANG.get("ZOOM_OUT"))
    
    #-------------------------
    # ボタンをフレームに配置
    btn_new_file.pack(side = tk.LEFT, padx = (5, 0)) # 左側だけ隙間を空ける
    btn_open_file.pack(side = tk.LEFT) 
    btn_save.pack(side = tk.LEFT)
    btn_close.pack(side = tk.LEFT)
    btn_zoom_in.pack(side = tk.LEFT)
    btn_zoom_out.pack(side = tk.LEFT)
    
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
    
    Var.tframes = []
    Var.fnames = []
    
    setToolBar()
    setStatusBar()
    
    Var.notebook = MPPP.CustomNotebook(height=Var.DEFAULT_HEIGHT, width=Var.DEFAULT_WIDTH)
    Var.notebook.pack(fill="both", expand=True)
    MPPP.add_tab()
    
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