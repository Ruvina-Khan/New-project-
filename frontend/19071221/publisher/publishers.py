from flask import Flask,Blueprint, render_template,session,current_app, request
from werkzeug.utils import secure_filename
import os

publishers= Blueprint("publishers",__name__,static_folder='static',template_folder='template')
img_path=os.path.join('static','image')

@publishers.route("/")
def home():
    if "type" in session:
        type_ =  session['type']
        image=os.path.join(img_path,'Nature.jpg')
        return render_template("pub_home.html",val=type_,img=image)

@publishers.route("/upload", methods=['POST'])
def img_u():
    if "type" in session:
        if request.method == 'POST':
            f= request.files['pic']
            f.save(os.path.join(img_path, secure_filename(f.filename)))
            return "done"

