""" 
Author: Shaikh Aquib

This is the Main class where we will initilize our Meta-Miner application.and integrate it with reader, writer and user_interface classes.

"""

from user_interface import Application
from tkinter import *
from tkinter import ttk

def test():
    pass

class Main:
    def __init__(self):
        self.obj = Application("700x400")
        self.obj.set_title("Meta-Miner")
        self.obj.set_icon("res\\icon.ico")
        self.spaces = "                                 \n\n "
        self.txt = """In our research and coaching on career reorientation, we’ve witnessed many people struggling to explain what they want to do next and why a change makes sense. One of us, in the context of writing a book, has studied a wide variety of major career shifts; the other has worked extensively with organizations and individuals on the use of narrative to bring about positive change. Each of us has been to enough networking events to know that the one we’ve described here is not unusual. But we’ve also seen a lot of people in the midst of significant transitions make effective use of contacts and successfully enlist supporters. What we’ve come to understand is that one factor more than any other makes the difference: the ability to craft a good story. """
        

    def menu(self):
        elements = {}
        # First create an empty menu for using it as bar in for further submenu
        bar = self.obj.add_menu("File",elements)
        # Add menu options in the form of dictionary
        menu = self.obj.add_menu("Export",{"HTML":test,"JSON":test,"PDF":test,"Text":test},handle=bar)
        

    def entry(self):
        self.obj.add_entry(60,0,0,spaces=35)
        browse_button = self.obj.add_button("Browse",0,1,is_entry_button=True)


    def list_(self,frame,scrollbar,elements):
        object_list = Listbox(frame,yscrollcommand=scrollbar.set)
        for element in elements:
            object_list.insert(END,element)
        object_list.pack(side=TOP)
        return object_list


    def setup_frame(self):
        """ Adds a frame and inside it displays image preview and meta-data in a scrollbar"""
        lbl = Label(self.obj,text=self.spaces)
        lbl.grid(row=0,column=3)

        frame = self.obj.create_frame(350,690,1,0)

        image_lbl = self.obj.create_image_label("D:\\Projects\\meta-miner\\res\\test_cases\\Images\\f0817152.jpg",master=frame)
        lbl = Label(frame,text=self.txt,wraplength=300,justify=CENTER)
        lbl.pack()

        sb = ttk.Scrollbar(frame)
        #listbox = self.list_(frame,sb,[lbl,image_lbl])
        sb.config(command=[image_lbl,lbl])
        sb.pack(side=RIGHT,fill=Y)
        #sb.config(command=listbox.yview)
        self.obj.mainloop()
    
if __name__ == "__main__":
    app = Main()
    app.menu()
    app.entry()
    app.setup_frame()