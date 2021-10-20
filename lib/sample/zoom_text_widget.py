import tkinter as tk

root = tk.Tk()
root.state('zoomed')
font = ('Courier', 10)


def zoom(zoom_scale):
    global font

    font = (font[0],) + (font[1] + 1,)
    text.config(font=font)


canvas = tk.Canvas(root)
frame = tk.Frame(canvas)
zoom_scale = tk.Scale(root, orient='vertical', from_=1, to=500)
zoom_scale.config(command=lambda args: zoom(zoom_scale))

zoom_scale.set(10)

text = tk.Text(frame, font=font)
text.grid(row=0, column=0)

canvas.create_window(0, 0, anchor='nw', window=frame)
# make sure everything is displayed before configuring the scroll region
canvas.update_idletasks()

canvas.configure(scrollregion=canvas.bbox('all'))
canvas.pack(fill='both', side='left', expand=True)
zoom_scale.pack(fill='y', side='right')
root.mainloop()