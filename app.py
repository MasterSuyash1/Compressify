from flask import Flask, render_template, request, send_file
import os
import zipfile

app = Flask(__name__)

# Route to render the file upload form
@app.route('/')
def upload_file_form():
    return render_template('upload.html')

# Route to handle file upload and zip creation
@app.route('/upload', methods=['POST'])
def upload_file():
    # Create a temporary directory to store uploaded files
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded files to the temporary directory
    for uploaded_file in request.files.getlist('files'):
        if uploaded_file.filename != '':
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            uploaded_file.save(file_path)

    # Create a zip file containing the uploaded files
    zip_file_path = 'uploaded_files.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    # Clean up temporary directory
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        os.remove(file_path)
    os.rmdir(temp_dir)

    # Send the zip file as a response to the user
    return send_file(zip_file_path, as_attachment=True, download_name='uploaded_files.zip')

if __name__ == '__main__':
    app.run(debug=True)


