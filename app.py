# app.py
from flask import Flask, request, send_file, render_template
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('images')
    image_list = []

    for file in files:
        if file and file.filename.endswith(('jpg', 'jpeg', 'png')):
            image_file = BytesIO()
            file.save(image_file)
            image_file.seek(0)  # إعادة تعيين المؤشر
            img = Image.open(image_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_list.append(img)

    pdf_output = convert_images_to_pdf(image_list)

    return send_file(pdf_output, as_attachment=True, download_name='output.pdf', mimetype='application/pdf')

def convert_images_to_pdf(image_list):
    output = BytesIO()
    if image_list:
        image_list[0].save(output, save_all=True, append_images=image_list[1:], format='PDF')
        output.seek(0)
        return output
    return None

if __name__ == '__main__':
    app.run(debug=True)