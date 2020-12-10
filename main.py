#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, jsonify, render_template, request, redirect, flash, send_file
from google.cloud import storage
import os
from predict import get_prediction
from werkzeug.utils import secure_filename
import tempfile

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# UPLOAD_FOLDER = '/home/jesse_lybianto/msds-434-final/uploads'

app = Flask(__name__)
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLOUD_STORAGE_BUCKET = 'msds-434-final-vcm'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)
    print(blob)
    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    print(blob.public_url)
    print(uploaded_file)
    print(filename)
    print(uploaded_file.filename)
    
    get_blob = bucket.get_blob(uploaded_file.filename)
    print(get_blob)
    downloaded_blob = get_blob.download_as_string()
    print(downloaded_blob)
    # bucket = client.get_bucket('yourbucketname')
    # blob = bucket.blob(filename)
    # with tempfile.NamedTemporaryFile() as temp:
    #     blob.download_to_filename(temp.name)
    #     send_file(temp.name, attachment_filename=uploaded_file.filename)

    # gcs_file = cloudstorage.open(file)
    # contents = gcs_file.read()
    # gcs_file.close()

    result = get_prediction(downloaded_blob)
    print(result)

    final_class = []
    final_score = []
    
    for r in result:
        final_class.append(str(r.display_name))
    for s in result:
        final_score.append(round(s.classification.score, 6))
    res = {final_class[i]: final_score[i] for i in range(len(final_class))}
    print(res)
    return jsonify(res)

# def predict_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No file selected for uploading')
#             return redirect(request.url)
#         if file:
#             filename = secure_filename(file.filename)
#             print("Step1")
#             print(filename)
#             file.upload()
#             print("Step2")
#             print(file)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             print(file)
#             result = get_prediction(str(os.path.join(UPLOAD_FOLDER, filename)))
#             print(result)

#             final_class = []
#             final_score = []
            
#             for r in result:
#                 final_class.append(str(r.display_name))
#             for s in result:
#                 final_score.append(round(s.classification.score, 6))
#             res = {final_class[i]: final_score[i] for i in range(len(final_class))}
#             print(res)
#             return jsonify(res)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)