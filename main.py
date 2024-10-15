import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os
import shutil
from extension_mapping import EXTENSION_TO_FOLDER

# Light and Dark Theme
themes = {
    "light": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "button_bg": "#E0E0E0",
        "button_fg": "#000000",
        "frame_bg": "#F0F0F0",
    },
    "dark": {
        "bg": "#2E2E2E",
        "fg": "#FFFFFF",
        "button_bg": "#4E4E4E",
        "button_fg": "#FFFFFF",
        "frame_bg": "#3E3E3E",
    }
}

#----------------------------------------------------------------------------------------------------------------------#

# Dictionary to store original file paths for undo functionality
file_moves = {}
created_folders = []  # List to store folders created during sorting

def create_backup(original_folder):
    # Get the base name of the original folder
    base_name = os.path.basename(original_folder)

    # Create the backup folder name by appending "(BACKUP)"
    backup_folder_name = f"{base_name} (BACKUP)"

    # Create the full backup folder path
    backup_folder_path = os.path.join(os.path.dirname(original_folder), backup_folder_name)

    # Create the backup directory
    os.makedirs(backup_folder_path, exist_ok=True)

    # Copy the contents of the original folder to the backup folder
    for item in os.listdir(original_folder):
        original_item_path = os.path.join(original_folder, item)
        backup_item_path = os.path.join(backup_folder_path, item)

        # Check if it's a file or directory and copy accordingly
        if os.path.isdir(original_item_path):
            shutil.copytree(original_item_path, backup_item_path, dirs_exist_ok=True)
        else:
            shutil.copy2(original_item_path, backup_item_path)

    print(f"Backup created at: {backup_folder_path}")


# Function to select folder
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        status_label.config(text = f"Selected folder: {folder_selected}")
        global selected_folder
        selected_folder = folder_selected

        # Hide the select button and show the other buttons
        select_button.pack_forget()
        sort_button.pack(pady = 5)
        undo_button.pack(side = tk.LEFT, padx = 5)
        recursive_sort_button.pack(side = tk.LEFT, padx = 5)
        change_button.pack(pady = 5)


