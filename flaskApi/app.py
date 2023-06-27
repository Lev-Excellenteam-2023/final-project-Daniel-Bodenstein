import logging
from zipfile import BadZipFile
from flask import Flask, request, jsonify
import app_service

app = Flask(__name__)

# Configure the logger
logging.basicConfig(level=logging.DEBUG)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Log request details
    log_message = f"Request Details: Method={request.method}, URL={request.url}, IP={request.remote_addr}, User-Agent={request.user_agent}"
    logging.info(log_message)

    # check if file send
    if 'file' not in request.files:
        error_msg = 'No file found in request!'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        error_msg = 'No file selected!'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    try:
        uid = app_service.upload_pptx(file)
    except (BadZipFile, ValueError) as e:
        error_message = str(e)
        logging.error('Invalid file format: %s', error_message)
        return jsonify({'error_msg': 'Invalid file format: ' + error_message}), 400

    response = {
        'msg': 'File saved successfully!',
        'UID': uid
    }

    logging.info('File uploaded successfully with UID: %s', uid)
    return jsonify(response), 200


@app.route('/explanation', methods=['GET'])
def get_explanation():
    uid = request.args.get('uid')

    if not uid:
        error_msg = 'Missing UID parameter'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    if not app_service.check_if_uid_exist(uid):
        error_msg = 'uid doesnt exist'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    explanation = app_service.get_explanation_by_uid(uid)

    if not explanation:
        error_msg = f'explanation {uid} dont ready'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    return jsonify({'explanation': explanation}), 200


def run_api():
    app.run(debug=True)


if __name__ == '__main__':
    run_api()