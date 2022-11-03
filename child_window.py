from tkinter import *
from pymongo import MongoClient
import customtkinter


class ChildWindow:
    def __init__(self, parent, width, height, title="MyWindow", resizable=(False, False), icon=None):
        self.root = customtkinter.CTkToplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+850+350")
        self.root.resizable(resizable[0], resizable[1])
        self.close_wind = False
        self.but = customtkinter.CTkButton(self.root, text='Create', command=self.createCollection)
        self.nameDB = customtkinter.CTkEntry(self.root, width=165)
        self.list_box = customtkinter.CTkComboBox(self.root)
        self.nameCollection = customtkinter.CTkEntry(self.root, width=165)
        self.name_db = customtkinter.CTkLabel(self.root, text='Write name DB')
        self.name_collection = customtkinter.CTkLabel(self.root, text='Write name collection')
        self.but_to_collection = customtkinter.CTkButton(self.root, text='Create', command=self.collection)
        self.but_drop_collection = customtkinter.CTkButton(self.root, text='Drop Collection',
                                                           command=self.drop_collection)
        self.but_drop_db = customtkinter.CTkButton(self.root, text='Drop DB', command=self.drop_db)
        if icon:
            self.root.iconbitmap(icon)

    def drop_db(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(self.list_box.get())
        self.root.destroy()

    def drop_collection(self):
        client = MongoClient('localhost', 27017)
        var = client[self.list_box.get()]
        collection = var[self.nameCollection.get()]
        collection.drop()
        # print(self.nameDB.get())
        self.close_wind = True
        # print(self.close_wind)
        self.root.destroy()
        # print('ok')

    def draw(self):
        self.name_db.configure(text='Write name DB')
        self.name_db.pack()
        self.nameDB.pack()
        self.name_collection.pack()
        self.nameCollection.pack()
        self.but.place(x=30, y=150)

    def draw_for_drop_db(self):
        client = MongoClient('localhost', 27017)
        self.name_db.configure(text='Choose DB')
        self.name_db.pack()
        self.list_box.set('Change')
        self.list_box.configure(values=client.list_database_names(), width=165)
        self.but_drop_db.place(x=30, y=150)
        self.list_box.pack()

    def draw_for_drop(self):
        client = MongoClient('localhost', 27017)
        self.name_db.configure(text='Choose DB')
        self.name_db.pack()
        self.list_box.set('Change')
        self.list_box.configure(values=client.list_database_names(), width=165)
        self.list_box.pack()
        self.name_collection.pack()
        self.nameCollection.pack()
        self.but_drop_collection.place(x=30, y=150)

    def draw_for_db(self):
        client = MongoClient('localhost', 27017)
        self.name_db.configure(text='Choose DB')
        self.name_db.pack()
        self.list_box.set('Change')
        self.list_box.configure(values=client.list_database_names(), width=165)
        self.list_box.pack()
        self.name_collection.pack()
        self.nameCollection.pack()
        self.but_to_collection.place(x=30, y=150)

    def collection(self):
        client = MongoClient('localhost', 27017)
        var = client[self.list_box.get()]
        collection = var.create_collection(self.nameCollection.get())
        print(self.nameDB.get())
        self.close_wind = True
        print(self.close_wind)
        self.root.destroy()
        print('ok')

    def createCollection(self):
        client = MongoClient('localhost', 27017)
        var = client[self.nameDB.get()]
        collection = var.create_collection(self.nameCollection.get())
        print(self.nameDB.get())
        self.close_wind = True
        print(self.close_wind)
        self.root.destroy()
