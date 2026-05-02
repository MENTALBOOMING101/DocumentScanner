from tkinter import *
from tkinter import ttk , messagebox,Toplevel,filedialog
from PIL import ImageTk,Image
from documentscanner import documentScanner
import os
class ScanDocGui:
    ScannedDocument=""
    def __init__(self,parent):
        self.parent=parent
        self.mainframe = ttk.Frame(parent,padding=(3,3,12,12))
        self.mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

        self.ImageFilePath = StringVar()
        self.ImageFilePath_entry= ttk.Entry(self.mainframe,width=50,textvariable=self.ImageFilePath)
        self.ImageFilePath_entry.grid(column=2,row=1,sticky=(W,E))

        self.imagechange=ttk.Label(self.mainframe)
        self.imagechange.grid(column=2,row=2,sticky=(W,E))

        ttk.Button(self.mainframe,text="Scan Document",command=self.ScanDocument).grid(column=3,row=1,sticky=E)
        ttk.Label(self.mainframe, text="Filepath To Document: ").grid(column=1,row=1, sticky=W)


        parent.columnconfigure(0,weight=1)
        parent.rowconfigure(0,weight=1)
        self.mainframe.columnconfigure(2,weight=1)
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)
            
        self.ImageFilePath_entry.focus()
        parent.bind("<Return>",self.ScanDocument)
        
    def ScanDocument(self,*args):
        if os.path.exists(self.ImageFilePath.get()):
            value = documentScanner(self.ImageFilePath.get())
            docImage = Image.fromarray(value)
            self.docImageCopy=docImage.copy()
            docImage.thumbnail((750,750))
            self.imgObj=ImageTk.PhotoImage(docImage)
            self.CreateDocumentGui()
            
        else:
            messagebox.showinfo(message=f"File Path {self.ImageFilePath.get()} doesn't exist")
            
    def SaveDocument(self):
        filename=filedialog.asksaveasfilename(defaultextension=".jpeg",filetypes=[("Jpeg File","*.jpeg"),("PNG file","*.png"),("All Files","*.*")])
        self.docImageCopy.save(f"{filename}")
        self.SaveMessage.set(f"Image has been saved in {filename}")
        
    def CheckTopLevelRemovable(self):
        if type(self.ScannedDocument) is str:
            return False
        else:
            return True
    def CreateDocumentGui(self):
        if self.CheckTopLevelRemovable() == True:
            self.ScannedDocument.destroy()
            
        self.ScannedDocument=Toplevel(self.parent)
        ttk.Button(self.ScannedDocument,text="Save Scanned Document",command=self.SaveDocument).grid(column=1,row=1,sticky=N)
        self.SaveMessage=StringVar()
        ttk.Label(self.ScannedDocument,textvariable=self.SaveMessage).grid(column=1,row=2,sticky=N)
        ttk.Label(self.ScannedDocument,image=self.imgObj).grid(column=1,row=3,sticky=N)
    
root=Tk()
root.title("Document To Scanner")
ScanDocGui(root)
root.mainloop()