from flask import Flask, render_template, request, send_file
from PIL import Image
from inspect import getsourcefile
import io
import base64
import sys
import os.path as path
import importlib

# ugly: @todo change this whole app to work from the same pacakge
dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, dir[:dir.rfind(path.sep)])
core = importlib.import_module("community-version")
sys.path.pop(0)

#from community-version import convert_image_to_ascii
# from convert_image import convert_image_to_ascii

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def image_render():
    if request.method == "POST":
        # Handle image upload
        image = request.files["image"]
        if image:
            image = Image.open(io.BytesIO(image.read()))
            # Convert the image to a base64 string for HTML display
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # Convert image to ascii art
            ascii_art = core.convert_image_to_ascii(image)
            return render_template("ascii_art.html",ascii_art=ascii_art,image_str=img_str)
    return render_template("ascii_art.html",ascii_art=None,image_str=None)

@app.route("/download_ascii",methods=["GET","POST"])
def save_ascii_art():
    if request.method == "POST":
        ascii_art = request.form.get('ascii_art', '')
        with open("ascii_art.txt", "w") as f:
            f.write(ascii_art)
        return send_file("ascii_art.txt", as_attachment=True, download_name="ascii_art.txt")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)