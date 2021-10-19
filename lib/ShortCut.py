import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk

from lib import Var
from lib import MainWindow
from lib import language as LANG
from lib import MotePadPlusPlus as MPPP

def ctrl_w(event):
    MPPP.close_file()
        
def ctrl_n(event):
    MPPP.add_tab()

def ctrl_s(event):
    MPPP.file_save()

def ctrl_alt_s(event):
    MPPP.file_new_save()
    
def binds():
    Var.root.bind("<Control-q>", sys.exit)
    Var.root.bind("<Control-Q>", sys.exit)
    
    Var.root.bind("<Control-w>", ctrl_w)
    Var.root.bind("<Control-W>", ctrl_w)
    
    Var.root.bind("<Control-n>", ctrl_n)
    Var.root.bind("<Control-N>", ctrl_n)
    
    Var.root.bind("<Control-s>", ctrl_s)
    Var.root.bind("<Control-S>", ctrl_s)

    Var.root.bind("<Control-Alt-s>", ctrl_alt_s)
    Var.root.bind("<Control-Alt-S>", ctrl_alt_s)