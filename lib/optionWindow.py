import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar
from lib import language as LANG
from lib import settings
from lib import Var
from lib import MainWindow



def createOptionWindow():
    if Var.optionWindow == None or not Var.optionWindow.winfo_exists():
        Var.optionWindow = tk.Toplevel(Var.root)
        Var.optionWindow.geometry("300x100")
        Var.optionWindow.title(f"{Var.EDITORDISPLAYNAME} - {LANG.get('OPTIONS')}")
        labelExample = tk.Label(Var.optionWindow, text = "")

        ### Listbox ###
        if Var.selectedLangValue == None:
            Var.selectedLangValue = StringVar()

        Var.selectedLangValue.set(LANG.get('LANG'))

        combobox = ttk.Combobox(Var.optionWindow, state="readonly", textvariable=Var.selectedLangValue, values=list(LANG.getLangDist().values()))

        labelExample.pack()
        combobox.pack()

        restartButton=tk.Button(Var.optionWindow, text = f"{LANG.get('SET_OPTIONS')}", command = MainWindow.restart)

        restartButton.pack()

        def language_selected(event):
            keys = [k for k, v in LANG.getLangDist().items() if v == f'{combobox.get()}']
            if len(keys) > 0:
                settings.updateOption("language", keys[0])
                Var.optionWindow.title(f"{Var.EDITORDISPLAYNAME} - {LANG.get('OPTIONS')}")
                restartButton["text"] = LANG.get('SET_OPTIONS')
        Var.optionWindow.bind("<<ComboboxSelected>>", language_selected)

def clearVariables():
    Var.optionWindow = None
    Var.selectedLangValue = None

def refreshVariables():
    Var.selectedLangValue = StringVar()

    Var.selectedLangValue.set(LANG.get('LANG'))