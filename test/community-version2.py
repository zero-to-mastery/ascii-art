#!/usr/bin/python3
## Community Version
"""This is class SIMPLEcmd"""

import os
from PIL import Image
import cmd
from example.make_art import convert_image_to_ascii


def is_image_file(path_to_file):
    """
    This function checks if the the file is valid image
    """
    if not os.path.isabs(path_to_file):
        path_to_file = os.path.abspath(path_to_file)

    try:
        with Image.open(path_to_file) as img:
            return True
    except Exception as not_image:
        return False


class SimpleCmd(cmd.Cmd):
    """this is command interpreter class"""
    prompt = "(hackfest) "

    def do_quit(self, arg):
        """This method exit the program"""
        return True

    def do_EOF(self, arg):
        """Exits the program without crashing"""
        print()
        return True

    def helf_quit(self):
        """This is quit method help message"""
        print("Quit command to exit the program\n")

    def do_ascii(self, args):
        """
        converts images to 
        
        convert image to ascii
        Usage: ascii  <image_file_path>
        Example: ascii image.jpg

        when creating multiple images
        Usage: ascii <image_file_path> <image_file_path> <image_file_path>
        Example: ascii imgege1.png image2.png image3.png
        """

        if not args:
            print("** Image missing **")
            return
        all_images = args.split()

        
        def create_many_instances(file):
            
            if is_image_file(file):
                try:
                    with Image.open(file) as image:
                        ascii_img = convert_image_to_ascii(image)
                    print()
                    print(ascii_img)
                    print()
                    print()

                except Exception as e:
                    print("Error occured!", e)
                    return
            else:
                print()
                print(f"{file} is not a valid image file")
                return

        if len(all_images) < 2:
            create_many_instances(all_images[0])
        elif len(all_images) > 1:
            for image in all_images:
                create_many_instances(image)


if __name__ == "__main__":
    SimpleCmd().cmdloop()
