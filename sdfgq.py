import matplotlib.pyplot as plt
plt.set_cmap('YlGn')

import tkinter as tk

def on_click():
    print(var.get())

root = tk.Tk()
var = tk.IntVar()
tk.Checkbutton(root, variable=var).pack()
tk.Button(root, text="Print state to console", command=on_click).pack()
root.mainloop()