import json
import os
import uuid

from werkzeug.utils import secure_filename

from sweater import ALLOWED_EXTENSIONS, app, UPLOAD_FOLDER, db
from sweater.model import ImageInfo


class File:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def save(file):

        if file and File.allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   secure_filename(filename)))
            return filename
        else:
            return False

    @staticmethod
    def store(data):

        record = ImageInfo(
            type_of_task=data.get('type'),
            date=data.get('date'),
            labels=json.dumps(data.get('labels')),
            input_path=data.get('input_path'),
            output_path=data.get('output_path')
        )

        db.session.add(record)
        db.session.commit()

        return record
