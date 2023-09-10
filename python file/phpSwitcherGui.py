import os,re,winreg,json,ctypes,sys
import json
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
# import ttkbootstrap as bttk
from tkinter import messagebox
import webbrowser

#colors
bg_fore="#383838"
colorEdit="#0b4f16"
colorEditHover="#07330e"
bg_back="#303030"
white_fore="white"

app_icon='./phpswitcher.ico'
can_pass = True
# Your variables
appVerion = "PHP Swicher V1.0.1"
docs = 'https://github.com/maged909/windows-php-switcher'
aboutTxt = f'PHP Switcher\nIt\'s a simple open-source python tool that allows you to switch between php versions by modifying the system environment variable "PATH" to tell windows where the desired php is.\n\nRead the documentation here: {docs}'

guideHelp = 'https://github.com/maged909/windows-php-switcher/blob/main/README.md#config-notes'
configGuideUrl = f"Need help with the config? visit our config guide: {guideHelp}"

def showError(msg):
    messagebox.showerror("Configuration File Error", msg)
    exit()


if os.path.exists('config.json'):
    # Load the contents of the JSON file into a dictionary
    with open('config.json', 'r') as file:
        php_versions = json.load(file)
    validationFailed = False
    # Check that the dictionary has the expected structure
    expected_keys = {'path'}
    for key in php_versions:
        if not isinstance(php_versions[key], dict) or set(php_versions[key].keys()) != expected_keys:
            showError("Config Error: 'config.json' has an invalid structure. key '{}' must have 'path' keys.".format(key)+'\n\n'+configGuideUrl)
        if not validationFailed:
            if not os.path.isabs(php_versions[key]['path']):
                showError("Config Error: 'path' value for '{}' is not a vaild absolute path.".format(key)+'\n\n'+configGuideUrl)
            if re.search(r';', php_versions[key]['path']):
                showError("Config Error: 'path' value for '{}' contains ';' character.".format(key)+'\n\n'+configGuideUrl)

    if not validationFailed:
        # Check that there are no duplicate values in any key or value
        flat_values = []
        for key, value in php_versions.items():
            flat_values.extend(list(value.values()) + [key])
        if len(set(flat_values)) != len(flat_values):
            showError("Error: 'config.json' contains duplicate values."+'\n\n'+configGuideUrl)
        else:
            validConfig = True
else:
    can_pass = False
    # Function to create the config file and set can_pass to True
    def create_config_and_set_can_pass_true():
        global can_pass  # Declare can_pass as a global variable
        config_data = {}
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)
        global php_versions
        with open('config.json', 'r') as file:
            php_versions = json.load(file)
        can_pass = True
        root.destroy()

    # Initialize the main window
    root = ctk.CTk()
    root.title("PHP Switcher Error!")
    # Set the icon for the main window
    root.iconbitmap(app_icon)

    # Set the window dimensions and position it in the center
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.minsize(window_width,window_height)
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Label displaying the error message
    error_message = "Error: MISSING 'config.json'!\ndoes not exist in the current directory."
    error_label = ctk.CTkLabel(root, text=error_message, text_color=white_fore, bg_color='transparent', fg_color='transparent', height=0)
    error_label.configure(font=("Helvetica", 16))  # Set the font size to 16
    error_label.pack(fill='both', expand=True)

    # Create a frame to hold buttons
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(side='bottom', fill='x')

    # Create a button to generate the config file and set can_pass to True (right bottom corner)
    generate_button = ctk.CTkButton(button_frame, text="Generate Config File", command=create_config_and_set_can_pass_true)
    generate_button.pack(side='right', padx=10, pady=10)

    # Create a cancel button to close the window (left bottom corner)
    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=root.destroy,fg_color=bg_fore,bg_color=bg_back,hover_color=bg_back)
    cancel_button.pack(side='left', padx=10, pady=10)

    root.mainloop()
    # showError("Error: MISSING 'config.json' - does not exist in the current directory.")

if not can_pass:
    sys.exit()

