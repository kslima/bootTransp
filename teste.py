from ttkwidgets import CheckboxTreeview
import tkinter as tk

root = tk.Tk()

tree = CheckboxTreeview(root)
tree.pack()

tree.insert("", "end", "1", text="1")
tree.insert("", "end", "2", text="2")

root.mainloop()


