import os

from flask import Flask, request, jsonify
from passporteye import read_mrz
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/documents/identify", methods=["POST"])
def upload_photo():
    photo = request.files.get("photo")
    file_name = secure_filename(photo.filename)

    if photo and valid_file(file_name):
        images_dir = os.path.join(os.path.abspath(os.getcwd()), "images")
        img_path = os.path.join(images_dir, file_name)
        photo.save(img_path)
        result = identify_image(img_path)
        return jsonify(result), 200
    return jsonify({"error": "invalid file"}), 400


def valid_file(filename):
    return "." in filename and filename.split(".")[1].lower() in [
        "jpg",
        "jpeg",
        "png",
    ]


def identify_image(img_path):
    mrz = read_mrz(img_path)
    result_dict = {"passport": False, "national_id": False}
    if mrz:
        if mrz.type == "ID":
            result_dict["national_id"] = True
        else:
            result_dict["passport"] = True
    return result_dict



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)