def switch_php_version():
    selected_item = version_tree.selection()
    if selected_item:
        selected_version = version_tree.item(selected_item[0], "values")[0]
        new_path = php_versions[selected_version]["path"]

        # Get the environment variable registry key
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 0, winreg.KEY_ALL_ACCESS)

        # Get the current value of the PATH variable
        path_value = winreg.QueryValueEx(key, "PATH")[0]

        # Split the path value into a list of directories
        path_dirs = path_value.split(";")

        # Remove existing PHP version paths from the PATH variable
        for item_id in version_tree.get_children():
            version = version_tree.item(item_id, "values")[0]
            php_path = php_versions[version]["path"]
            if php_path in path_dirs:
                path_dirs.remove(php_path)

        # Check if the new PHP path is already in the PATH variable
        if new_path not in path_dirs:
            # Insert the new PHP path at the beginning of the list
            path_dirs.insert(0, new_path)

            # Join the path directories back into a single string
            new_path_value = ";".join(path_dirs)

            # Update the PATH variable in the registry
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)

            # Update the PATH variable in the current process environment
            os.environ["PATH"] = new_path_value

        # Close the registry key
        winreg.CloseKey(key)
        current_version.set(f"{selected_version}")
        switch_button.configure(state="disabled")
#Define a callback function
def callback(url):
   webbrowser.open_new_tab(url)

# Create a GUI window
window = ctk.CTk()
window.title('PHP Switcher')
window.geometry('800x400')
window.minsize(800,400)
window.configure(bg=bg_back)
window.iconbitmap(app_icon)


# Create a style for the notebook
SNoteBook = ttk.Style(window)
SNoteBook.theme_use("default")

# Configure the notebook style
SNoteBook.configure("Notebook.TNotebook", background=bg_fore, fieldbackground=bg_fore, foreground=white_fore, borderwidth=0)

# Configure the style for the tabs (inactive tabs)
SNoteBook.configure("TNotebook.Tab", background=bg_fore, foreground=white_fore, padding=[10, 5], borderwidth=0)

# Configure the style for the active tab
SNoteBook.map("TNotebook.Tab", background=[("selected", bg_back)], foreground=[("selected", white_fore)])

# Configure the style for the notebook body
SNoteBook.configure("TFrame", borderwidth=0)

notebook = ttk.Notebook(window, style="Notebook.TNotebook")
notebook.pack(fill="both", expand=True)

# Add tabs and content to the notebook
switchPhp = ttk.Frame(notebook)
configFrame = ttk.Frame(notebook)
# Configure row and column weights to make the frame expand with the window
configFrame.grid_rowconfigure(1, weight=1)
configFrame.grid_columnconfigure(0, weight=1)
# configFrame.grid_rowconfigure(1, weight=2)

about = ttk.Frame(notebook)

notebook.add(switchPhp, text="Switch PHP")

def sync_file(event=None):
    original_php_versions = {}
    try:
        with open('config.json', 'r') as file:
            original_php_versions = json.load(file)
    except FileNotFoundError:
        errorMsg("Error: config.json not found. Cannot reset changes.")
        return
    # Update the version_tree with the original data
    version_tree.delete(*version_tree.get_children())
    for version, config in original_php_versions.items():
        version_tree.insert("", "end", values=(version, config["path"]))

# Bind an event (e.g., <Button-1> for left mouse button click) to Tab 1's frame
switchPhp.bind("<FocusIn>", sync_file)

notebook.add(configFrame, text="Edit Config")

to_edit_version = tk.StringVar()
to_edit_path = tk.StringVar()

def changesMade():
    apply_button.configure(state="normal")
    reset_button.configure(state="normal")

def on_item_select(event):
    if not edit_tree.selection():
        return
    
    selected_item = edit_tree.selection()[0]
    hideEditFrame()
    hideEditFrameDisabled()

    # Get the selected item
    errorMsg("",errors_update)

    # Get the data from the selected item's columns
    version = edit_tree.item(selected_item, "values")[0]
    path = edit_tree.item(selected_item, "values")[1]

    to_edit_version.set(version)
    to_edit_path.set(path)

    if current_version.get() != version:
        showEditFrame()
    else:
        showEditFrameDisabled()

    # Show the frame
    # edit_frame.grid(row=1, column=0, padx=10, pady=10)

def delete_item(event=None):
    # Get the selected item
    selected_item = edit_tree.selection()[0]

    if not selected_item:
        return
    
    if current_version.get() == edit_tree.item(selected_item,'values')[0]:
        showEditFrameDisabled()
        return
    
    # Ask for confirmation using a dialog
    confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to delete this item?")
    
    if confirmation:
        # Delete the selected item from the Treeview
        edit_tree.delete(selected_item)
        hideEditFrame()
        changesMade()

def hideEditFrame():
    edit_frame.grid_forget()
    errorMsg("",errors_update)

