from zipfile import BadZipFile
import os
from parser import get_presentation_as_list_of_slides
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def save_list_as_json(data_list, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as file:
        json.dump(data_list, file)

    return file_path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    try:
        slides = get_presentation_as_list_of_slides(file)
    except (BadZipFile, ValueError) as e:
        return "It's not a .pptx file", 400

    uid = '123'
    r = save_list_as_json({"name": file.filename, "slides": slides}, './slides_to_explain', uid)

    #return jsonify({'b': slides})
    return r


if __name__ == "__main__":
    app.run(debug=True)
