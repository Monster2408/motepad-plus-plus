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
                Var.settings_temp_language = keys[0]
                restartButton["text"] = LANG.get('SET_OPTIONS', keys[0])
        Var.optionWindow.bind("<<ComboboxSelected>>", language_selected)

def clearVariables():
    Var.optionWindow = None
    Var.selectedLangValue = None
    
def setVariables():
    if Var.settings_temp_language != None:
        settings.updateOption("language", Var.settings_temp_language)