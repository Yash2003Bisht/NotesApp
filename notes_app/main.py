from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    desp = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    update_date = db.Column(db.String(20), nullable=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        notes = Notes(title=request.form['title'], desp=request.form['description'], date=datetime.datetime.now().strftime('%I:%M %p'))
        db.session.add(notes)
        db.session.commit()
        flash("Note Saved Successfully")
    notes_data = Notes().query.all()
    return render_template('index.html', notes_data=notes_data)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    notes = Notes().query.filter_by(id=id).first()
    db.session.delete(notes)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    notes = Notes().query.filter_by(id=id).first()
    if request.method == 'POST':
        notes.title = request.form['title']
        notes.desp = request.form['description']
        notes.update_date = datetime.datetime.now().strftime('%I:%M %p')
        db.session.add(notes)
        db.session.commit()
        flash("Note Updated Successfully")
        return redirect('/')
    return render_template('edit.html', notes=notes)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search = request.form['search']
    notes = Notes().query.all()
    ids = []
    for note in notes:
        if search.lower() in note.title.lower() or search.lower() in note.desp.lower():
            ids.append(note.id)
    print(ids)
    return render_template("search_detail.html", search=search , notes=notes, ids=ids)


if '__main__' == __name__:
    app.run(debug=True)
