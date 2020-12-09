import tkinter as tk
from os import listdir
from os.path import isfile, join, dirname, abspath
pathToScript = dirname(abspath(__file__))
import HopscotchFileFunctions as HSF
import PrintHSCode as HSP
import json

versionNumber = "Dev.0.1"

#get all HS json files
pathToJSON = join(pathToScript, "json_projects")
draftFileNames = [f for f in listdir(pathToJSON) if isfile(join(pathToJSON, f))]

draftString = ""
draftDictionary = {}

#print (draftFileNames)


def get_json_dictionary(directory,showJSON):
    global draftDictionary, draftString
    with open(directory, mode='r',encoding="utf-8") as f:
        if showJSON: draftString = HSF.remove_emoji(f.read())
        else: draftString = HSF.remove_emoji(HSP.printAllCode(f.read()))
        f.seek(0)
        draftDictionary = json.loads(f.read())

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.filename = ""

        #configure grid to expand to window size
        tk.Grid.rowconfigure(root, 2, weight=1)
        tk.Grid.columnconfigure(root, 3, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Hopscotch Code Viewer " + str(versionNumber))

        quit = tk.Button(root,text="Quit",fg="red",command=root.destroy)
        quit.grid(column=1,ipady=2,ipadx=5,pady=2,sticky="w")

        self.listOfFilenames = tk.Listbox(root, selectmode = "BROWSE")
        self.listOfFilenames.grid(column=1,rowspan=5,sticky="ns")
        for filename in draftFileNames:
            self.listOfFilenames.insert("end", filename)

        showCodeButton = tk.Button(root, text = "Show Code", command = self.show_code)
        showCodeButton.grid(column=1,pady=2,sticky="w")

        showJSONButton = tk.Button(root, text = "Show JSON", command = self.show_json)
        showJSONButton.grid(column=1,pady=2,sticky="w")

    def show_json(self):
        self.setup_text_window(showJSON=True)

    def show_code(self):
        self.setup_text_window(showJSON=False)

    def setup_text_window(self, showJSON):
        if self.listOfFilenames.curselection() != []:
            self.filename = draftFileNames[list(map(int, self.listOfFilenames.curselection()))[0]]
            self.projectFilenameText = tk.Label(root, text = self.filename)
            self.projectFilenameText.grid(column=3,row=1)

            get_json_dictionary(join(pathToJSON, self.filename),showJSON)

            self.scrollbar = tk.Scrollbar(root)
            self.scrollbar.grid(column=4,row=2,rowspan=15,sticky="NS")

            self.codeLabel = tk.Text(root,height=20,background="#f4f4f4",yscrollcommand=self.on_textscroll,font="Menlo", spacing1=3)
            self.codeLabel.insert("insert",draftString)
            self.codeLabel.grid(column=3,row=2,rowspan=20, sticky="nsew")

            widthOfLinenumber = len(str(len(draftString.splitlines())))
            self.lineNumberLabel = tk.Text(root,width=widthOfLinenumber,height=20,background="#f4f4f4",yscrollcommand=self.on_textscroll,font="Menlo")
            self.lineNumberLabel.grid(column=2,row=2,rowspan=20, sticky="ns")
            for i in range(len(draftString.splitlines())):
                self.lineNumberLabel.insert("insert",str(i) + "\n")
            self.lineNumberLabel.tag_config("center+gray", justify='center', foreground="gray", spacing1 = 3)
            self.lineNumberLabel.tag_add("center+gray", 1.0, "end")
            self.lineNumberLabel.config(state="disabled")

            self.scrollbar.config(command=self.on_scrollbar)

    def on_scrollbar(self, *args):
        '''Connect the yview action together'''
        self.lineNumberLabel.yview(*args)
        self.codeLabel.yview(*args)

    def on_textscroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel
        is moved on a text widget'''
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])


root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
