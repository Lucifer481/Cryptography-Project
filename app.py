import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from dataProcessing import *
from Threads import *
from hybridCrypt import *
import time

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "null"

# Check if uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('Nofile.html')

        file = request.files['file']
        if file.filename == '':
            return render_template('Nofile.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Original.txt')
            file.save(save_path)

            print(f"✅ File saved as: {save_path}")  # Debugging step
            return start()  # Now calling start() without arguments

    return render_template('Invalid.html')


def start():
    file_path = './Original.txt'
    
    if not os.path.exists(file_path):
        return render_template('Empty.html')

    with open(file_path, 'r') as content:
        first_char = content.read(1)  # Read the first character to check if it's empty

    if not first_char:
        return render_template('Empty.html')
    else:
        return render_template('Option.html')


@app.route('/encrypt/')
def encrypt_file():
    file_path = os.path.join(UPLOAD_FOLDER, "Original.txt")

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return render_template('Empty.html')

    Segment()  # Splitting file
    gatherInfo()  # Gathering metadata
    crypt = HybridCrypt()  # Creating encryption instance
    crypt.encrypt()  # Encrypting data

    return render_template('Option.html')

@app.route('/decrypt/')
def decrypt_file():
    crypt = HybridCrypt()  # Create instance
    crypt.decrypt()  # Perform decryption
    Merge()  # Merge file segments back

    return "Decryption Successful! Download your file from 'Output.txt'"


@app.route('/return-files-data/')
def return_files_data():
    try:
        return send_file('./Output.txt', as_attachment=True)
    except Exception as e:
        return str(e)

def resultE():
    path = "./Segments"
    dir_list = os.listdir(path)
    return render_template('Result.html', dir_list=dir_list)

def resultD():
    return render_template('resultD.html')

if __name__ == '__main__':
    app.run(debug=True)
