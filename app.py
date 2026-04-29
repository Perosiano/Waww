import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Pastikan folder upload ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def apply_filter(image_path, filter_type):
    img = cv2.imread(image_path)
    
    if filter_type == 'grayscale':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'sepia':
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img = cv2.transform(img, kernel)
    elif filter_type == 'blur':
        img = cv2.GaussianBlur(img, (15, 15), 0)
    
    cv2.imwrite(image_path, img)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        filter_type = request.form.get('filter')
        
        if file.filename == '':
            return "No selected file"
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Terapkan filter
            apply_filter(filepath, filter_type)
            
            return render_template('index.html', filename=filename)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
