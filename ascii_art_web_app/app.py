from flask import Flask, render_template, request
from PIL import Image
from inspect import getsourcefile
from datetime import datetime
import io
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

@app.route("/", methods=["GET", "POST"])
def index():
    season_emoji = None
    # Set emoji for the holiday season
    seasons = {"April":"🐰", "October":"🎃", "December":"🎅"}
    if datetime.now().strftime("%B") in seasons:
        season_emoji = seasons[datetime.now().strftime("%B")]

    if request.method == "POST":
        # Handle image upload
        image = request.files["image"]
        if image:
            image = Image.open(io.BytesIO(image.read()))
            ascii_art = core.convert_image_to_ascii(image)

            return render_template("index.html", ascii_art=ascii_art, season_emoji=season_emoji)

    return render_template("index.html", ascii_art=None, season_emoji=season_emoji)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)