def cancelEdit():
    hideEditFrame()
    edit_tree.selection_remove(edit_tree.get_children())

def showEditFrame():
    # edit_frame.pack(side='top',fill='x', expand=True,padx=10, pady=5)
    edit_frame.grid(row=1, column=1,sticky='new')

def hideEditFrameDisabled():
    edit_frame_disabled.grid_forget()
    # errorMsg("",errors_update)

def showEditFrameDisabled():
    # edit_frame.pack(side='top',fill='x', expand=True,padx=10, pady=5)
    edit_frame_disabled.grid(row=1, column=1,sticky='new')

def update_item():
    # Get the selected item
    selected_item = edit_tree.selection()[0]

    if not validToAdd(to_edit_version,to_edit_path,errors_update,True,edit_tree.item(selected_item,'values')):
        return

    # Update the Treeview with the new values
    new_version = version_entry.get()
    new_path_edit = path_entry.get()
    edit_tree.item(selected_item, values=(new_version, new_path_edit))
    changesMade()
    hideEditFrame()

def browse_folder_update():
    folder_path = tk.filedialog.askdirectory()
    to_edit_path.set(folder_path)
    validToAdd(to_edit_version,to_edit_path,errors_update)

# Define a function to validate adding a new PHP version
def validToAdd(v_text,p_text,errorV,isUpdate=False,selected=None):
    v_text = v_text.get()
    p_text = p_text.get()
    
    # Check if version and path are not empty
    if v_text == '' or p_text == '':
        errorMsg("Error: Version and Path must not be empty.",errorV)
        return False
    
    # Check for duplicate versions
    existing_versions = [edit_tree.item(item, "values")[0] for item in edit_tree.get_children()]
    if v_text in existing_versions:
        if isUpdate and selected[0] == v_text:
            errorMsg("",errorV)
        else:
            errorMsg("Error: This version already exists. Please provide a unique version.",errorV)
            return False

    # Check for duplicate paths
    existing_paths = [edit_tree.item(item, "values")[1] for item in edit_tree.get_children()]
    if p_text in existing_paths:
        if isUpdate and selected[1] == p_text:
            errorMsg("",errorV)
        else:
            errorMsg("Error: This path already exists. Please provide a unique path.",errorV)
            return False
    
    # Check if the path is absolute and doesn't contain ';'
    if not os.path.isabs(p_text):
        errorMsg("Error: Invalid path. Please provide an absolute path.",errorV)
        return False
    
    if ";" in p_text:
        errorMsg("Error: Invalid path. Path cannot contain ';'.",errorV)
        return False
    
    errorMsg("",errorV)
    # If all checks pass, the input is valid
    return True

# Create a Treeview to display PHP versions for editing
edit_tree = ttk.Treeview(configFrame, columns=("Version", "Path"), show="headings", selectmode="browse")
edit_tree.heading("Version", text="Version")
edit_tree.heading("Path", text="Path")

# # Configure column widths
# edit_tree.column("Version", width=50)
# edit_tree.column("Path", width=350)

errors = tk.StringVar()
errors_update = tk.StringVar()

# Create the frame for editing using pack
edit_frame = ctk.CTkFrame(configFrame,bg_color=bg_back,fg_color=bg_back)
edit_frame_disabled = ctk.CTkFrame(configFrame,bg_color=bg_back,fg_color=bg_back)
# Configure row and column weights to make the frame expand with the window
# edit_frame.grid_rowconfigure(1, weight=1)
edit_frame.grid_columnconfigure(1, weight=1)
edit_frame_disabled.grid_columnconfigure(1, weight=1)



addErrorFrame = ctk.CTkFrame(edit_frame,bg_color=bg_back,fg_color=bg_back)
addErrorFrame.grid(row=0,column=0,columnspan=5,sticky='ew')

sepFrame = ctk.CTkFrame(addErrorFrame,bg_color=bg_fore,fg_color=bg_fore,height=2)
sepFrame.pack(fill='x',padx=3,pady=4)

sepFrame = ctk.CTkFrame(edit_frame_disabled,bg_color=bg_fore,fg_color=bg_fore,height=2)
sepFrame.pack(fill='x',padx=3,pady=4)

error_label = ctk.CTkLabel(edit_frame_disabled,text='Selected php version is the current version,\nso you can\'t update or delete it.' ,text_color='red',bg_color='transparent',fg_color='transparent', height=0)
error_label.pack()

