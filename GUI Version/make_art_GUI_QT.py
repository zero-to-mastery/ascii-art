# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
import os
import sys
import tkinter 
import tkinter.font as tkfont
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog as fd
from PIL import Image

ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']


# Modified example code for Creating GUI Application using Tkinter by @Jude_Savio
app = tkinter.Tk()
text_box = scrolledtext.ScrolledText(app,bg='white',fg='#4682B4')
text_box.tag_configure("center",justify="center")
image_path = ''
message = ''

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
        print('Successful')
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image)
    message = image_ascii
    print((message))
    text_box.insert(tkinter.INSERT,message)
    text_box.tag_add("center", "1.0", "end")

def browse_file():
    """ For Getting the file path that gets chosen by the user 
    """
    filename = fd.askopenfilename()
    print('Browse File Function - ',filename)
    image_path = filename
    handle_image_conversion((image_path))

def quit_app():
    """ To quit the mainloop of the app
    """
    app.destroy()

def create_window(): 
    """ Specifying the Structure and the widgets of the app
    """ 

    app.title("ASCII-QT")
    app.minsize(900,400)
    app.configure(bg='#003366')
    font = tkfont.Font(family="Sans Serif" ,size=20, weight="bold")
    bt_font = tkfont.Font(family="Sans Serif" ,size=10, weight="bold")
    label = tkinter.Label(app, text="ASCII ART",font=font, bg='#003366',fg='white')
    label.pack(pady=10)
    text_box.pack(pady=30,expand=True, fill='both')
    button_frame = tkinter.Frame(app,bg='#003366')
    button_frame.pack(side='bottom',pady=15)
    choose_button = tkinter.Button(button_frame, text="Choose",width=10,activebackground='white',activeforeground='#4682B4',font=bt_font,command=browse_file)
    cancel_button = tkinter.Button(button_frame,text="Quit",width=10,activebackground='white',activeforeground='#4682B4',font=bt_font,command=quit_app)
    choose_button.pack(side = 'left',padx=25)
    cancel_button.pack(side = 'left',padx=25)
    app.mainloop()

def main():
    create_window()
    
if __name__=='__main__':
    main()