#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, jsonify, render_template, request, redirect, flash
import os
from predict import get_prediction
from werkzeug.utils import secure_filename

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
UPLOAD_FOLDER = '/home/jesse_lybianto/msds-434-final/uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print(file)
            result = get_prediction(str(os.path.join(UPLOAD_FOLDER, filename)))
            print(result)

            final_class = []
            final_score = []
            
            for r in result:
                final_class.append(str(r.display_name))
            for s in result:
                final_score.append(s.classification.score)
            res = {final_class[i]: final_score[round(i, 6)] for i in range(len(final_class))}
            print(res)
            return jsonify(res)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)