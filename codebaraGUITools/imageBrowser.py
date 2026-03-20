# Python program to create 
# a file explorer in Tkinter
 
# import all components
# from the tkinter library
from tkinter import Tk, Button, Listbox,Frame, Label, PhotoImage
import tarfile
import os
import json
import pathlib
from PIL import Image
from codebara.config import CARD_FILE_EXTENSION
from codebara.tools import getSha256FromFile
# import filedialog module
from tkinter import filedialog
TEMP_DIRECTORY='./tmp/gui/'

class ImageBrowser:
    listValues:list=[]
    directory:str=str(pathlib.Path.cwd())
    def openfolder(self):
        print('open folder')
        self.directory=filedialog.askdirectory(initialdir= self.directory, title='base de navigation', mustexist = True, parent=self.window)
        #self.l_folder.config(text=self.directory)
        self._refreshList()
    def quit(self):
        print('quit')
        p=pathlib.Path(TEMP_DIRECTORY)
        if p.is_dir() is True:
               p.rmdir()
        quit()
    def destroyTemp(self):
        print('destroy temp')
    def selectOnList(self,a):
        print('select onList')
        selected:str=self.listFiles.selection_get()
        if selected=='..':
            print('parent dir')
            self.directory=self.directory[0:self.directory.rindex('/')]
            self._refreshList()
        else:
            p=pathlib.Path(self.directory+'/'+selected)
            if p.is_dir():
                self.directory+='/'+selected
                self._refreshList()
            #elif selected.endswith('tar.gz'):
            elif selected.endswith(CARD_FILE_EXTENSION) or selected.endswith('tar.gz'):
                self._openCardFile(self.directory+'/'+selected)
    def _openCardFile(self, filename):
        print('open card')
        folder='./tmp/GUI'
        with tarfile.open(filename,'r') as f:
            p=pathlib.Path(folder)
            if p.is_dir() is False:
               p.mkdir(parents=True)
            f.extractall(path=p)
        hashsResults={'front':False,'perso':False,'back':False, 'datas':False}
        filehash=getSha256FromFile(filename)
        print(filehash)
        with open(folder+'/hashs.json') as j:
            #s:str=j.read()
            hash=json.load(j)
            hashsResults={
                'front':getSha256FromFile(folder+'/front.png')==hash['front'],
                'perso':getSha256FromFile(folder+'/perso.png')==hash['perso'],
                'back': getSha256FromFile(folder+'/back.png')==hash['back'],
                'datas':getSha256FromFile(folder+'/datas.json')==hash['datas']
            }
            #self.fileCheck.config(background='GREEN' if hashsResults['front'] else 'RED')
            self.frontCheck.config(background='GREEN' if hashsResults['front'] else 'RED')
            self.backCheck.config(background='GREEN' if hashsResults['back'] else 'RED')
            self.persoCheck.config(background='GREEN' if hashsResults['perso'] else 'RED')
            self.datasCheck.config(background='GREEN' if hashsResults['datas'] else 'RED')
            print(hashsResults)

        image = Image.open('./tmp/GUI/front.png')
        image.resize((400, 700)).save('./tmp/GUI/front.png')
        imagef = PhotoImage(file='./tmp/GUI/front.png')        
        self.imagef_label.config(image=imagef)
        image = Image.open('./tmp/GUI/back.png')
        image.resize((400, 700)).save('./tmp/GUI/back.png')
        imageb=PhotoImage(file='./tmp/GUI/back.png')
        self.imageb_label.config(image=imageb)
        imagec=PhotoImage(file='./tmp/GUI/perso.png')
        self.imagec_label.config(image=imagec)
        with open('./tmp/GUI/datas.json') as j:
            s:str=j.read()
            self.label_data_explorer.config(text=s.encode('utf-8'))
        
        # Change label contents
        #label_file_explorer.configure(text="File Opened: "+filename)
        self.l_folder.config(text=filename)
    def _refreshList(self):
        print('refresh')
        self.l_folder.config(text=self.directory)
        self.listFiles.delete(0,len( self.listValues)-1)
        self.listValues=[{"value":"..", "type":'dir'}]
        self.listFiles.insert(0,'..')
        i=1
        for f in os.listdir(self.directory):
            p=pathlib.Path(self.directory+'/'+f)
            if p.is_dir(): # si f est un dossier
                self.listValues.append({"value":f, "type":'dir'})
                self.listFiles.insert(i,f)
                
            elif f.endswith(CARD_FILE_EXTENSION) or f.endswith('.tar.gz'):
                self.listValues.append({"value":f, "type":'file'})
                self.listFiles.insert(i,f)
                
                # Traitement sur le fichier f
            i+=1
    def show(self):    
        self.window=Tk()
        self.window.title('File Explorer')
        self.window.config(background='white')
        self.window.geometry("1024x1024")

        """buttonsFrame=Frame(self.window, height=50)
        buttonsFrame.place(relx=5, rely=0, relwidth=1, height=40)
        """
        self.b_open=Button(self.window, text="OpenFolder",command=self.openfolder )
        self.b_open.place(relx=0.25, y=5, height=20, relwidth=0.15)

        self.b_exit=Button(self.window, text="Exit",command=quit )
        self.b_exit.place(relx=0.6, y=5, height=20, relwidth=0.15)
        self.l_folder=Label(self.window, text=self.directory)
        self.l_folder.place(relx=0.01, y=27, height=20, relwidth=0.98)
        """centralFame=Frame(window)
        centralFame.place(relx=0, rely=0.1, relwidth=1,relheight=0.8)"""

        self.listFiles=Listbox(self.window, font=("Helvetica", 15))
        self.listFiles.bind('<Double-1>', self.selectOnList)
        self.listFiles.place(x=0.08,y=55, relwidth=0.3,relheight=0.87 )
        self.centralRightFrame=Frame(
            master=self.window, bd=3, cursor='hand2', 
            highlightcolor='red',
            highlightbackground='black',
            highlightthickness=2, pady=10
        )
        self.centralRightFrame.place(relx=0.315, y=55, relwidth=0.65, height=790)

        #center

        self.imagec_label = Label(self.centralRightFrame, text='center', width=384, height=256)
        self.imagec_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.imagec_label.grid(column=1,row=3)

        #front
        self.imagef_label = Label(self.centralRightFrame, text='image', width=500)
        self.imagef_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.imagef_label.grid(column=2,row=3)

        #back

        self.imageb_label = Label(self.centralRightFrame, text='image', width=500)
        self.imageb_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.imageb_label.grid(column=3,row=3)

        self.checkFrame=Frame(self.window, bd=4, pady=10, padx=10)
        self.checkFrame.place(relx=0.315, y=855, relwidth=0.65,height=155)
        
        self.checksum=Label(self.checkFrame, text="checksum",font=("Helvetica", 20))
        self.checksum.grid(column=1, row=1, columnspan=7)
        self.fileCheck=Label(self.checkFrame, text="file", background='RED',pady=5, padx=10, font=("Helvetica", 15), width=100)
        self.fileCheck.grid(column=1, row=2, columnspan=7)
        self.empty=Label(self.checkFrame, text=" ",font=("Helvetica", 10), width=10)
        self.empty.grid(column=1, row=3, columnspan=7)
        self.persoCheck=Label(self.checkFrame, text="perso", background='RED',pady=5, font=("Helvetica", 15), width=30)
        self.persoCheck.grid(column=1, row=4)
        self.empty2=Label(self.checkFrame, text=" ",font=("Helvetica", 10), width=10)
        self.empty2.grid(column=2, row=4)
        
        self.frontCheck=Label(self.checkFrame, text="front", background='RED',pady=5, font=("Helvetica", 15), width=30)
        self.frontCheck.grid(column=3, row=4)
        self.empty3=Label(self.checkFrame, text=" ",font=("Helvetica", 10), width=10)
        self.empty3.grid(column=4, row=4)
        self.backCheck=Label(self.checkFrame, text="back", background='RED',pady=5, font=("Helvetica", 15), width=30)
        self.backCheck.grid(column=5, row=4)
        self.empty4=Label(self.checkFrame, text=" ",font=("Helvetica", 10), width=10)
        self.empty4.grid(column=6, row=4)
        self.datasCheck=Label(self.checkFrame, text="datas", background='RED',pady=5, font=("Helvetica", 15), width=30)
        self.datasCheck.grid(column=7, row=4)
        
        self.label_data_explorer = Label(self.window, 
                                    text = "card data",bd=3, cursor='hand2', 
                                    highlightcolor='red',
                                    highlightbackground='black',
                                    highlightthickness=2, pady=10,wraplength=800, 
                                    font=("Helvetica", 22)) 
        #label_data_explorer.pack()
        self.label_data_explorer.place(relx=0.315, y=1000, relwidth=0.65,height=150)

        
        self._refreshList()
        self.window.mainloop()
    def __init__(self):
        print("inti")