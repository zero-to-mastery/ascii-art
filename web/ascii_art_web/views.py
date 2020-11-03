from pathlib import Path

from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from oop_version.make_art_oo import ConvertImageToASCII

from ascii_art_web import app
from ascii_art_web.util import *


@app.route('/', methods=['GET', 'POST'])
def img_upload():
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_size(request.cookies["filesize"]):
                    flash("filesize exceeded max limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    flash("no filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    if not Path.exists(Path("./input_images")):
                        Path.mkdir(Path(app.config["IMAGE_UPLOADS"]))

                    # make sure the path is a unix based path to escape dependency from oop_version for windows users
                    full_path = Path.joinpath(
                        Path(app.config["IMAGE_UPLOADS"]),
                        Path(filename)).as_posix()
                    image.save(full_path)

                    # convert image to acsii
                    ascii_convert_obj = ConvertImageToASCII(
                        file_path=full_path, option="-s")
                    global file_path
                    file_path = ascii_convert_obj.handle_image_conversion()

                    # display ascii art in webpage
                    return render_template('img-display.html',
                                           content=file_path)

                else:
                    flash("Only PNG or JPG files are accepted.")
                    return redirect(request.url)

            return redirect(request.url)
    return render_template("img-upload.html")
