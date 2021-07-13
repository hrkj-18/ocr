# Simple enough, just import everything from tkinter.
from tkinter import *
import cv2
import sys
import os
from tkinter.font import Font
from tkinter import filedialog
import tkinter as tk
from tkinter import Tk, Text, Scrollbar, Menu, messagebox, filedialog, BooleanVar, Checkbutton, Label, Entry, StringVar, Grid, Frame
import os, subprocess, json, string



#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):
        frame = Frame(root)
        #myFont = Font(family="Times New Roman", size=12)
        
        self.yscrollbar = Scrollbar(ctr_right, orient="vertical")
        self.yscrollbar.pack(side="right", fill="y")
        self.editor = Text(ctr_right ,yscrollcommand=self.yscrollbar.set)
        self.editor.pack(side="right")
        self.editor.config( wrap = "word", # use word wrapping
               undo = True, # Tk 8.4 
               width = 80, 
               height= 80,
               #font=myFont
               )        
        self.editor.focus()
        
        self.yscrollbar.config(command=self.editor.yview)        
        #frame.pack(fill="both", expand=1)
        
 

        ############################################################################################
        # changing the title of our master widget      
        self.master.title("OCR APP")

        # allowing the widget to take the full space of the root window
        #self.pack(fill=BOTH, expand=1)
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        filemenu = Menu(menu)

    

        #added "file" to our menu
        #filemenu = Menu(self.menubar, tearoff=0)# tearoff = 0 => can't be seperated from window
        #filemenu.add_command(label="New", underline=1, command=self.client_exit, accelerator="Ctrl+N")
        filemenu.add_command(label="Open...", underline=1, command=self.file_open)
        filemenu.add_command(label="Save", underline=1, command=self.file_save)
        filemenu.add_command(label="Save As...", underline=5, command=self.file_save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=2, command=self.client_exit)
        menu.add_cascade(label="File", menu=filemenu)


        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Select Image",underline=1, command=self.showImg)
        edit.add_command(label="Process", command=self.shellscript)
        #edit.add_command(label="New", underline=1, command=self.client_exit)
        edit.add_command(label="Refresh", command=self.Refresh)

        #added "file" to our menu
        menu.add_cascade(label="Image", menu=edit)   
    def save_if_modified(self, event=None):
        if self.editor.edit_modified(): #modified
            response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?") #yes = True, no = False, cancel = None
            if response: #yes/save
                result = self.file_save()
                if result == "saved": #saved
                    return True
                else: #save cancelled
                    return None
            else:
                return response #None = cancel/abort, False = no/discard
        else: #not modified
            return True     
    def file_open(self, event=None, filepath=None):
        result = self.save_if_modified()
        if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            if filepath == None:
                filepath = filedialog.askopenfilename()
                #filepath="hi.txt"
            if filepath != None  and filepath != '':
                with open(filepath, encoding="utf-8") as f:
                    fileContents = f.read()# Get all the text from file.           
                # Set current text to file contents
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, fileContents)
                self.editor.edit_modified(False)
                self.file_path = filepath

    def imgDestroy(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath=self.file_path)
        return result
    def file_save_as(self, event=None, filepath=None):
        if filepath == None:
            filepath = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
        try:
            with open(filepath, 'wb') as f:
                text = self.editor.get(1.0, "end-1c")
                f.write(bytes(text, 'UTF-8'))
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "saved"
        except FileNotFoundError:
            print('FileNotFoundError')
            return "cancelled"
    def showImg(self):
        
        filename = filedialog.askopenfilename(title = "Select file",filetypes = (("image files","*.jpg *.jpeg *.png"),("all files","*.*"))) 
        #call for mouse click crop 
        os.system('python m.py --image '+filename)

        load = Image.open("/home/simran/Desktop/OCR_APP2/bw_cropped.jpg")
        w, h = load.size
        f1 = 1.0*500/w  # 1.0 forces float division in Python2
        f2 = 1.0*500/h
        factor = min([f1, f2])
        #print(f1, f2, factor)  # test
        # use best down-sizing filter
        width = int(w*factor)
        height = int(h*factor)
        load = load.resize((width, height), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(ctr_left, image=render,bg = "black")
        img.image = render
        img.place(x=100, y=50)
        
        #call for line segmentation --input is bw_cropped saved image
        os.system('python lineseg.py')
        os.system('python textseg.py')
        os.system('python seg2.py')
        os.system('python char_padding.py')
        os.system('python char_binarize.py')

        #self.file_open(None,"/home/simran/Desktop/OCR_APP2/input.txt")
    def shellscript(self, event=None):
        os.system('bash gg.sh')
        self.file_open(None,"/home/simran/Desktop/OCR_APP2/output.txt")
    def file_quit(self, event=None):
        result = self.save_if_modified()
        if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            self.root.destroy() #sys.exit(0)
    
    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        
    
    def undo(self, event=None):
        self.editor.edit_undo()
        
    def redo(self, event=None):
        self.editor.edit_redo()   
 
    def Refresh(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
    def client_exit(self):
        exit()



# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry('%dx%d+0+0' % (width,height))

# create all of the main containers
frame = Frame(root, bg='lavender', width=450, height=50, pady=3)
center = Frame(root, bg='gray2', width=60, height=40, padx=3, pady=3)
btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)
btm_frame2 = Frame(root, bg='lavender', width=450, height=45, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

#frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
#btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")
# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, bg='white', width=700, height=190,padx=3)
ctr_right = Frame(center, bg='white', width=800, height=190, padx=3, pady=3)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_right.grid(row=0, column=1, sticky="nsew")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  
