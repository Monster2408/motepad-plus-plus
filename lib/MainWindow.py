import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import PhotoImage
import sys
import os

from lib import language as LANG
from lib import Var
from lib import optionWindow as OpWin
from lib import NotePadPlusPlus as NPPP
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

def _rightSlide(event):
    if Var.tab_frame.winfo_width()>Var.notebook.winfo_width()-30:
        if (Var.tframes.winfo_width()-(Var.tab_frame.winfo_width()+Var.tab_frame.winfo_x()))<=35:
            Var.xLocation-=20
            Var.tab_frame.place(x=Var.xLocation,y=0)
def _leftSlide(event):
    if not Var.notebook.winfo_x()== 0:
        Var.xLocation+=20
        Var.notebook.place(x=Var.xLocation,y=0)
    
def start():
    """メインウインドウ作成用関数
    
    設定繁栄が面倒なため設定後は一度全ウインドウをキルして再度この関数を実行すること。
    """    
    Var.root = tk.Tk()
    Var.root.title(f'{Var.EDITORDISPLAYNAME}')
    
    iconfile = settings.resource_path("MotePad++_icon.ico")
    Var.root.iconbitmap(default=iconfile)
    
    Var.root.geometry('400x300')
    Var.notebook = ttk.Notebook(Var.root)
    Var.notebook.pack(fill='both',expand=1)
    Var.tframes = []
    Var.fnames = []
    add_tab()
    
    # メニューバーの作成
    Var.menubar = tk.Menu(Var.root)
    Var.root.configure(menu = Var.menubar)
    
    slideFrame = ttk.Frame(Var.root)
    slideFrame.place(relx=1.0, x=0, y=1, anchor=tk.NE)
    leftArrow = ttk.Label(slideFrame, text="\u25c0")
    leftArrow.bind("<1>",_leftSlide)
    leftArrow.pack(side=tk.LEFT)
    rightArrow = ttk.Label(slideFrame, text=" \u25b6")
    rightArrow.bind("<1>",_rightSlide)
    rightArrow.pack(side=tk.RIGHT)
    # notebookContent.bind( "<Configure>", _resetSlide)
    
    setFileMenu()
    setOptionMenu()
    
    Var.root.bind("<Control-q>", sys.exit)
    Var.root.bind("<Control-Q>", sys.exit)
    
    Var.root.bind("<Control-w>", ShortCut.ctrl_w)
    Var.root.bind("<Control-W>", ShortCut.ctrl_w)
    
    Var.root.bind("<Control-q>", sys.exit)
    Var.root.bind("<Control-Q>", sys.exit)
    
    Var.root.bind("<Control-n>", ShortCut.ctrl_n)
    Var.root.bind("<Control-N>", ShortCut.ctrl_n)

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
        
def start2():
    Var.root = tk.Tk()
    Var.root.title(f'{Var.EDITORDISPLAYNAME}')
    
    iconfile = settings.resource_path("MotePad++_icon.ico")
    Var.root.iconbitmap(default=iconfile)

    Var.root.rowconfigure(0, minsize=500, weight=1)
    Var.root.columnconfigure(1, minsize=500, weight=1)
    
    Var.text_editor = tk.Text(Var.root)
    Var.linenumber_frame = tk.Frame(Var.root, relief=tk.FLAT, bd=2, width=40)
    Var.tab_frame = tk.Frame(Var.root, relief=tk.FLAT, bd=2)

    Var.scrollbar = tk.Scrollbar(Var.root, orient=tk.VERTICAL, command=Var.text_editor.yview)
    Var.text_editor["yscrollcommand"] = Var.scrollbar.set

    Var.scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S, tk.E))
    Var.tab_frame.grid(row=0, sticky=(tk.W, tk.E))
    Var.linenumber_frame.grid(row=1, column=0, sticky="ns")
    Var.text_editor.grid(row=1, column=1, sticky='nsew')

    # メニューバーの作成
    Var.menubar = tk.Menu(Var.root)
    Var.root.configure(menu = Var.menubar)

    setFileMenu()
    setOptionMenu()

    Var.root.mainloop()
        
def add_tab(fname = None): # // TODO タブを閉じるボタン作成必須
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
    tframe=NPPP.NotePadPlusPlus(Var.notebook)
    Var.tframes.append(tframe)
    if os.path.isfile(fname):
        f=open(fname,'r')
        lines=f.readlines()
        f.close()
        for line in lines:
            tframe.text.insert('end',line)
    Var.fnames.append(fname)
    title=os.path.basename(fname)
    prof_img = PhotoImage(file=settings.resource_path("close_black.png"))
    Var.notebook.add(tframe,text=title,image=prof_img, compound='right')
    Var.notebook.select(Var.notebook.tabs()[Var.notebook.index('end')-1])