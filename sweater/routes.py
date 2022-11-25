import json

from flask import render_template, request, make_response, redirect, url_for

from helper.Classification import *
#from helper.Segmentation import *
from helper.File import *
from sweater import session


@app.route("/")
def home():
    session.permanent = True
    return render_template('page/home.html')


@app.route("/classification")
def classification():
    classification_data = session['classification'] if 'classification' in session.keys() else ''
    filepath = session['classification_filepath'] if 'classification_filepath' in session.keys() else ''

    return render_template('page/classification.html', classification=classification_data, filepath=filepath)


@app.route("/classification_upload", methods=['POST'])
def classification_image():
    filepath = File.save(request.files['file'])

    classed_image = Classification.handler(filepath)

    file_info = File.store(classed_image)

    session['classification'] = classed_image.get('labels')
    session['classification_filepath'] = classed_image.get('output_path')
    if not session.modified:
        session.modified = True

    return app.redirect('/classification')


@app.route("/segmentation")
def segmentation():
    data = session['filepath'] if 'filepath' in session.keys() else ''
    return render_template('page/segmentation.html', filepath=data)


@app.route("/segmentation_upload", methods=['POST'])
def segmentation_image():
    filepath = File.save(request.files['file'])
    classed_image = Segmentation.handler(filepath)

    file_info = File.store(classed_image)

    session['filepath'] = classed_image.get('output_path')
    if not session.modified:
        session.modified = True

    return app.redirect('/segmentation')


@app.errorhandler(404)
def page_not_not_found(error):
    return render_template('page/404.html')
