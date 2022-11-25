from sweater import db


class ImageInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type_of_task = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=True)
    labels = db.Column(db.Text, nullable=True)
    input_path = db.Column(db.String, nullable=True)
    output_path = db.Column(db.String, nullable=True)
