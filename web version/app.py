import time
from pathlib import Path
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from oop_version.make_art_oo import ConvertImageToASCII

app = Flask(__name__)

BASE_DIR = Path(__file__).parent.as_posix()
app.config["IMAGE_UPLOADS"] = f"{BASE_DIR}/input_images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG"]
app.config["MAX_IMAGE_FILESIZE"] = 5 * 1024 * 1024

file_path = ""


def allowed_image(filename):
    # accept only files with .ext
    if '.' not in filename:
        return False

    # accept only .png or .jpg file extensions
    ext = filename.rsplit('.', 1)[1]
    if not ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return False
    return True


def allowed_image_size(filesize):
    if not int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def img_upload():
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_size(request.cookies["filesize"]):
                    print("filesize exceeded max limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("no filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    if not Path.exists(Path("./input_images")):
                        Path.mkdir(Path(app.config["IMAGE_UPLOADS"]))

                    # make sure the path is a unix based path to escape dependency from oop_version for windows users
                    full_path = Path.joinpath(Path(app.config["IMAGE_UPLOADS"]), Path(filename)).as_posix()
                    image.save(full_path)

                    # convert image to acsii
                    ascii_convert_obj = ConvertImageToASCII(file_path=full_path, option="-s")
                    global file_path
                    file_path = ascii_convert_obj.handle_image_conversion()

                    # display ascii art in webpage
                    return render_template('img-display.html', content=file_path)

                else:
                    print("only png files are accepted")
                    return redirect(request.url)

            return redirect(request.url)
    return render_template("img-upload.html")


def clean_up(file):
    pass


if __name__ == "__main__":
    app.run(debug=True)
