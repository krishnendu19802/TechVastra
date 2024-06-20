from werkzeug.utils import secure_filename
from PIL import Image
import os

UPLOAD_FOLDER = 'uploads/'
# Allow only specific file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def files_save(file,fileName):
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        # Generate a secure filename without extension
        filename = secure_filename(file.filename)
        filename_without_ext = os.path.splitext(filename)[0]
        # Define the custom filename with .jpg extension
        custom_filename = f'{fileName}.jpg'
        save_path = os.path.join(UPLOAD_FOLDER, custom_filename)

        # Convert and save the image as .jpg
        with Image.open(file) as img:
            # Convert image to RGB (required for .jpg format)
            rgb_img = img.convert('RGB')
            rgb_img.save(save_path, 'JPEG')

        return {'message':'File successfully uploaded and saved as .jpg', 'code':200}
    else:
        return {'message':'File type not allowed','code': 400}