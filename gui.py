from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from documentscanner import documentScanner
def ScanDocument():
    global imgObj,docImageCopy
    try:
        value = documentScanner(ImageFilePath.get())
        docImage = Image.fromarray(value)
        docImageCopy=docImage.copy()
        docImage.thumbnail((750,750))
        imgObj=ImageTk.PhotoImage(docImage)
        imagechange['image']=imgObj
        ttk.Button(mainframe,text="Save Scanned Document", command=saveImage).grid(column=4,row=1,sticky=W)

    except ValueError:
        pass
def saveImage():
    docImageCopy.save(f"./ScannedDocument.jpeg")
root=Tk()
root.title("Document To Scanner")

mainframe = ttk.Frame(root,padding=(3,3,12,12))
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

ImageFilePath = StringVar()
ImageFilePath_entry= ttk.Entry(mainframe,width=50,textvariable=ImageFilePath)
ImageFilePath_entry.grid(column=2,row=1,sticky=(W,E))

imagechange=ttk.Label(mainframe)
imagechange.grid(column=2,row=2,sticky=(W,E))



ttk.Button(mainframe,text="Scan Document",command=ScanDocument).grid(column=3,row=1,sticky=E)
ttk.Label(mainframe, text="Filepath To Document: ").grid(column=1,row=1, sticky=W)


root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
mainframe.columnconfigure(2,weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5,pady=5)
    
ImageFilePath_entry.focus()
root.bind("<Return>",ScanDocument)

root.mainloop()