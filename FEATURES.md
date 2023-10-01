
<<<<<<< HEAD
# T-Crypt 

`USAGE:` python3 script.py <image_file_path> [output_file_path] [brightness]

`Argument Validation:` Validate the command-line input to ensure that the user provides the correct number of arguments and that the provided file path is valid.

`Adjustable Brightness:` Allows adjusting the brightness of the generated ASCII art by mapping pixel intensity to ASCII characters based on different ranges. RANGE [ .0 - 1 ]

`Output to File:` Allow saving the generated ASCII art to a text file instead of printing it to the console. 

`Function Documentation:` Add docstrings to functions to describe what each function does.

`Constants as Uppercase:` Convert ASCII_CHARS to uppercase to indicate that it's a constant.

`Error Handling:` Improve error handling by catching specific exceptions. For instance, catch the FileNotFoundError and PermissionError to provide more informative error messages to the user.

# SmokeRaven667

Made `-p/--path` a required CLI param.
Added option CLI param `-s/--silhouette` to output image as an ASCII silhouette. Defaults to False.


Integrated the project with Django and created HOME view which renders
home.html page.
=======
created class SimpleCmd which emulates command interpreter.
	=> method ascii. takes all args passed to separated by space
>>>>>>> 42de240 (added cmd class where images can be passed one or many)
