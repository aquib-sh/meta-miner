""" 
Author: Shaikh Aquib

This is the Main class where we will initialize our Meta-Miner application and integrate it with reader, writer and user_interface classes.

"""

from user_interface import Application
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image

def test():
    pass

class Main():

    def __init__(self):
        self.obj = Application("700x400")
        self.obj.set_title("Meta-Miner")
        self.obj.set_icon("res\\icon.ico")

        self.spaces = "                                 \n\n "
        self.txt = """
        In our research and coaching on career reorientation, 
        we’ve witnessed many people struggling to explain what they want to do next and why a 
        change makes sense. One of us, in the context of writing a book, 
        has studied a wide variety of major career shifts; the other has worked extensively 
        with organizations and individuals on the use of narrative to bring about positive change. 
        Each of us has been to enough networking events to know that the one we’ve described here is not unusual. 
        But we’ve also seen a lot of people in the midst of significant transitions make effective use of contacts 
        and successfully enlist supporters. What we’ve come to understand 
        is that one factor more than any other makes the difference: the ability to craft a good story. """

        # Getting the root of Application class for flexibility
        self.root = self.obj.return_root()
        
        self.frame = self.obj.create_frame(350,690,1,0)
        self.canvas = Canvas(self.frame)
    
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
        object_list = Listbox(self.frame,yscrollcommand=scrollbar.set)
        for element in elements:
            object_list.insert(END,element)
        object_list.pack(side=TOP)
        return object_list

    def image_create(self,path):
        img = ImageTk.PhotoImage(Image.open(path).resize((200,200)))
        return img

    def update_image(self,image_object,new_image_path):
        img = self.image_create(new_image_path)
        self.root.img = img
        self.canvas.itemconfigure(image_object,image=img)

    def create_scrollbar(self,orientation="vertical"):
        if orientation == "vertical":
            bar = Scrollbar(self.frame,orient=VERTICAL)
            bar.pack(side=RIGHT,fill=Y)
            bar.config(command=self.canvas.yview)

        if orientation == "horizontal":
            bar = Scrollbar(self.frame,orient=HORIZONTAL)
            bar.pack(side=BOTTOM,fill=X)
            bar.config(command=self.canvas.xview)
        return bar

    def setup_canvas(self):
        """ Adds a frame and inside it displays image preview and meta-data in a scrollbar"""
        elements_dict = {}

        vbar = self.create_scrollbar()
        self.canvas.config(height=2000,width=690,scrollregion=(0,0,690,2000),yscrollcommand=vbar.set)
        self.canvas.pack()
        
        img = self.image_create(r"D:\Projects\meta-miner\res\test_cases\Images\f18257920.jpg")
        #precautions due to stupid feature of garbage collection in python
        self.root.img = img 
        
        self.canvas.config(background="grey")
        self.canvas.create_image(320,100,image=img)
        self.canvas.create_text(350,500,text=self.txt,font="Times 18 italic bold",fill="white",width=500)
        elements_dict["image"] = img

        return elements_dict

    # Create canvas and all the images and text to it

    def end(self):
        self.obj.mainloop()
    
if __name__ == "__main__":
    app = Main()
    app.menu()
    app.entry()
    canvas_elements = app.setup_canvas()
    if("image" in canvas_elements):
        app.update_image(canvas_elements["image"],r"D:\Projects\meta-miner\res\test_cases\Images\f0820608.jpg")
    app.end()
