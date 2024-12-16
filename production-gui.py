import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import speech_functions


# Function for opening folder directory
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    if folder_path:
        folder_text.set(folder_path)


# cannot call function which has parameters, so create a function with none
# then can call on function with parameters
# calls the speech script so that we can add the URL and file path
def save():
    try:
        warn_tuple = speech_functions.get_speech(url.get(), folder_text.get())
        if any(warn_tuple):
            messagebox.showwarning(title="Warning", message=", ".join(warn_tuple))
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e))
    else:
        messagebox.showinfo(title="All Done", message="All Done")


# creating the GUI root
root = tk.Tk()
root.title("Presentation Copies | Download and Save Content [V1]")

# creating the window
mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Insert the website URL from Click Up into the box below").grid(column=1, columnspan=2, row=1, sticky="nw")


# input field - would text widget be better so can wrap
# depending on size of URL
url = tk.StringVar()
url_entry = ttk.Entry(mainframe, width=100, textvariable=url)
# url_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
url_entry.grid(column=2, row=2, sticky="we")
url.set("")

# label for input field
ttk.Label(mainframe, text="Website Link (URL)").grid(column=1, row=2, sticky=tk.W)

# Create a button to browse for a folder
ttk.Button(mainframe, text="Choose Folder", command=browse_folder).grid(
    column=3, row=3, sticky=tk.W
)

# entry / text field for the folder directory /file path
folder_text = tk.StringVar()
folder = tk.Entry(mainframe, textvariable=folder_text)
new_text = ""
folder_text.set(new_text)
# folder.grid(column=2, row=2, sticky=(tk.W, tk.E))
folder.grid(column=2, row=3, sticky="we")

# execute button
ttk.Button(mainframe, text="Finish", command=save).grid(column=2, row=4, sticky=tk.W)

# adding padding around widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

url_entry.focus()
# root.bind("<Return>", calculate)

root.mainloop()
