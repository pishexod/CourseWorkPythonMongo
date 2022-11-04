import tkinter as tk


class Child(tk.Toplevel):

    def submitFunction(self):
        amount = 2
        self.parent.amount.set(str(amount))  # Set parent amount.
        self.parent.moto = 2
        self.destroy()

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.frame = tk.Frame(self)
        self.frame.grid()

        submit = tk.Button(self.frame, text='Submit', command=self.submitFunction).grid(row=0, column=0)


class exGui(tk.Tk):

    def update(self):
        self.kid = Child(self)
        print(self.amount, self.kid, self.amount.get())
        print(self.moto)

    def __init__(self):
        tk.Tk.__init__(self)
        frame = tk.Frame(self)
        frame.grid()
        self.amount = tk.StringVar()  # Make amount a StringVar
        self.amount.set('0')
        self.moto = 0# Set it to 0
        self.button = tk.Button(frame, text="pay", command=self.update).grid(row=0, column=0)
        self.button = tk.Button(frame, text="Quit", fg="red", command=frame.quit).grid(row=0, column=1)
        self.result = tk.Label(frame, textvariable=self.amount).grid(row=0, column=2)  # Add a result label.


# This is linked to the self.amount StringVar.

def main():
    exGui().mainloop()


if __name__ == '__main__':
    main()
