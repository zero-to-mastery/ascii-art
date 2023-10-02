from flask import Flask, render_template, request
from PIL import Image
import io
from convert_image import convert_image_to_ascii

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle image upload
        image = request.files["image"]
        if image:
            image = Image.open(io.BytesIO(image.read()))
            ascii_art = convert_image_to_ascii(image)
            return render_template("index.html", ascii_art=ascii_art)

    return render_template("index.html", ascii_art=None)

if __name__ == "__main__":
    app.run(debug=True)