generalErrorL = ctk.CTkLabel(window,text='' ,text_color='red',bg_color=bg_fore,fg_color=bg_fore, height=0)

addVLabel = ctk.CTkLabel(addErrorFrame,text="Edit PHP Version: " ,bg_color='transparent',fg_color='transparent')
# addVLabel.grid(row=0,column=1,columnspan=3,sticky='w')
addVLabel.pack()
error_label = ctk.CTkLabel(addErrorFrame,textvariable=errors_update ,text_color='red',bg_color='transparent',fg_color='transparent', height=0)
error_label.pack()


# Labels and Entry widgets for editing (inside edit_frame)
version_label = ctk.CTkLabel(edit_frame, text="Version:")
version_label.grid(row=2, column=0, padx=5, pady=5)
version_entry = ctk.CTkEntry(edit_frame,textvariable=to_edit_version)
version_entry.grid(row=2, column=1,columnspan=3, padx=5, pady=5,sticky='ew')

path_label = ctk.CTkLabel(edit_frame, text="Path:")
path_label.grid(row=3, column=0, padx=5, pady=5)
path_entry = ctk.CTkEntry(edit_frame,textvariable=to_edit_path)
path_entry.grid(row=3, column=1,columnspan=2, padx=5, pady=5,sticky='ew')

# Create a button to trigger the folder dialog
browse_button_edit = ctk.CTkButton(edit_frame, text="Browse",fg_color=bg_back,hover_color=bg_fore, command=browse_folder_update,width=50)
browse_button_edit.grid(row=3,column=3,padx=4,pady=4)

# Buttons for delete and update (inside edit_frame)
cancel_button = ctk.CTkButton(edit_frame, text="Cancel", fg_color=colorEdit,hover_color=colorEditHover, command=cancelEdit, width=50)
cancel_button.grid(row=4, column=0, padx=5, pady=5)
delete_button = ctk.CTkButton(edit_frame, text="Delete", fg_color=colorEdit,hover_color=colorEditHover, command=delete_item, width=50)
delete_button.grid(row=4, column=2, padx=5, pady=5)
update_button = ctk.CTkButton(edit_frame, text="Update", fg_color=colorEdit,hover_color=colorEditHover, command=update_item, width=50)
update_button.grid(row=4, column=3, padx=5, pady=5)


# Bind the Treeview's selection event to the on_item_select function
edit_tree.bind("<ButtonRelease-1>", on_item_select)
edit_tree.bind("<Delete>", delete_item)

# Insert PHP versions into the editable Treeview
for version, config in php_versions.items():
    edit_tree.insert("", "end", text=version, values=(version, config["path"]))

# edit_tree.pack(side='left',fill="both", expand=True, padx=5)
edit_tree.grid(padx=5,row=0,rowspan=4,column=0,sticky='nswe')

addVFrame = ctk.CTkFrame(configFrame,bg_color=bg_back,fg_color=bg_back)
# addVFrame.pack(fill="x",expand=True,padx=10, pady=5)
addVFrame.grid(row=0, column=1,sticky='new')

# Configure row and column weights to make the frame expand with the window
addVFrame.grid_rowconfigure(1, weight=1)
addVFrame.grid_columnconfigure(1, weight=1)

to_add_version = tk.StringVar()
to_add_path = tk.StringVar()

def errorMsg(error_message,errorsV):
    errorsV.set(error_message)

# def add_version_typing(event=None):
#     if validToAdd():
#         add_button.configure(state="normal")
#     else:
#         add_button.configure(state="disabled")

def browse_folder():
    folder_path = tk.filedialog.askdirectory()
    to_add_path.set(folder_path)
    validToAdd(to_add_version,to_add_path,errors)
    # add_version_typing()
    # print(folder_path)

addErrorFrame = ctk.CTkFrame(addVFrame,bg_color=bg_back,fg_color=bg_back)
addErrorFrame.grid(row=0,column=0,columnspan=5,sticky='ew')
addVLabel = ctk.CTkLabel(addErrorFrame,text="Add New Version: " ,bg_color='transparent',fg_color='transparent')
# addVLabel.grid(row=0,column=1,columnspan=3,sticky='w')
addVLabel.pack()
error_label = ctk.CTkLabel(addErrorFrame,textvariable=errors ,text_color='red',bg_color='transparent',fg_color='transparent', height=0)
error_label.pack()
# error_label.grid(row=3,column=2,columnspan=3,sticky='e')

