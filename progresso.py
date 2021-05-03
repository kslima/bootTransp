from tkinter import *
from tkinter.ttk import *
import time

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x250+1000+300')
cont = True


def step():
    while cont:
        ws.update_idletasks()
        pb1['value'] += 20

        time.sleep(0.1)


pb1 = Progressbar(ws, orient=HORIZONTAL, mode='indeterminate')
pb1.pack(expand=True)

Button(ws, text='Start', command=step).pack()

ws.mainloop()