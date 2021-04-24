import os
from flask import abort
from app import app, ALLOWED_EXTENSIONS, APP_ROOT, ForbiddenError


class FileService:
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def ensure_directory_exists(path):
        print('FileService.ensure_directory_exists()')
        if not os.path.exists(path):
            os.mkdir(path)

    def file_request(folder, request, validations):
        print('FileService.file_request()')
        if validations['entity']:
            abort(403)

        if not 'file' in request.files:
            abort(500)

        try:
            file = request.files['file']
            # print(request.files['file'])

            if file and FileService.allowed_file(file.filename):
                filename = request.form['filename']
                private_url = os.path.join(APP_ROOT, folder, filename)
                FileService.ensure_directory_exists(private_url)
                # print(private_url)
                # print('\n')
                file.save(private_url)
        except Exception as e:
            abort(500, description='Not found')