# btnsFrame = ctk.CTkFrame(configFrame,bg_color=bg_back,fg_color=bg_back)
# btnsFrame.pack(fill="x",padx=10, pady=5)

# Create a button to trigger the folder dialog
browse_button = ctk.CTkButton(addVFrame, text="Browse",fg_color=bg_back,hover_color=bg_fore, command=browse_folder,width=50)
browse_button.grid(row=2,column=2,padx=4,pady=4)

# Create buttons for adding, removing, and applying changes
version_input = ctk.CTkEntry(addVFrame,placeholder_text='Version',textvariable=to_add_version)
# version_input.bind("<FocusOut>",add_version_typing)
path_input = ctk.CTkEntry(addVFrame,placeholder_text='Path',textvariable=to_add_path)
# path_input.bind("<FocusOut>",add_version_typing)

add_button = ctk.CTkButton(addVFrame,fg_color=colorEdit,hover_color=colorEditHover, text="Add New Verion",width=30)

VLabel = ctk.CTkLabel(addVFrame,text="Version: " ,bg_color='transparent',fg_color='transparent')
VLabel.grid(row=1,column=0,pady=5)
version_input.grid(row=1,column=1,columnspan=3,sticky='nsew',padx=4,pady=4)
PLabel = ctk.CTkLabel(addVFrame,text="Path: " ,bg_color='transparent',fg_color='transparent')
PLabel.grid(row=2,column=0,pady=5)
path_input.grid(row=2,column=1,padx=4,pady=4,sticky='nsew')
add_button.grid(row=1,column=4,rowspan=2,sticky='nsew',padx=4,pady=4)


# remove_button = ctk.CTkButton(btnsFrame,fg_color=colorEdit,hover_color=colorEditHover, text="-",width=30)
apply_button = ctk.CTkButton(configFrame,bg_color=bg_back,fg_color=colorEdit,hover_color=colorEditHover, text="Apply", state="disabled")

# Create a "Reset" button to reset changes
reset_button = ctk.CTkButton(configFrame,bg_color=bg_back,fg_color=bg_fore,hover_color=bg_back, text="Reset Changes",state="disabled")

# remove_button.pack(side="left")
# apply_button.pack(side="bottom", pady=5)
apply_button.grid(row=2, column=1,sticky='e', padx=3, pady=3)
reset_button.grid(row=2, column=1,sticky='w', padx=3, pady=3)

# Define a function to add a new PHP version to the editable Treeview
def add_php_version():
    if not validToAdd(to_add_version,to_add_path,errors):
        return
    edit_tree.insert("", "end", values=(to_add_version.get(), to_add_path.get()))
    to_add_path.set('')
    to_add_version.set('')
    changesMade()

# Define a function to apply changes to the config.json file
def apply_changes():
    # Clear previous errors
    error_label.configure(text="")
    
    new_php_versions = {}
    for item in edit_tree.get_children():
        version = edit_tree.item(item, "values")[0]
        path = edit_tree.item(item, "values")[1]
        new_php_versions[version] = {"path": path}

    # Check for duplicates in the new_php_versions dictionary
    if len(new_php_versions) != len(set(new_php_versions.keys())):
        errorMsg("Error: Duplicate PHP versions detected. Please fix and try again.")
        return

    # Check for invalid paths
    for version, config in new_php_versions.items():
        if not os.path.isabs(config["path"]):
            errorMsg(f"Error: Invalid path for '{version}'. Please provide an absolute path.")
            return
        if ";" in config["path"]:
            errorMsg(f"Error: Invalid path for '{version}'. Path cannot contain ';'.")
            return

    # Update the php_versions dictionary with the new values
    php_versions.clear()
    php_versions.update(new_php_versions)

    # Save the updated config to config.json
    with open('config.json', 'w') as file:
        json.dump(php_versions, file, indent=4)

    # Disable the apply button again
    apply_button.configure(state="disabled")
    reset_button.configure(state="disabled")

# Define a function to reset changes from the config.json file
def reset_changes():
    # Clear previous errors
    error_label.configure(text="")

    # Load the original data from config.json
    original_php_versions = {}
    try:
        with open('config.json', 'r') as file:
            original_php_versions = json.load(file)
    except FileNotFoundError:
        errorMsg("Error: config.json not found. Cannot reset changes.")
        return

    # Update the edit_tree with the original data
    edit_tree.delete(*edit_tree.get_children())
    for version, config in original_php_versions.items():
        edit_tree.insert("", "end", values=(version, config["path"]))

    hideEditFrame()
    # Disable the apply button again
    apply_button.configure(state="disabled")
    reset_button.configure(state="disabled")

