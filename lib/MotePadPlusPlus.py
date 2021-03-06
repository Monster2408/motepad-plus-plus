import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import base64

from lib import Var
from lib import settings
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
        self._saved = True

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind("<Motion>", self.on_close_motion)

        self.bind("<<SaveRenameFile>>", self.save_motion)
        self.bind("<<SaveFile>>", self.save_motion)
        self.bind("<<ChangeFrameText>>", self.edit_motion)
        
        self.bind("<<ChangeFrameText>>", self.tab_change_motion)

    def tab_change_motion(self, event=None):
        # key = self.images[4]
        # if not self._saved:
        #     self.images[4] = tk.PhotoImage(f"{key}", self.img_tab_icon_unsaved)
        # else:
        #     self.images[4] = tk.PhotoImage(f"{key}", self.img_tab_icon)
        pass

    def save_motion(self, event):
        self._saved = True
        self.tab_change_motion()

    def edit_motion(self, event):
        self._saved = False
        self.tab_change_motion()

    def on_close_motion(self, event):
        element = self.identify(event.x, event.y)
        if "close" in element:
            self.state(['!pressed'])
            self.state(['hover'])
        else:
            self.state(['!pressed'])
            self.state(['!hover'])

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        self.tab_change_motion()
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self.state(['hover'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self._saved:
            self.state(['!focus'])
        else:
            self.state(['focus'])
        if not self.instate(['pressed']) and not self.instate(['hover']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            self.state(['!pressed'])
            self.state(['!hover'])
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            close_file(index)

        self.state(["!pressed"])
        self.state(['!hover'])
        self._active = None

    def __initialize_custom_style(self):
        img_close = image_file_to_base64(settings.resource_path("icon/tab/closeTabButton.gif"))
        img_closehover = image_file_to_base64(settings.resource_path("icon/tab/closeTabButton_hover.gif"))
        img_closepressed = image_file_to_base64(settings.resource_path("icon/tab/closeTabButton_push.gif"))
        img_closeintact = image_file_to_base64(settings.resource_path("icon/tab/closeTabButton_inact.gif"))
        self.img_tab_icon = image_file_to_base64(settings.resource_path("icon/tab/saved.gif"))
        self.img_tab_icon_unsaved = image_file_to_base64(settings.resource_path("icon/tab/unsaved.gif"))
        
        style = ttk.Style()
        self.images = (
            # 
            tk.PhotoImage("img_close", data=img_close),
            tk.PhotoImage("img_closehover", data=img_closehover),
            tk.PhotoImage("img_closepressed", data=img_closepressed),
            tk.PhotoImage("img_closeintact", data=img_closeintact),
            tk.PhotoImage("img_tab_icon", data=self.img_tab_icon),
            tk.PhotoImage("img_tab_icon_unsaved", data=self.img_tab_icon_unsaved),
        )

        style.element_create(
            "close", "image", "img_close",
            ("!active", "!selected", "!pressed", "!hover", "!disabled", "img_closeintact"),
            ("!active", "!selected", "!pressed", "hover", "!disabled", "img_closehover"), 
            ("!active", "!selected", "pressed", "hover", "!disabled", "img_closepressed"),
            ("active", "selected", "!pressed", "hover", "!disabled", "img_closehover"), 
            ("active", "selected", "pressed", "hover", "!disabled", "img_closepressed"),
            ("active", "selected", "!pressed", "!hover", "!disabled", "img_close"), 
            border=8, sticky=''
        )
        style.element_create(
            "tab_icon", "image", "img_tab_icon",
            border=8, sticky=''
        )
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
                                    ("CustomNotebook.tab_icon", {"side": "left", "sticky": ''}),
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
        self.bind_all('<KeyPress>', self._beenModified)
        self.bind("<<SaveFile>>", self.saved)
        self.bind("<<SaveRenameFile>>", self.saved)
        self.beforeText = text.get(0.0,tk.END)
        self.editNow = False

    def _beenModified(self, event=None):
        if self.beforeText == self.text.get(0.0,tk.END):
            return
        self.beforeText = self.text.get(0.0,tk.END)
        self.editNow = True
        self.event_generate("<<ChangeFrameText>>")
    
    def saved(self, event):
        """???????????????????????????????????????
        """
        self.editNow = False
        
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
    Var.notebook.state(["!pressed"])
    Var.notebook.state(["!hover"])
    Var.notebook.event_generate("<<NotebookTabClosed>>")
    if len(Var.tframes) < 1:
        add_tab()

def open_text():
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    filepath = askopenfilename(filetypes=typ)
    if not filepath:
        return
    add_tab(filepath)

def file_new_save():
    file_save(True)

def file_save(rename = False):
    typ = [(f'{LANG.get("TEXT_FILES")}', '*.txt')]
    idx = Var.notebook.tabs().index(Var.notebook.select())
    tframe = Var.tframes[idx]
    fname = Var.fnames[idx]
    if rename == False and os.path.exists(fname):
        with open(fname, 'w') as save_file:
            text = tframe.text.get('1.0', tk.END+"-1c")
            save_file.write(text)
            Var.tframes[idx].event_generate("<<SaveFile>>")
        return
    dirname = os.path.dirname(fname)
    basename = os.path.basename(fname)
    Var.tframes[idx].event_generate("<<SaveFileCheck>>")
    filepath = asksaveasfilename(defaultextension='txt', filetypes=typ, initialfile=basename, initialdir=dirname)
    if not filepath:
        return
    with open(filepath, 'w') as save_file:
        text = tframe.text.get('1.0', tk.END+"-1c")
        save_file.write(text)
        if basename != fname:
            Var.fnames[idx] = filepath
            Var.tframes[idx].event_generate("<<SaveRenameFile>>")
            if Var.tab_filename_startsspace: Var.notebook.tab(Var.notebook.select(), text=f" {basename}")
            else: Var.notebook.tab(Var.notebook.select(), text=basename)
        else: Var.tframes[idx].event_generate("<<SaveFile>>")
        
def add_tab(fname = None): 
    """???????????????

    Args:
        fname (string): [description]. ??????????????????????????????????????????
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
    
    if Var.tab_filename_startsspace: Var.notebook.add(tframe,text=f" {title}")
    else: Var.notebook.add(tframe,text=title)
    Var.notebook.select(Var.notebook.tabs()[Var.notebook.index('end')-1])
    
    Var.notebook.state(["!pressed"])
    Var.notebook.state(["!hover"])
    Var.notebook.state(["focus"])

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

def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode('utf-8')

def zoomIn():
    zoom(1)
    
def zoomOut():
    zoom(-1)