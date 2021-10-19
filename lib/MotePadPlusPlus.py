import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

from lib import Var
from lib import MainWindow
from lib import language as LANG

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind("<<NotebookTabChanged>>", self.on_change_select_tab)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            close_file(index)

        self.state(["!pressed"])
        self._active = None
            
    def on_change_select_tab(self, event):
        pass

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            # 
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            '''),
            tk.PhotoImage("img_closehover", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
            '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closehover"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

class CustomFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        text = tk.Text(self,wrap='none',undo=True,font=(Var.font, Var.text_size))
        x_sb = tk.Scrollbar(self,orient='horizontal')
        y_sb = tk.Scrollbar(self,orient='vertical')
        x_sb.config(command=text.xview)
        y_sb.config(command=text.yview)
        text.config(xscrollcommand=x_sb.set,yscrollcommand=y_sb.set)
        text.grid(column=0,row=0,sticky='nsew')
        x_sb.grid(column=0,row=1,sticky='ew')
        y_sb.grid(column=1,row=0,sticky='ns')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.text = text
        self.x_sb = x_sb
        self.y_sb = y_sb
        self.text.bind("<Enter>", self.enter)
        self.text.bind("<Leave>", self.leave)
        self.text.bind("<Control-MouseWheel>", self.zoom_ctrl)
    
    def getText(self) -> tk.Text:
        return self.text
        
    def enter(self, event):
        Var.frame_hover_now = True

    def leave(self, event):
        Var.frame_hover_now = False
    
    def zoom_ctrl(self, event):
        if event.delta > 0:
            zoomIn()
        else:
            zoomOut()
        
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
            background="#ffffff", relief='solid', borderwidth=1,
            wraplength = self.wraplength
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
            
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
        add_tab()

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
    tframe=CustomFrame(Var.notebook)
    # tframe.bind("<Enter>", enter)
    # tframe.bind("<Leave>", leave)
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

def zoom(scale: int):
    size = Var.text_size
    size += scale
    if Var.MINIMUMTEXTSIZE >= size or Var.MAXTEXTSIZE <= size:
        return
    
    Var.text_size += scale
    for frame in Var.tframes:
        txt = ''
        if frame.text != None:
            txt = frame.text.get(0.0,tk.END+"-1c")
        frame.text.delete(0.0,tk.END)
        frame.text.configure(font=(Var.font, Var.text_size))
        frame.text.insert(0.0,txt)

def zoomIn():
    zoom(1)
    
def zoomOut():
    zoom(-1)