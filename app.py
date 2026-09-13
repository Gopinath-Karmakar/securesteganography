print("APP.PY STARTED")

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

import os
import uuid

from werkzeug.utils import secure_filename

from core.secure_embed import secure_embed
from core.secure_extract import secure_extract

from metrics.quality import (
    calculate_mse,
    calculate_psnr,
    image_capacity
)

app = Flask(__name__)

app.secret_key = "steganography_secret_key"

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

ALLOWED_EXTENSIONS = {
    "png",
    "bmp",
    "jpg",
    "jpeg"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/embed", methods=["GET", "POST"])
def embed():

    if request.method == "GET":
        return render_template("embed.html")

    try:

        image = request.files["image"]
        message = request.form["message"]
        password = request.form["password"]

        if image.filename == "":
            flash("Please select an image.")
            return redirect(request.url)

        if not allowed_file(image.filename):
            flash("Only PNG, JPG, JPEG and BMP files are allowed.")
            return redirect(request.url)

        filename = secure_filename(image.filename)

        unique_name = str(uuid.uuid4()) + "_" + filename

        original_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_name
        )

        image.save(original_path)

        output_name = "stego_" + unique_name

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"],
            output_name
        )

        secure_embed(
            image_path=original_path,
            message=message,
            password=password,
            output_path=output_path
        )

        mse = calculate_mse(
            original_path,
            output_path
        )

        psnr = calculate_psnr(
            original_path,
            output_path
        )

        capacity = image_capacity(original_path)

        return render_template(
    "result.html",
    mode="embed",
    image_name=output_name,
    original_image=unique_name,
    stego_image=output_name,
    mse=round(mse,8),
    psnr=round(psnr,2),
    capacity=capacity
)

    except Exception as e:

        return f"<h2>Error</h2><pre>{e}</pre>"
    

@app.route("/extract", methods=["GET", "POST"])
def extract():

    if request.method == "GET":
        return render_template("extract.html")

    image = request.files.get("image")
    password = request.form.get("password")

    if image is None or image.filename == "":
        flash("Please select a stego image.", "warning")
        return redirect(url_for("extract"))

    if not allowed_file(image.filename):
        flash("Only PNG, JPG, JPEG and BMP files are allowed.", "warning")
        return redirect(url_for("extract"))

    filename = secure_filename(image.filename)

    unique_name = str(uuid.uuid4()) + "_" + filename

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_name
    )

    image.save(image_path)

    try:

        message = secure_extract(
            image_path=image_path,
            password=password
        )

        return render_template(
            "result.html",
            mode="extract",
            message=message
        )

    except Exception:

        flash(
            "Incorrect password or hidden message not found.",
            "danger"
        )

        return redirect(url_for("extract"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/download/<filename>")
def download(filename):

    file_path = os.path.join(
        app.config["OUTPUT_FOLDER"],
        filename
    )

    return send_file(
        file_path,
        as_attachment=True
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_file(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )


@app.route("/output/<filename>")
def output_file(filename):

    return send_file(
        os.path.join(
            app.config["OUTPUT_FOLDER"],
            filename
        )
    )

if __name__ == "__main__":
    print("STARTING FLASK SERVER...")
    app.run(host="127.0.0.1", port=5000, debug=True)