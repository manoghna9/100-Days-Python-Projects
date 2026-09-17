from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from collections import Counter
import numpy as np
import os
import uuid


# ==========================================================
# FLASK SETUP
# ==========================================================

app = Flask(__name__)

# Folder where uploaded images will be stored
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the folder if it doesn't already exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allow the browser to access uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
# ==========================================================
# FIND THE MOST COMMON COLOURS
# ==========================================================

def find_common_colours(image_path):
    """
    Opens an image, converts its pixels into a NumPy array,
    and finds the 10 most common RGB colours.
    """

    # Open the image
    image = Image.open(image_path)

    # Convert it to RGB so every pixel has
    # exactly three values: Red, Green and Blue
    image = image.convert("RGB")

    # Convert the image into a NumPy array
    pixels = np.array(image)

    # Example:
    #
    # A pixel might look like:
    # [255, 0, 0]
    #
    # which means:
    # Red = 255
    # Green = 0
    # Blue = 0

    # Turn the 2D/3D pixel array into a list of RGB values
    pixels = pixels.reshape(-1, 3)

    # Count how many times each RGB combination occurs
    colour_counts = Counter(map(tuple, pixels))

    # Get the 10 most common colours
    most_common = colour_counts.most_common(10)

    colours = []

    # Total number of pixels
    total_pixels = len(pixels)

    for rgb, count in most_common:

        red, green, blue = rgb

        # Convert RGB to HEX
        hex_code = "#{:02X}{:02X}{:02X}".format(
            red,
            green,
            blue
        )

        # Calculate what percentage of the image
        # this colour represents
        percentage = round(
            (count / total_pixels) * 100,
            2
        )

        colours.append({
            "hex": hex_code,
            "rgb": f"RGB({red}, {green}, {blue})",
            "percentage": percentage
        })

    return colours


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        colours=None,
        image=None,
        error=None
    )


# ==========================================================
# IMAGE UPLOAD
# ==========================================================

@app.route("/analyse", methods=["POST"])
def analyse():

    # Check whether the user actually selected a file
    if "image" not in request.files:

        return render_template(
            "index.html",
            colours=None,
            image=None,
            error="Please choose an image first."
        )

    file = request.files["image"]

    # Check whether the filename is empty
    if file.filename == "":

        return render_template(
            "index.html",
            colours=None,
            image=None,
            error="Please choose an image first."
        )

    try:

        # Give the uploaded image a unique filename
        extension = os.path.splitext(file.filename)[1].lower()

        filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save the image
        file.save(file_path)

        # Analyse the image
        colours = find_common_colours(file_path)

        # Path used by the browser to display the image
        image_url = f"/uploads/{filename}"

        return render_template(
            "index.html",
            colours=colours,
            image=image_url,
            error=None
        )

    except Exception:

        return render_template(
            "index.html",
            colours=None,
            image=None,
            error="Something went wrong while processing the image."
        )


# ==========================================================
# RUN THE APP
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True, port=6003)