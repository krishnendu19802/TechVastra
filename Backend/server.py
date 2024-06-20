from flask import Flask, request, redirect, url_for,send_file
from werkzeug.utils import secure_filename
from PIL import Image
import subprocess
import os
import Helper
app = Flask(__name__)

# Set the folder to save uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def run_script(script_name):
    try:
        completed_process = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        return [True]
    except subprocess.CalledProcessError as e:
        return [False,str(e)]

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    print(request.files)
    if 'person' not in request.files or 'fabric' not in request.files:
        return 'No file part', 400
    person = request.files['person']
    fabric=request.files['fabric']
    value=Helper.files_save(person,'person')
    if(value.get('code')!=200):
        return value.get('message'),value.get('code')
    value2=Helper.files_save(fabric,'fabric')
    if(value2.get('code')!=200):
        return value.get('message'),value.get('code')
    
    #point
    value=run_script('create_mask.py')
    if(value[0]==False):
        return value[1],400
    value=run_script('get_result.py')
    if(value[0]==False):
        return value[1],400
    
    output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], 'result.jpg')
    print(output_image_path)
    # Ensure the output file exists
    if not os.path.exists(output_image_path):
        return 'Output image not found', 500
    print('image found')
    # return send_file(output_image_path, mimetype='image/jpeg')
    return 'saved',200
    # return 'Files saved successfully',200
   

if __name__ == '__main__':
    app.run(debug=True)
