from tkinter import *
from pymongo import MongoClient
import customtkinter


class ChildWindow:
    def __init__(self, parent, width, height, title="MyWindow", resizable=(False, False), icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+850+350")
        self.root.resizable(resizable[0], resizable[1])
        self.close_wind = False
        self.but = Button(self.root, text='Create', command=self.createCollection)
        self.nameDB = Entry(self.root)
        self.nameCollection = Entry(self.root)
        # for k in i:
        #     print(k)
        # keys = []
        # pos = len(i.keys())
        # for key in i.keys():
        #     keys.append(key)
        # self.table = Treeview(self.main_frame, show='headings', columns=keys)
        # for k, val in i.items():
        #     print(k)
        # for kv in i.items():
        #     print(kv)
        # for j in keys:
        #     self.table.heading(f'{j}', text=j)
        # print(i.values())
        # values.append(i.values().__str__())
        # self.table.insert('', END, values=[list(i.values())[::1]])
        # self.table.insert('', END, values=i)
        #
        # self.table.pack(side=RIGHT, fill=BOTH, expand=1, ipadx=300)

        # self.table.heading(f'{i.keys()}', text=i.keys().__str__())
        # self.table.insert("", END, values=i)
        if icon:
            self.root.iconbitmap(icon)

    def draw(self):
        self.but.pack()
        self.nameDB.pack()
        self.nameCollection.pack()

    def createCollection(self):
        client = MongoClient('localhost', 27017)
        var = client[self.nameDB.get()]
        collection = var.create_collection(self.nameCollection.get())
        print(self.nameDB.get())
        self.close_wind = True
        print(self.close_wind)
        self.root.destroy()
