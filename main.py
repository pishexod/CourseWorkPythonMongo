import os
import re
from tkinter.font import Font
from tkinter.ttk import Treeview

from bson import ObjectId

from child_window import ChildWindow
from tkinter import *
from tkinter import ttk
from threading import Thread
import customtkinter
import sys
import time
from pymongo import MongoClient
import json
import bson


class Window:
    def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None):

        self.dbBut = None
        self.client = MongoClient()

        self.root = Tk()

        self.add_DB = None
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+400+150")
        self.root.resizable(resizable[0], resizable[1])
        self.main_frame = Frame(self.root, bg='grey')
        self.main_frame.pack(fill=BOTH, expand=1, side=RIGHT)

        self.list_box = customtkinter.CTkComboBox()

        self.font = Font(size=20)
        self.collection_taken = None

        self.pb = ttk.Progressbar(self.main_frame, orient='horizontal', mode='determinate', length=280)
        self.com = Thread(target=self.sys_com)

        self.button = customtkinter.CTkButton(self.main_frame, text="Download", command=self.onclick, width=100,
                                              height=50)

        self.textJSON = Text(self.main_frame)
        self.forJSON = None

        self.columns = '#1'
        self.table = Treeview(self.main_frame, show='headings', columns=self.columns)

        self.collection_table = Listbox(self.main_frame, font=self.font)
        self.scroll = Scrollbar(self.main_frame, orient=VERTICAL, command=self.table.yview)
        self.scrollY = Scrollbar(self.main_frame, orient=HORIZONTAL, command=self.table.xview)
        self.table.configure(yscrollcommand=self.scroll.set, xscrollcommand=self.scrollY.set)

        self.btn = customtkinter.CTkButton()
        self.collection_table.bind("<<ListboxSelect>>", self.callback)
        self.table.bind('<<TreeviewSelect>>', self.callbackTree)

        self.style = ttk.Style(self.main_frame)
        self.style.configure('Treeview', rowheight=70)

        self.data = None
        self.but_delete_json = Button(self.main_frame)
        self.but_update_json = Button(self.main_frame)
        self.but_add_json = Button(self.main_frame)
        self.but_insert_json = Button(self.main_frame)

        if icon:
            self.root.iconbitmap(icon)

    @staticmethod
    def time_string():
        return time.strftime('%H:%M:%S')

    def add_json(self):
        print(self.textJSON.get('1.0', END))
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        js = self.textJSON.get('1.0', END)
        js = js.replace("'", '"')
        z = json.loads(js)
        var_no_ar.insert_one(z)

    def insert_json(self):
        self.but_insert_json.place_forget()
        self.but_add_json.configure(text='Add json', command=self.add_json)
        self.but_add_json.place(x=10, y=550)
        self.table.place_forget()
        print('ok')
        self.textJSON.delete('1.0', END)
        self.scroll.pack_forget()
        self.scrollY.pack_forget()
        self.textJSON.place(x=210, y=0, width=890, height=1000)

    def update_json(self):
        self.but_insert_json.place_forget()
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        strk = self.textJSON.get('1.18', '1.42')
        strf = self.textJSON.get("1.0", "1.1") + self.textJSON.get('1.46', END)
        js = strf.replace("'", '"')
        z = json.loads(js)
        var_no_ar.replace_one({"_id": ObjectId(strk)}, z)
        print('ok')

    def delete_json(self):
        self.but_insert_json.place_forget()
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        strk = self.textJSON.get('1.0', END).split(' ')[1]
        var_no_ar.delete_one({'_id': strk[1:len(strk) - 2]})
        self.textJSON.place_forget()
        self.table.place(x=210, y=0, width=1000, height=1000)
        self.but_delete_json.place_forget()

    def callbackTree(self, event):
        selection = self.table.selection()[0]
        self.but_insert_json.place_forget()
        self.but_delete_json.configure(text='Delete', command=self.delete_json)
        self.but_delete_json.place(x=10, y=350)
        self.but_update_json.place(x=10, y=450)
        self.but_update_json.configure(text='Update', command=self.update_json)
        self.textJSON.delete('1.0', END)
        self.scroll.pack_forget()
        self.scrollY.pack_forget()
        self.forJSON = self.table.item(selection, "values")
        self.textJSON.insert(END, self.table.item(selection, "values"))
        self.table.place_forget()
        self.textJSON.place(x=210, y=0, width=890, height=1000)
        print(self.table.item(selection, "values"))

    def progress(self):
        if self.pb['value'] < 100:
            self.pb['value'] += 20

    def draw_button(self):
        self.button.place(x=500, y=300)

    def sys_com(self):
        self.pb.pack()
        self.pb.start()
        # os.system('curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add - ; echo "deb [ '
        #           'arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | '
        #           'sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list ; echo y | sudo apt install '
        #           'mongodb-org; '
        #           'sudo systemctl start mongod.service; sudo systemctl status mongod; sudo systemctl enable mongod')
        self.pb.stop()
        self.pb.pack_forget()
        # self.label.pack()
        self.mongo_connect()
        # self.label.place(x=50, y=1)
        sys.exit()

    def callback(self, event):
        selection = event.widget.curselection()
        if selection:
            self.table.delete(*self.table.get_children())
            self.scroll.pack(side=RIGHT, fill=Y)
            self.scrollY.pack(fill=X, side=BOTTOM)
            index = selection[0]

            self.data = event.widget.get(index)
            self.table.heading('#1', text=str(self.data))
            var = self.client[self.list_box.get()].get_collection(self.data).find()
            print(self.client[self.list_box.get()].get_collection(self.data))
            self.collection_table.place_forget()

            for col in self.table['column']:
                self.table.column(col, width=20000)
            self.table.update()
            for ind, i in enumerate(var):
                self.table.insert('', END, values=i)
            self.but_insert_json.configure(text="Insert", command=self.insert_json)
            self.but_insert_json.place(x=10, y=550)
            self.table.place(x=210, y=0, width=1000, height=1000)
            self.table.update()

    def create_db(self):
        child_wind = ChildWindow(self.root, 200, 200, 'create')
        child_wind.draw()

    def draw_combo(self):
        self.list_box.configure(values=self.client.list_database_names(), command=self.get_collection, width=200)
        self.list_box.after(5000, self.draw_combo)

    def get_collection(self, ind):
        self.but_insert_json.place_forget()
        self.but_delete_json.place_forget()
        self.but_update_json.place_forget()
        self.table.place_forget()
        self.scroll.pack_forget()
        self.collection_table.configure(listvariable=None)
        self.collection_table.pack()
        print(self.list_box.get())
        self.collection_taken = self.client[self.list_box.get()]
        var = Variable(value=self.collection_taken.list_collection_names())
        self.collection_table.configure(listvariable=var, width=110)
        self.collection_table.place(x=210, y=0, width=1000, height=1000)
        self.but_add_json.place_forget()

    def mongo_connect(self):
        PanedWindow().pack(fill=BOTH)
        self.list_box.configure(values=self.client.list_database_names(), command=self.get_collection, width=200)
        self.add_DB = customtkinter.CTkButton(text='Add DB', command=self.create_db).place(x=10, y=650)
        self.list_box.set('Change')
        self.list_box.place(x=1, y=25)
        self.draw_combo()

    def run(self):
        self.draw_button()
        self.root.mainloop()

    def onclick(self):
        self.button.place_forget()
        self.com.start()


if __name__ == "__main__":
    window = Window(1100, 750, "MongoDB by Pishexod")
    window.run()
