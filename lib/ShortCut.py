from lib import Var
from lib import MainWindow

def ctrl_w(event):
    idx = Var.notebook.tabs().index(Var.notebook.select())
    frame = Var.tframes[idx]
    name = Var.fnames[idx]
    Var.tframes.remove(frame)
    Var.fnames.remove(name)
    frame.destroy()
    if len(Var.tframes) < 1:
        MainWindow.add_tab()
        
def ctrl_n(event):
    MainWindow.add_tab()