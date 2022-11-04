import tkinter as tk


class Child(tk.Toplevel):

    def submitFunction(self):
        amount = 2
        self.parent.amount.set(str(amount))  # Set parent amount.
        self.destroy()

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.frame = tk.Frame(self)
        self.frame.grid()

        submit = tk.Button(self.frame, text='Submit', command=self.submitFunction).grid(row=0, column=0)
