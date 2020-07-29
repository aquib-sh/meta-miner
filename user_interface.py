
""" 
Application User Interface 
Author: Shaikh Aquib
    
User-Interface class for Meta-Miner

Param: size (String) 
       (Window size for the application example("500x500"))

Functions: set_title        - Sets title of window.
           set_icon         - Sets icon of the window.
           add_menu         - Creates menu or submenu.
           add_entry        - Adds an entry widget.
           add_button       - Adds button on specified position
"""


from tkinter import *
from tkinter import ttk

class Application(Tk):
    def __init__(self,size):
        super().__init__()
        self.geometry(size)


    # Sets title of window
    def set_title(self,title):
        self.title(title)


    # Sets icon for window
    def set_icon(self,path):
        self.iconbitmap(False,path)


    # Adds menu to the window or pre-existing menus
    def add_menu(self,name,element_list=None,handle=None):

        """ element_list = {'name':command_to_execute}
            element_list is a dictionary of all the menu items to be added
            where name of item is key and associated function is value
            handle is the menu on which we want to build our new menu, 
            It is use to create nested menus, by default it is kept off """      
        
        # tearOff is the appreance of ---- before the menu elements
        # It looks ugly so better keep it off
        self.option_add('*tearOff', False)
        
        """ If handle is not present then it will create a new menubar
            and set it as the default menu bar here, if handle is present
            it will use that handle as menubar and create menu on top of that """
        
        if(handle == None):
            menu_bar = Menu(self)
            self.config(menu=menu_bar)
        else:
            menu_bar = handle

        file_ = Menu(menu_bar)
        menu_bar.add_cascade(menu=file_,label=name)
        
        if(element_list != None):
            for lab,fun in element_list.items():
                file_.add_command(label=lab,command=fun)
        # Return menu object
        return file_


    # Adds entry widget or single line text field
    def add_entry(self,width_,row_,column_,spaces=0):

        """ Spaces are used to create an adjustment for entry widget 
            if spaces are present they will be added in order to shift
            entry widget to right"""

        entry = ttk.Entry(self,width=width_)
        spaces_ = ""
 
        if(spaces > 0):
            for i in range(0,spaces):
                spaces_+=" "
            lbl = Label(self,text=spaces_)
            lbl.grid(row=0,column=0)
            entry.grid(row=row_,column=column_+1)
        else:
            entry.grid(row=row_,column=column_)

    # Adds button on the specified position
    def add_button(self,name,row_,column_,is_entry_button = False):
        button = ttk.Button(self,text=name)
        """ if is_entry_button=True extra 1 column is added to occupy the 
            empty spaces in column 0"""
        if(is_entry_button):
            button.grid(row=row_,column=column_+1)
        else:
            button.grid(row=row_,column=column_)
        return button


#--------------------------------------TESTING---------------------------------------------------
def test():
    pass

if __name__ == "__main__":
    obj = Application("700x400")
    obj.set_title("Meta-Miner")
    obj.set_icon("res\\icon.ico")

    elements = {}
    # First create an empty menu for using it as bar in for further submenu
    bar = obj.add_menu("File",elements)
    menu = obj.add_menu("Export",{"HTML":test,"JSON":test,"PDF":test,"Text":test},handle=bar)

    obj.add_entry(60,0,0,spaces=35)
    browse_button = obj.add_button("Browse",0,1,is_entry_button=True)

    obj.mainloop()