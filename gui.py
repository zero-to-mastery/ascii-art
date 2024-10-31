import importlib.util
from tkinter import Menu, Scrollbar, StringVar, Text, Tk, Toplevel, filedialog, ttk
from tkinter.constants import END, FALSE, NORMAL, E, N, S, W

# Workaroung because of hyphen in filename
module_name = "community-version"
file_path = "./community-version.py"
spec = importlib.util.spec_from_file_location(module_name, file_path)
community_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(community_version)


def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("JPEG", "*.jpg *.jpeg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("TIFF", "*.tiff")])
    if file_path:
        image_path.set(file_path)


def convert_image():
    image = image_path.get()
    if image:
        ascii_art = community_version.handle_image_conversion(image)
        display_ascii_art(ascii_art)


def save_file(ascii_art):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(ascii_art)


def display_ascii_art(ascii_art):
    # Create ascii art preview window
    preview_window = Toplevel(root)
    preview_window.title("ZTM - Ascii Preview")
    preview_window.iconbitmap("ztm-icon.ico")
    preview_window.columnconfigure(0, weight=1)
    preview_window.rowconfigure(0, weight=1)

    # Create Preview Window Frame
    preview_frame = ttk.Frame(preview_window, padding="3 3 12 12")
    preview_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    preview_frame.columnconfigure(0, weight=1)
    preview_frame.rowconfigure(0, weight=1)

    # Create text widget to display the ascii art
    text_widget = Text(preview_frame, wrap="none")  # Set wrap to none
    text_widget.insert(END, ascii_art)
    text_widget.config(state=NORMAL)
    text_widget.grid(column=0, row=0, sticky=(N, W, E, S))

    # Add vertical scrollbar
    vert_scroll_bar = Scrollbar(preview_frame, orient="vertical", command=text_widget.yview)
    text_widget.config(yscrollcommand=vert_scroll_bar.set)
    vert_scroll_bar.grid(column=1, row=0, sticky=(N, S))

    # Add horizontal scrollbar
    horz_scroll_bar = Scrollbar(preview_frame, orient="horizontal", command=text_widget.xview)
    text_widget.config(xscrollcommand=horz_scroll_bar.set)
    horz_scroll_bar.grid(column=0, row=1, sticky=(W, E))

    # Add File Menu
    preview_window.option_add("*tearOff", FALSE)
    menubar = Menu(preview_window)
    preview_window["menu"] = menubar
    menu_file = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label="File")

    # Add Save functionality to File Menu
    menu_file.add_command(label="Save As...", command=lambda: save_file(ascii_art))


# Create the root window
root = Tk()
root.title("ZTM - Ascii Art")
root.iconbitmap("ztm-icon.ico")

# Main Window Frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Labels
ttk.Label(mainframe, text="Select an image:").grid(column=0, row=0, sticky=(W))

# Image path field
image_path = StringVar()
image_entry = ttk.Entry(mainframe, width=50, textvariable=image_path).grid(column=1, row=1, sticky=(W, E), padx=0)

# Buttons
ttk.Button(mainframe, text="Browse", command=browse_image).grid(column=0, row=1, sticky=(W))
ttk.Button(mainframe, text="Convert", command=convert_image).grid(column=0, row=2, sticky=(W))

# Add padding
for child in mainframe.winfo_children():
    child.grid_configure(padx=0, pady=5)

# Run mainloop
root.mainloop()
