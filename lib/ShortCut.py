import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk

from lib import Var
from lib import MainWindow
from lib import language as LANG
from lib import MotePadPlusPlus as MPPP

def close_file(index = -1):
    if index == -1:
        index = Var.notebook.tabs().index(Var.notebook.select())
    idx = index
    frame = Var.tframes[idx]
    name = Var.fnames[idx]
    Var.notebook.forget(idx)
    Var.tframes.remove(frame)
    Var.fnames.remove(name)
    # frame.destroy()
    Var.notebook.event_generate("<<NotebookTabClosed>>")
    if len(Var.tframes) < 1:
        MPPP.add_tab()

def open_text():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    filepath = askopenfilename(filetypes=typ)
    if not filepath:
        return
    MPPP.add_tab(filepath)

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

def ctrl_w(event):
    MPPP.close_file()
        
def ctrl_n(event):
    MPPP.add_tab()
    
def binds():
    Var.root.bind("<Control-q>", sys.exit)
    Var.root.bind("<Control-Q>", sys.exit)
    
    Var.root.bind("<Control-w>", ctrl_w)
    Var.root.bind("<Control-W>", ctrl_w)
    
    Var.root.bind("<Control-n>", ctrl_n)
    Var.root.bind("<Control-N>", ctrl_n)