# Function to organize files non-recursively
def organize_files():
    global file_moves
    global created_folders
    file_moves = {}
    created_folders = []

    if not selected_folder:
        return

    directory = selected_folder
    moved_files_count = 0
    total_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

    # Create a backup if enabled
    if backup_enabled.get():  # Use .get() to retrieve the value of the BooleanVar
        create_backup(directory)  # Backup the selected directory

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):
            continue

        file_extension = filename.split('.')[-1].lower()

        folder_name = 'Others'
        for category, extensions in EXTENSION_TO_FOLDER.items():
            if file_extension in extensions:
                folder_name = category
                break

        folder_path = os.path.join(directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            created_folders.append(folder_path)

        new_path = os.path.join(folder_path, filename)

        file_moves[new_path] = file_path

        shutil.move(file_path, new_path)
        moved_files_count += 1

        status_label.config(text=f"Moved {moved_files_count}/{total_files} files...")
        root.update_idletasks()

    messagebox.showinfo("Success", f"Successfully organized {moved_files_count} files!")
    status_label.config(text="Organization complete.")


    # Hide sorting buttons after sorting
    sort_button.pack_forget()
    recursive_sort_button.pack_forget()

# Function to organize files recursively
def organize_files_recursive(directory):
    global file_moves
    global created_folders
    file_moves = {}
    created_folders = []

    moved_files_count = 0

    for root_dir, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root_dir, filename)
            file_extension = filename.split('.')[-1].lower()

            folder_name = 'Others'
            for category, extensions in EXTENSION_TO_FOLDER.items():
                if file_extension in extensions:
                    folder_name = category
                    break

            folder_path = os.path.join(root_dir, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                created_folders.append(folder_path)

            new_path = os.path.join(folder_path, filename)

            file_moves[new_path] = file_path

            shutil.move(file_path, new_path)
            moved_files_count +=  1

            status_label.config(text = f"Moved {moved_files_count} files...")
            root.update_idletasks()

    messagebox.showinfo("Success", f"Successfully organized {moved_files_count} files recursively!")
    status_label.config(text = "Recursive organization complete.")

    # Hide sorting buttons after sorting
    sort_button.pack_forget()
    recursive_sort_button.pack_forget()

# Function to undo file moves
def undo_file_moves():
    if not file_moves:
        messagebox.showinfo("Undo", "No file moves to undo.")
        return

    moved_files_count = 0
    total_files = len(file_moves)

    for new_path, original_path in file_moves.items():
        shutil.move(new_path, original_path)
        moved_files_count +=  1

        status_label.config(text = f"Undoing {moved_files_count}/{total_files} files...")
        root.update_idletasks()

    for folder in created_folders:
        if os.path.exists(folder) and not os.listdir(folder):
            os.rmdir(folder)

    file_moves.clear()
    created_folders.clear()

    messagebox.showinfo("Undo", f"Successfully undone {moved_files_count} file moves!")
    status_label.config(text = "Undo complete.")

    # Re-show buttons after undoing
    undo_button.pack(side = tk.LEFT, padx = 5)
    recursive_sort_button.pack(side = tk.LEFT, padx = 5)
    change_button.pack(pady = 5)

# Function to allow the user to select a different folder
def reset_selection():
    select_folder()

# Function to Switch Themes
def switch_theme(theme):
    root.config(bg=themes[theme]["bg"])

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=themes[theme]["bg"], fg=themes[theme]["fg"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=themes[theme]["button_bg"], fg=themes[theme]["button_fg"])
        elif isinstance(widget, tk.Frame):
            widget.config(bg=themes[theme]["frame_bg"])

def toggle_theme():
    new_theme = "dark" if theme_var.get() == "light" else "light"
    theme_var.set(new_theme)
    switch_theme(new_theme)

    theme_button.config(image=sun_icon if new_theme == "light" else moon_icon)

#----------------------------------------------------------------------------------------------------------------------#

# Create the main Tkinter window
root = tk.Tk()
root.title("File Organizer")
root.geometry("600x300")
root.resizable(False, False)
root.configure(bg = "#e0e0e0")

# Set up fonts and styles
title_font = ('Comic Sans MS', 18, 'bold')
button_font = ('Arial', 12)
label_font = ('Arial', 10)

# Variable to store selected folder
selected_folder = None

# Create a title label with vibrant color
title_label = tk.Label(root, text = "Totally Working File Organizer", font = title_font, bg = "#e0e0e0", fg = "#FF5722")
title_label.pack(pady = 10)

# Create a button frame for better layout
button_frame = tk.Frame(root, bg = "#e0e0e0")
button_frame.pack(pady = 10)

# Create a button to select the folder with a gradient background
select_button = tk.Button(button_frame, text = "✨ Select Folder to Organize ✨", font = button_font, bg = "#FF4081", fg = "white",
                          command = select_folder, relief = "raised", activebackground = "#FF80AB", padx = 10, pady = 5)
select_button.pack(pady = 5, padx = 10)

# Create a label to show the status of the operation
status_label = tk.Label(root, text = "No folder selected yet.", font = label_font, bg = "#e0e0e0", fg = "#3F51B5")
status_label.pack(pady = 10)

# Toggle button for the Theme Switch
theme_var = tk.StringVar(value="light")

#Backup Checkbox
backup_enabled = tk.BooleanVar()

# Load Light/Dark Theme Icon
sun_icon = ImageTk.PhotoImage(Image.open("icon/theme_switch.png").resize((30, 30)))  # Adjust size as needed
moon_icon = ImageTk.PhotoImage(Image.open("icon/theme_switch.png").resize((30, 30)))


# Create buttons for "Sort Folder", "Undo", "Sort Recursive", "Select Different Folder", etc.
sort_button = tk.Button(button_frame, text = "📁 Sort Folder", font = button_font, bg = "#4CAF50", fg = "white",
                        command = organize_files, relief = "raised", activebackground = "#66BB6A", padx = 10, pady = 5)

undo_button = tk.Button(button_frame, text = "↩️ Undo", font = button_font, bg = "#FF9800", fg = "white",
                        command = undo_file_moves, relief = "raised", activebackground = "#FFB74D", padx = 10, pady = 5)

recursive_sort_button = tk.Button(button_frame, text = "🔄 Sort Recursive", font = button_font, bg = "#2196F3", fg = "white",
                                   command = lambda: organize_files_recursive(selected_folder), relief = "raised", activebackground = "#42A5F5", padx = 10, pady = 5)

change_button = tk.Button(button_frame, text = "🔄 Select a Different Folder", font = button_font, bg = "#9C27B0", fg = "white",
                          command = reset_selection, relief = "raised", activebackground = "#AB47BC", padx = 10, pady = 5)

theme_button = tk.Label(root, image=sun_icon)
theme_button.bind("<Button-1>", lambda event: toggle_theme())


# Arrange buttons in the button frame
sort_button.pack(pady = 5)  # Pack Sort Folder at the top
undo_button.pack(side = tk.LEFT, padx = 5)  # Pack Undo and Sort Recursive side by side
recursive_sort_button.pack(side = tk.LEFT, padx = 5)
change_button.pack(pady = 5)  # Pack Select Different Folder at the bottom
theme_button.place(x=10, y=10)
tk.Checkbutton(root, text="Enable Backup", variable=backup_enabled).pack(pady=10)

# Hide all buttons except for the select button initially
sort_button.pack_forget()
undo_button.pack_forget()
recursive_sort_button.pack_forget()
change_button.pack_forget()
switch_theme(theme_var.get())

# Start the Tkinter event loop
root.mainloop()

