import tkinter
from client_serial import loop

m = tkinter.Tk()

button = tkinter.Button(m, text="Run Command", command=lambda: loop("Your Command"))
button.pack()


m.mainloop()
