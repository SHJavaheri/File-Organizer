import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

#Defining a map for file extensions to custom folder names
EXTENSION_TO_FOLDER = {
    'jpg': 'Images',
    'jpeg': 'Images',
    'png': 'Images',
    'gif': 'Images',
    'mp3': 'Music',
    'wav': 'Music',
    'mp4': 'Videos',
    'avi': 'Videos',
    'txt': 'Documents',
    'pdf': 'Documents',
    'docx': 'Documents',
    'exe': 'Programs'
}


# Function to select folder
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # Update the status label
        status_label.config(text = f"Selected folder: {folder_selected}")
        # Store the selected folder path in a global variable
        global selected_folder
        selected_folder = folder_selected
        # Show the "Sort Folder" and "Select Different Folder" buttons
        sort_button.pack(pady = 5)
        change_button.pack(pady = 5)


# Function to organize files
def organize_files():
    if not selected_folder:
        return

    directory = selected_folder
    moved_files_count = 0
    total_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):
            continue

        file_extension = filename.split('.')[-1].lower()

        if file_extension in EXTENSION_TO_FOLDER:
            folder_name = EXTENSION_TO_FOLDER[file_extension]
        else:
            folder_name = 'Others'

        folder_path = os.path.join(directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        new_path = os.path.join(folder_path, filename)
        shutil.move(file_path, new_path)
        moved_files_count += 1

        # Update status message as files are moved
        status_label.config(text = f"Moved {moved_files_count}/{total_files} files...")
        root.update_idletasks()  # Update UI dynamically

    # Final message when organization is complete
    messagebox.showinfo("Success", f"Successfully organized {moved_files_count} files!")
    status_label.config(text = "Organization complete.")

    # Hide the "Sort Folder" and "Select Different Folder" buttons again
    sort_button.pack_forget()
    change_button.pack_forget()


# Function to allow the user to select a different folder
def reset_selection():
    # Reuse the select_folder function to ask for a new directory
    select_folder()


# Create the main Tkinter window
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x250")
root.resizable(False, False)  # Fix window size

# Set up fonts and styles
button_font = ('Helvetica', 12, 'bold')
label_font = ('Helvetica', 10)
bg_color = '#f0f0f0'
root.configure(bg = bg_color)

# Variable to store selected folder
selected_folder = None

# Create title label
title_label = tk.Label(root, text = "Welcome to the File Organizer", font = ('Helvetica', 14, 'bold'), bg = bg_color)
title_label.pack(pady = 10)

# Create a button to select the folder
select_button = tk.Button(root, text = "Select Folder to Organize", font = button_font, bg = "#4CAF50", fg = "white",
                          command = select_folder)
select_button.pack(pady = 10)

# Create a label to show the status of the operation
status_label = tk.Label(root, text = "No folder selected yet.", font = label_font, bg = bg_color)
status_label.pack(pady = 10)

# Create buttons for "Sort Folder" and "Select a Different Folder" (hidden initially)
sort_button = tk.Button(root, text = "Sort Folder", font = button_font, bg = "#2196F3", fg = "white", command = organize_files)
change_button = tk.Button(root, text = "Select a Different Folder", font = button_font, bg = "#f44336", fg = "white",
                          command = reset_selection)

# Start the Tkinter main loop
root.mainloop()
