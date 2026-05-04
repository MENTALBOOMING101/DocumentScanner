from tkinter import *
from tkinter import ttk , messagebox,Toplevel,filedialog
from PIL import ImageTk,Image
from documentscanner import documentScanner,imageToText,imageToPdf
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

        ttk.Button(self.mainframe,text="Scan Document",command=self.ScanDocument).grid(column=4,row=1,sticky=E)
        ttk.Button(self.mainframe,text="Browse",command=self.Browse).grid(column=3,row=1, sticky = W)
        ttk.Label(self.mainframe, text="Filepath To Document: ").grid(column=1,row=1, sticky=W)


        parent.columnconfigure(0,weight=1)
        parent.rowconfigure(0,weight=1)
        self.mainframe.columnconfigure(2,weight=1)
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)
            
        self.ImageFilePath_entry.focus()
        parent.bind("<Return>",self.ScanDocument)
        
 # Checks if pathFile exist then makes the image to Scanned Document
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
            
 # Ask where to save and save as Jpeg as default
    def SaveDocument(self):
        filename=filedialog.asksaveasfilename(defaultextension=".jpeg",filetypes=[("Jpeg File","*.jpeg"),("PNG file","*.png"),("All Files","*.*")])
        self.docImageCopy.save(f"{filename}")
        self.SaveMessage.set(f"Image has been saved in {filename}")

 # Checks Whether ScannedDocument has been used for creating Window
    def CheckTopLevelRemovable(self):
        if type(self.ScannedDocument) is str:
            return False
        else:
            return True
        
 # Creates A Window that shows the Scanned Document and Have a Button for Saving
    def CreateDocumentGui(self):
        if self.CheckTopLevelRemovable() == True:
            self.ScannedDocument.destroy()
            
        self.ScannedDocument=Toplevel(self.parent)
        ttk.Button(self.ScannedDocument,text="Save Document",command=self.SaveDocument).grid(column=1,row=1,sticky=N)
        ttk.Button(self.ScannedDocument,text="Save Document as PDF",command=self.SaveDocumentAsPDF).grid(column=2,row=1,sticky=N)
        ttk.Button(self.ScannedDocument,text="Turn Image to text",command=self.TurnDocumentToString).grid(column=3,row=1,sticky=N)
        self.SaveMessage=StringVar()
        ttk.Label(self.ScannedDocument,textvariable=self.SaveMessage).grid(column=1,row=2,sticky=N)
        ttk.Label(self.ScannedDocument,image=self.imgObj).grid(column=2,row=3,sticky=N)
        
 # Creates a dialog that can be used for browsing files for adding Scanned Documents
    def Browse(self):
        filename = filedialog.askopenfilename(filetypes=[("Jpeg File","*.jpeg"),("PNG file","*.png"),("All Files","*.*")])
        self.ImageFilePath.set(filename)
        
  # Turns Image into PDF
    def SaveDocumentAsPDF(self):
        filename=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF files","*.pdf"),("All Files","*.*")])      
        imageToPdf(self.docImageCopy,filename)
        self.SaveMessage.set(f"Image has been saved in {filename}")

 # Turn Image in to String
    def TurnDocumentToString(self):
        
        textString=Toplevel(self.ScannedDocument)
        
        self.documentText= StringVar()
        ttk.Label(textString,textvariable=self.documentText).grid(column=1,row=1 ,sticky=S)
        self.documentText.set(imageToText(self.docImageCopy))
        print(self.documentText.get())
        ttk.Button(textString,text="Close").grid(column=1,row=2,sticky=S)

    
root=Tk()
root.title("Document To Scanner")
ScanDocGui(root)
root.mainloop()