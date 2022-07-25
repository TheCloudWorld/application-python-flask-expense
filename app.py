# from crypt import methods
from pydoc import render_doc
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# Configure the X-Ray recorder to generate segments with our service name
xray_recorder.configure(service='secondary')
XRayMiddleware(app, xray_recorder)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///wilshan.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Mm(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.expense}"

@app.route('/', methods=['GET', 'POST'])
def table():
    if request.method== "POST":
  #      print(request.form["expense"])
        name = request.form['expense']
        value  = request.form['cost']
        mm = Mm(expense=name, cost=value)
        db.session.add(mm)
        db.session.commit()
    allShow = Mm.query.all()
#    print(allShow)
    return render_template('table.html', allshow=allShow)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method== "POST":
        name = request.form['expense']
        value  = request.form['cost']
        mm = Mm.query.filter_by(sno=sno).first()
        mm.expense = name
        mm.cost = value
        db.session.add(mm)
        db.session.commit()
        return redirect("/")
    update = Mm.query.filter_by(sno=sno).first()
    return render_template('update.html', update=update)

@app.route('/delete/<int:sno>')
def delete(sno):
    delete = Mm.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/")

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)

