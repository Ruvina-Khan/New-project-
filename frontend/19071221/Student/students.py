from flask import Flask,Blueprint, render_template,session

students= Blueprint("students",__name__,static_folder='static',template_folder='template')

@students.route("/")
def home():
    if "type" in session:
        type_ =  session['type']
        return render_template("Student_Home.html",val= type_.upper())

@students.route("//publishers")
def publishers():
    if "type" in session:
        type_ =  session['type']
        return render_template("Publishers.html",val= type_.upper())
