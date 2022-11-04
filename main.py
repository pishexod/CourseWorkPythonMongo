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


# import bson


class Window:
    def __init__(self, width, height, title="MyWindow", resizable=(False, False), icon=None):

        self.dbBut = None
        self.client = MongoClient()

        self.root = customtkinter.CTk()

        self.add_DB = None
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+400+150")
        self.root.resizable(resizable[0], resizable[1])
        customtkinter.set_default_color_theme('dark-blue')
        customtkinter.set_appearance_mode('dark')
        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1, side=RIGHT)

        self.list_box = customtkinter.CTkComboBox(self.main_frame)
        self.font = Font(size=20)
        self.collection_taken = None

        self.pb = customtkinter.CTkProgressBar(self.main_frame)
        self.com = Thread(target=self.sys_com)

        self.button = customtkinter.CTkButton(self.main_frame, text="Download", command=self.onclick, width=100,
                                              height=50)

        self.textJSON = customtkinter.CTkTextbox(self.main_frame, text_font=30)
        self.forJSON = None

        self.columns = '#1'
        self.table = Treeview(self.main_frame, show='headings', columns=self.columns)

        self.banner = customtkinter.CTkLabel(text='Select DB', text_font=20)

        self.collection_table = Listbox(self.main_frame, font=self.font, bg='#434343', fg='#C0C0C0', bd=0)
        self.scroll = customtkinter.CTkScrollbar(self.main_frame, command=self.table.yview)
        self.scrollY = customtkinter.CTkScrollbar(self.main_frame, orientation="horizontal",
                                                  command=self.table.xview)
        self.table.configure(yscrollcommand=self.scroll.set,
                             xscrollcommand=self.scrollY.set)

        self.btn = customtkinter.CTkButton(self.main_frame)
        self.collection_table.bind("<Double-1>", self.callback)
        self.table.bind('<<TreeviewSelect>>', self.callbackTree)

        self.style = ttk.Style(self.main_frame)
        # self.style.theme_use()
        self.style.configure('Treeview', rowheight=70, background='#434343', fieldbackground='#434343',
                             foreground='white')

        self.data = None
        self.but_delete_json = customtkinter.CTkButton(self.main_frame)
        self.but_update_json = customtkinter.CTkButton(self.main_frame)
        self.but_add_json = customtkinter.CTkButton(self.main_frame)
        self.but_insert_json = customtkinter.CTkButton(self.main_frame)

        self.but_add_collection = customtkinter.CTkButton(self.main_frame, text='Add collection',
                                                          command=self.add_collection)
        self.drop_db = customtkinter.CTkButton(self.main_frame, command=self.del_db, text='Drop DB')
        self.drop_collection = customtkinter.CTkButton(self.main_frame, command=self.del_collection,
                                                       text='Drop collection')

        self.img = PhotoImage(file='/home/pishexod/PycharmProjects/OS/img/icons8-back-arrow-30.png', width=30,
                              height=30)
        self.but_back = customtkinter.CTkButton(self.main_frame, command=self.back_def, text='', image=self.img,
                                                height=20, width=20)
        self.but_back_for_table = customtkinter.CTkButton(self.main_frame, image=self.img, text='', height=20, width=20,
                                                          command=self.back_def_for_table)
        if icon:
            self.root.iconbitmap(icon)

    @staticmethod
    def time_string():
        return time.strftime('%H:%M:%S')

    def back_def_for_table(self):
        self.collection_table.update()
        self.but_back_for_table.place_forget()
        self.but_insert_json.place_forget()
        self.but_delete_json.place_forget()
        self.but_update_json.pack_forget()
        self.but_add_json.place_forget()
        self.collection_table.place(x=210, y=0, width=1000, height=1000)
        self.table.place_forget()

    def back_def(self):
        self.table.update()
        self.but_back_for_table.place(x=175, y=98)
        self.but_back.place_forget()
        self.but_update_json.place_forget()
        self.but_delete_json.place_forget()
        self.but_insert_json.place(x=30, y=550)
        self.textJSON.place_forget()
        self.table.place(x=210, y=0, width=1000, height=1000)

    def del_collection(self):
        print('ok')
        child_wind = ChildWindow(self.root, 200, 200, 'create')
        child_wind.draw_for_drop()

    def del_db(self):
        print('ok')
        child_wind = ChildWindow(self.root, 200, 200, 'create')
        child_wind.draw_for_drop_db()

    def add_json(self):
        print(self.textJSON.textbox.get('1.0', END))
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        js = self.textJSON.textbox.get('1.0', END)
        js = js.replace("'", '"')
        z = json.loads(js)
        var_no_ar.insert_one(z)

    def insert_json(self):
        self.but_back_for_table.place_forget()
        self.but_back.place(x=175, y=98)
        self.but_insert_json.place_forget()
        self.but_add_json.configure(text='Add json', command=self.add_json)
        self.but_add_json.place(x=30, y=550)
        self.table.place_forget()
        self.textJSON.textbox.delete('1.0', END)
        self.scroll.pack_forget()
        self.scrollY.pack_forget()
        self.textJSON.place(x=210, y=0, width=890, height=1000)

    def update_json(self):
        self.but_insert_json.place_forget()
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        strk = self.textJSON.textbox.get('1.18', '1.42')
        strf = self.textJSON.textbox.get("1.0", "1.1") + self.textJSON.textbox.get('1.46', END)
        js = strf.replace("'", '"')
        z = json.loads(js)
        var_no_ar.replace_one({"_id": ObjectId(strk)}, z)
        print('ok')

    def delete_json(self):
        self.but_insert_json.place_forget()
        var_no_ar = self.client[self.list_box.get()].get_collection(self.data)
        strk = self.textJSON.textbox.get('1.18', '1.42')
        var_no_ar.delete_one({'_id': ObjectId(strk)})
        self.textJSON.place_forget()
        self.table.delete(*self.table.get_children())
        self.scroll.pack(side=RIGHT, fill=Y)
        self.scrollY.pack(side=BOTTOM, fill=X)
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
        self.table.update()
        self.table.place(x=210, y=0, width=1000, height=1000)
        self.but_delete_json.place_forget()

    def callbackTree(self, event):
        selection = self.table.selection()[0]
        self.but_insert_json.place_forget()
        self.but_delete_json.configure(text='Delete', command=self.delete_json)
        self.but_delete_json.place(x=30, y=350)
        self.but_update_json.place(x=30, y=450)
        self.but_update_json.configure(text='Update', command=self.update_json)
        self.textJSON.textbox.delete('1.0', END)
        self.scroll.pack_forget()
        self.scrollY.pack_forget()
        self.forJSON = self.table.item(selection, "values")
        self.textJSON.textbox.insert(END, self.table.item(selection, "values"))
        self.but_back_for_table.place_forget()
        self.table.place_forget()
        self.textJSON.place(x=210, y=0, width=890, height=1000)
        self.but_back.place(x=175, y=98)
        print(self.table.item(selection, "values"))

    def progress(self):
        if self.pb['value'] < 100:
            self.pb['value'] += 20

    def draw_button(self):
        self.button.place(x=500, y=300)

    def sys_com(self):
        self.pb.place(x=450, y=350)
        self.pb.start()
        # os.system('curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add - ; echo "deb [ '
        #           'arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | '
        #           'sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list ; echo y | sudo apt install '
        #           'mongodb-org; '
        #           'sudo systemctl start mongod.service; sudo systemctl status mongod; sudo systemctl enable mongod')
        self.pb.stop()
        self.pb.place_forget()
        self.mongo_connect()
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
            self.but_insert_json.place(x=30, y=550)
            self.table.place(x=210, y=0, width=1000, height=1000)
            self.but_back_for_table.place(x=175, y=98)
            self.table.update()

    def create_db(self):
        child_wind = ChildWindow(self.root, 200, 200, 'create')
        child_wind.draw()

    def draw_combo(self):
        self.list_box.configure(values=self.client.list_database_names(), command=self.get_collection, width=200)
        self.list_box.after(5000, self.draw_combo)

    def get_collection(self, ind):
        self.but_back_for_table.place_forget()
        self.but_back.place_forget()
        self.but_insert_json.place_forget()
        self.but_delete_json.place_forget()
        self.but_update_json.place_forget()
        self.table.place_forget()
        self.scroll.pack_forget()
        self.collection_table.configure(listvariable=None)
        self.collection_table.pack()
        self.banner.place_forget()
        self.collection_taken = self.client[self.list_box.get()]
        var = Variable(value=self.collection_taken.list_collection_names())
        self.collection_table.configure(listvariable=var, width=110, borderwidth=0, highlightthickness=0, border=0,
                                        background='#434343')
        self.collection_table.place(x=210, y=0, width=1000, height=1000)
        self.but_add_json.place_forget()

    def add_collection(self):
        child_wind = ChildWindow(self.root, 200, 200, 'create')
        child_wind.draw_for_db()
        print('ok')

    def mongo_connect(self):
        PanedWindow().pack(fill=BOTH)
        self.list_box.configure(values=self.client.list_database_names(), command=self.get_collection, width=200)
        self.add_DB = customtkinter.CTkButton(self.main_frame, text='Add DB', command=self.create_db).place(x=30, y=650)
        self.but_add_collection.place(x=30, y=620)
        self.banner.place(x=600, y=300)
        self.list_box.set('Change')
        self.drop_db.place(x=30, y=100)
        self.drop_collection.place(x=30, y=130)
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
