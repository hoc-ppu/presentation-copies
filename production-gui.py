import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk

import speech_functions

## some tests to do after demo ##

# # try removing the tk ttk - are they duplications?
# # the file dialog seemed to only work with tk?



# Function for opening folder directory
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    if folder_path:
        folder_text.set(folder_path)

# cannot call function which has parameters, so create a function with none
# then can call on function with parameters
# calls the speech script so that we can add the URL and file path
def save():
    speech_functions.get_speech(url.get(), folder_text.get())
    tk.messagebox.showinfo(title="All Done", message="All Done")

# creating the GUI root
root = Tk()
root.title("Presentation Copies | Download and Save Content")

# creating the window
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# input field - would text widget be better so can wrap depending on size of URL
url = StringVar()
url_entry = ttk.Entry(mainframe, width=100, textvariable=url)
url_entry.grid(column=2, row=1, sticky=(W, E))
url.set("https://hansard.parliament.uk/Commons/2024-10-10/debates/4D26F1DB-5194-49CD-85CF-087377B7A3DB/SportTeamGBAndParalympicsgb#contribution-B7C30195-448D-4087-9106-EDDC8FC517B7")

# label for input field
ttk.Label(mainframe, text="Website Link (URL)").grid(column=1, row=1, sticky=W)


# Create a button to browse for a folder
browse_button = ttk.Button(mainframe, text="Choose Folder", command=browse_folder).grid(column=3, row=2, sticky=W)

# label for browse file manager field -
#ttk.Label(mainframe, text="Select A Folder").grid(column=1, row=2, sticky=W)

# entry / text field for the folder directory /file path
folder_text = tk.StringVar()
folder = tk.Entry(mainframe, textvariable=folder_text)
new_text = "folder file path"
folder_text.set(new_text)
folder.grid(column=2, row=2, sticky=(W, E))


# execute button
ttk.Button(mainframe, text="Finish", command=save).grid(column=2, row=3, sticky=W)

# adding padding around widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

url_entry.focus()
# root.bind("<Return>", calculate)

root.mainloop()