# # Check and disable the button if the selected version is the same as the current version
# def removeVBtn(event):
#     selected_item = edit_tree.selection()
#     if selected_item:
#         selected_version = edit_tree.item(selected_item, "text")

# edit_tree.bind("<<TreeviewSelect>>", removeVBtn)

# Bind button actions to functions
reset_button.configure(command=reset_changes)
add_button.configure(command=add_php_version)
apply_button.configure(command=apply_changes)

# Disable the "Remove Version" button initially (when nothing is selected)
# remove_button.configure(state="disabled")

notebook.add(about, text="About")
# Create a label to display info
aboutLable = ttk.Label(about, text=aboutTxt,background=bg_back,foreground=white_fore,justify='left',wraplength=560,cursor="hand2")
aboutLable.pack(fill='x',padx=10,pady=5)
aboutLable.bind("<Button-1>", lambda e: callback(docs))

# Create a separator
separator = ttk.Separator(about, orient="horizontal")
separator.pack(fill="x", padx=10, pady=5)

# Create a label to display info
aboutLable = ttk.Label(about, text=configGuideUrl,background=bg_back,foreground=white_fore,justify='left',wraplength=560,cursor="hand2")
aboutLable.pack(fill='x',padx=10,pady=5)
aboutLable.bind("<Button-1>", lambda e: callback(guideHelp))

# Create a label for the text in the lower-left corner
text_label = ttk.Label(about, text=appVerion, background=bg_back,foreground=white_fore)
text_label.pack(side="bottom", anchor="e", padx=10, pady=10)

s = ttk.Style()
# Create style used by default for all Frames
s.configure('TFrame', background=bg_back)

current_version = tk.StringVar()

# Create a Treeview to display PHP versions in a table
version_tree = ttk.Treeview(switchPhp, columns=("Version", "Path"), show="headings",selectmode="browse")
version_tree.heading("Version", text="Version")
version_tree.heading("Path", text="Path")

# Configure column widths
version_tree.column("Version", width=100)  # Adjust the width as needed
version_tree.column("Path", width=300)     # Adjust the width as needed

style = ttk.Style(switchPhp)
style.theme_use("default")  # set theme to clam
style.configure("Treeview", background=bg_back, fieldbackground=bg_back, foreground=white_fore, borderwidth=0)
style.configure('Treeview.Heading', background=bg_back, foreground=white_fore, borderwidth=0)
# Apply the custom style to the Treeview.Heading style
style.map('Treeview.Heading', background=[('active', bg_fore)])

# Insert PHP versions into the table
for version, config in php_versions.items():
    item = version_tree.insert("", "end", text=version, values=(version, config["path"]))

version_tree.pack(fill="both", expand=True,padx=5)


VFrame = ctk.CTkFrame(switchPhp,fg_color='transparent')
VFrame.pack(fill="x", side='bottom',padx=10, pady=5)

currentVersionLable = ctk.CTkLabel(VFrame, text='Current PHP Version: ')
currentVersionLable.configure(font=("TkDefaultFont", 14, "bold"))
currentVersionLable.pack(side='left')
# Create a label to display the current PHP version
current_version_label = ctk.CTkLabel(VFrame, textvariable=current_version)
current_version_label.configure(font=("TkDefaultFont", 14, "bold"))
current_version_label.pack(side='left')

# Create a button to switch PHP version
switch_button = ctk.CTkButton(VFrame, text="Switch PHP Version", command=switch_php_version, state="disabled")
switch_button.pack(side='right')

# Check and disable the button if the selected version is the same as the current version
def check_button_state(event):
    selected_item = version_tree.selection()
    if selected_item:
        selected_version = version_tree.item(selected_item[0], "values")[0]
        if current_version.get() == selected_version:
            switch_button.configure(state="disabled")
        else:
            switch_button.configure(state="normal")

version_tree.bind("<<TreeviewSelect>>", check_button_state)


php_version = "N/A"
# Get the environment variable registry key
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 0, winreg.KEY_ALL_ACCESS)

# Get the current value of the PATH variable
path_value = winreg.QueryValueEx(key, "PATH")[0]
for version, config in php_versions.items():
    if config["path"]+";" in path_value:
        php_version = version
        break

# Set the initial value for the current PHP version
current_version.set(php_version)

# Start the GUI main loop
window.mainloop()
