#!/usr/bin/env python3
import click
import sys

from ascii_art.ascii_art import (all_supported_files, ascii_textinput, process, show_clock, show_credits,
                                 COLOR_OPTIONS, SUPPORTED_IMAGE_TYPES, ascii_text, show_timer)


@click.group()
def main():
    pass


@main.command()
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.option('-r', '--reverse', is_flag=True, help='reverse the ASCII_CHARS')
@click.option('-s', '--save', is_flag=True,
              help='save the output to file (by default the output file is [input_file]_output.txt)')
@click.option('-o', '--output', default=None, type=click.Path(),
              help='Specify the name of the output file instead of using the default. -s is implied.')
@click.option('-w', '--width', default=100, type=int,
              help='scale the image to fit a custom width')
@click.option('--all', is_flag=True, help='convert all supported files')
@click.option('-c', '--color', type=click.Choice(COLOR_OPTIONS, case_sensitive=False), default='black',
              help='Set output color')
@click.option('-hr', '--highres', is_flag=True, help='Converts using a wide range of Ascii characters.')
def convert(input_files, reverse, save, output, width, all, color, highres):
    """
    Converts images to text files, using ascii characters to display it.
    """
    if all:
        input_files = all_supported_files()

    for file in input_files:
        process(file, reverse=reverse, save=save,
                output=output, width=width, color=color.lower(), highres=highres)
    if not input_files and len(sys.argv) == 1:
        print("Image not specified. Please specify image or add --help for help.")


@main.command(help='list supported image formats and exit.')
def types():
    print(', '.join(SUPPORTED_IMAGE_TYPES))


@main.command(help="Show credits")
def credits():
    show_credits()


@main.command(help='show clock as a colorful animation. resize the terminal or press "q" or "x" to exit the clock.')
def clock():
    show_clock()


@main.command(help='Convert simple text into ASCII text format. Will prompt for the text if not specified.')
@click.argument("words", type=str, default=None, nargs=-1)
def text(words):
    if not words:
        ascii_textinput()
    else:
        ascii_text(" ".join(words))


@main.command(help='Count down n seconds to zero.')
@click.argument("seconds", type=int, default=10)
def timer(seconds: int):
    show_timer(seconds)


if __name__ == '__main__':
    main()
