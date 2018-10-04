from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from app.models import xml_details
import xml.etree.ElementTree as ET
from app import app, db
from flask_migrate import Migrate
import os

@app.route('/')
def landing_page():
    tags = ['countertop','island','tap','sink','Not Selected']
    return render_template('index.html', tags=tags)


@app.route('/uploadimg')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        target = os.path.join(app.config['APP_ROOT'], 'app/static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Image directory is already present or Couldn't create Image directory, Please check")
        for upload in request.files.getlist("file"):
            filename = upload.filename
            destination = "/".join([target, filename])
            upload.save(destination)
        return redirect(url_for('get_gallery'))


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('app/static/images')
    return render_template("gallery.html", image_names=image_names )



@app.route('/uploadxml')
def uploadxml():
    return render_template('uploadxml.html')


@app.route('/uploadingxml', methods=['GET', 'POST'])
def uploadingxml():
    if request.method == 'POST':
        db.create_all()
        tags = []
        target = os.path.join(app.config['APP_ROOT'], 'xml_files/')
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("XML directory is already present or Couldn't create the XML directory, Please check")
        if(request.files.getlist("file")):
            for upload in request.files.getlist("file"):
                filename = upload.filename
                print(filename)
                destination = "/".join([target, filename])
                upload.save(destination)

                tree = ET.parse(destination)

                root = tree.getroot()

                for name in root.iter('name'):
                    tags.append(name.text)
                    print(tags)

                for path in root.iter('path'):
                    print(path.text)

                imgfilename = filename.split('.')[0] + ".jpg"

                images_in_db =  xml_details.query.order_by(xml_details.image_name).all()
                images_path = xml_details.query.order_by(xml_details.image_path).all()

                if imgfilename in images_in_db and path.text in images_path:
                    pass
                else:
                    if len(tags) == 1:
                        post = xml_details(image_name=imgfilename, image_path=path.text, tag1=tags[0])
                    elif (len(tags) == 2):
                        post = xml_details(image_name=imgfilename, image_path=path.text, tag1=tags[0], tag2=tags[1])
                    elif (len(tags) == 3):
                        post = xml_details(image_name=imgfilename, image_path=path.text, tag1=tags[0], tag2=tags[1], tag3=tags[2])
                    elif (len(tags) == 4):
                        post = xml_details(image_name=imgfilename, image_path=path.text, tag1=tags[0], tag2=tags[1], tag3=tags[2], tag4=tags[3])

                db.session.add(post)
            db.session.commit()
        return render_template('progress.html')
