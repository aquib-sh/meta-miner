""" 
Author: Shaikh Aquib

This is the Main class where we will initialize our Meta-Miner application and integrate it with reader, writer and user_interface classes.

"""

from user_interface import Application
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from reader import MetaReader
from writer import MetaWriter
from PIL import ImageTk,Image

def test():
    pass

class Main():

    def __init__(self):
        self.obj = Application("700x400")
        self.obj.set_title("Meta-Miner")
        self.obj.set_icon("res\\icon.ico")
        
        self.spaces = "                                 \n\n "
        self.txt = ""

        self.DEFAULT_TEXT_POSITION = (350,460)
        self.INTERMEDIATE_TEXT_POSITION = (350,550)
        self.EXPANDED_TEXT_POSITION = (350, 880)

        # Getting the root of Application class for flexibility
        self.root = self.obj.return_root()
        self.root.resizable(False,False)

        self.frame = self.obj.create_frame(350,690,1,0)
        self.canvas = Canvas(self.frame)

        # Gets the path of the file currently opened
        self.current_filename = ""

        # Gets some variable for function transfers
        self.elements_dict = {}
        self.entry_ = self.obj.add_entry(60,0,0,spaces=35)

        self.img = self.image_create(r"res\icon.png")
       
        #precautions due to stupid feature of garbage collection in python
        self.root.img = self.img
        self.canvas_text = Text(self.canvas) 
        self.img_obj = self.canvas.create_image(320,100,image=self.img,state="hidden")
        self.text_obj = self.canvas.create_text(self.DEFAULT_TEXT_POSITION,text=self.txt,font=("system",16,"bold"),fill="white",width=500,anchor="center",state="hidden")

        self.image_extensions = ['jpeg','jpg','png','gif','tif']
        self.canvas.pack_forget()
        

    def menu(self):
        elements = {}
        # First create an empty menu for using it as bar in for further submenu
        bar = self.obj.add_menu("File",elements)

        # Add menu options in the form of dictionary
        menu = self.obj.add_menu("Export",{"HTML":test,"JSON":test,"PDF":test,"Text":test},handle=bar)
        

    # Opens up the file choosing dailogbox    
    def open_file_chooser(self):
        """ Does all the stuff necessary once the browse button is clicked 
            1> Gets the file path
            2> Displays preview if the file is an image
            3> Displays metadata
        """

        self.canvas.pack(fill=Y,expand=True)
        # Opens up a file choose dialog box
        self.current_filename = filedialog.askopenfilename(initialdir="C:\\Users\\.*\\Pictures",title="Select a file",filetypes=(("all files",".*.*"),))
        
        # Delete whatever is in there already
        self.entry_.delete(0,END)

        # Insert the path of file in entrybox
        self.entry_.insert(0,str(self.current_filename))

        # If the file is an image we will display its's preview
        is_image = self.is_image(self.current_filename)
        if is_image != None:
            self.display_image(self.current_filename)

        # Display the meta-data content
        self.display_data(self.current_filename)


    def display_image(self,file_path):
        """ If the file is an image then display its's preview. """
        self.update_image(self.img_obj, file_path)
        self.canvas.itemconfigure(self.img_obj, state="normal")

    
    def display_data(self,file_path):
        """ Display the meta-data of the file. 
            If the text is too long then shift the co-ordinates by using
            toward y axis by using expanded co-ordinates
            so that it doesn't punches on the image."""
        text_ = self.get_metadata(file_path)
        self.canvas.itemconfigure(self.text_obj, text=text_, state="normal")
        length = len(text_)
        if length > 2000:
            self.canvas.coords(self.text_obj,self.EXPANDED_TEXT_POSITION)
        elif length > 1000:
            self.canvas.coords(self.text_obj,self.INTERMEDIATE_TEXT_POSITION)
        else:
            self.canvas.coords(self.text_obj,self.DEFAULT_TEXT_POSITION)


    # Check if the file is an image
    def is_image(self,path):
        if len(path) == 0:
            return None
        p = path.split("/")
        name = p[len(p) -1].split(".")[1]
        if name in self.image_extensions:
            return True
        return False


    def browse(self):
        browse_button = self.obj.add_button("Browse",0,1,is_entry_button=True)
        browse_button.config(command=self.open_file_chooser)
        

    # Creates image object
    def image_create(self,path):
        """ Creates the ImageTk.PhotoImage object. """

        img = ImageTk.PhotoImage(Image.open(path).resize((200,200)))
        return img


    def update_image(self,image_object,new_image_path):
        """ Updates image based on path and canvas.create_image object. """

        img = self.image_create(new_image_path)
        self.root.img = img
        obj = self.canvas.itemconfigure(image_object,image=img)
        self.elements_dict["image"] = obj


    def create_scrollbar(self,orientation="vertical"):
        """ Adds a scrollbar depending upon whether horizontal is requested or vertical. """
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
        """ Adds a frame and inside it displays image preview and meta-data in a scrollbar. """
        
        vbar = self.create_scrollbar()
        self.canvas.config(height=2000,width=690,scrollregion=(0,0,690,2000),yscrollcommand=vbar.set)
        self.canvas.config(background="grey")
        
        self.elements_dict["image"] = self.img_obj

        return self.elements_dict


    def get_metadata(self,file):
        global reader_
        reader_ = MetaReader(file)
        data = reader_.get_dict()
        text = ""

        for key,value in data.items():
            text += "{} : {}\n".format(key,value)
        
        return text

    # Create canvas and all the images and text to it
    def end(self):
        self.obj.mainloop()
    
if __name__ == "__main__":
    app = Main()
    app.menu()
    app.browse()
    canvas_elements = app.setup_canvas()

    app.end()

"""
        a = ttk.Button(self.canvas,text="Asad",command=lambda: self.update_image(img_obj,r"D:\Projects\meta-miner\res\test_cases\Images\f0820608.jpg"))
        b = ttk.Button(self.canvas,text="Zahid",command=lambda: self.update_image(img_obj,r"D:\Projects\meta-miner\res\test_cases\Images\f0818368.jpg"))

        button_window = self.canvas.create_window(30,10,window=a)
        button_window2 = self.canvas.create_window(500,10,window=b)

"""