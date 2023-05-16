import os
from flask import abort
from app import app, ALLOWED_EXTENSIONS, APP_ROOT


class FileService:
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def ensure_directory_exists(path):
        file_dir = os.path.dirname(path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    def file_request(folder, request, validations):
        if validations.get('entity'):
            abort(403)

        if not 'file' in request.files:
            abort(500)

        try:
            file = request.files['file']

            if file:
                filename = request.form['filename']
                private_url = os.path.join(APP_ROOT, folder, filename)
                FileService.ensure_directory_exists(private_url)
                file.save(private_url)
        except Exception as e:
            abort(500, description=str(e))
