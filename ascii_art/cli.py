#!/usr/bin/env python3
import click
import sys

from ascii_art.ascii_art import (all_supported_files, ascii_text, process, show_clock, show_credits,
                                 COLOR_OPTIONS, SUPPORTED_IMAGE_TYPES)


@click.command()
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.option('-r', '--reverse', is_flag=True, help='reverse the ASCII_CHARS')
@click.option('-s', '--save', is_flag=True,
              help='save the output to file (by default the output file is [input_file]_output.txt)')
@click.option('-o', '--output', default=None, type=click.Path(),
              help='Specify the name of the output file instead of using the default. -s is implied.')
@click.option('-w', '--width', default=100, type=int,
              help='scale the image to fit a custom width')
@click.option('--credits', is_flag=True, help="Show credits")
@click.option('--clock', is_flag=True,
              help='show clock as a colorful animation. resize the terminal or press "q" or "x" to exit the clock.')
@click.option('--all', is_flag=True, help='convert all supported files')
@click.option('-c', '--color', type=click.Choice(COLOR_OPTIONS, case_sensitive=False), default='black',
              help='Set output color')
@click.option('--text', is_flag=True, help='Convert Simple Text Into Ascii Text Format, Enter Text After Prompt')
@click.option('--types', is_flag=True, help='list supported image formats and exit.')
@click.option('-hr', '--highres', is_flag=True, help='Converts using a wide range of Ascii characters.')
def main(input_files, reverse, save, output, width, credits, clock, all, color, text, types, highres):
    """
    Converts an image to a text file, using ascii characters to display it.
    """
    if types:
        print(', '.join(SUPPORTED_IMAGE_TYPES))
        return
    if clock:
        show_clock()
        return
    if credits:
        show_credits()
        print()

    if all:
        input_files = all_supported_files()

    if text:
        ascii_text()
        return

    for file in input_files:
        process(file, reverse=reverse, save=save,
                output=output, width=width, color=color.lower(), highres=highres)
    if not input_files and len(sys.argv) == 1:
        print("Image not specified. Please specify image or add --help for help.")


if __name__ == '__main__':
    main()
