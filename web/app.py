from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from sys import path
from os.path import realpath
path.append(realpath('./../'))
from logic.person import Person

app = Flask(__name__)
bootstrap = Bootstrap(app)
model = []


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/person', methods=['GET'])
def person():
    return render_template('person.html')


@app.route('/person_detail', methods=['POST'])
def person_detail():
    id_person = request.form['id_person']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    p = Person(id_person=id_person, name=first_name, last_name=last_name)
    model.append(p)
    return render_template('person_detail.html', value=p)


@app.route('/person_update/<id>')
def person_update(id):
    edit_person = None
    for person in model:
        if person.id_person == id:
            edit_person = person
            return render_template('person_update.html', value=edit_person)
    return render_template('404.html')

@app.route('/person_edit', methods=['POST'])
def person_edit():
    id_person = request.form['id_person']
    old_person = None
    for person in model:
        if person.id_person == id_person:
            old_person = Person(person.id_person, person.name, person.last_name)
            person.name = request.form['first_name']
            person.last_name = request.form['last_name']
            msg = '{old_person} was updated to {new_person}'.format(
                old_person=old_person, new_person=person)
            return render_template('person_detail.html', value=msg)
    return render_template('404.html')


@app.route('/person_delete/<id>', methods=['GET'])
def person_delete(id):
    for person in model:
        if person.id_person == id:
            temporal_person = person
            model.remove(person)
            msg = '{temporal_person} was deleted'.format(
                temporal_person=temporal_person)
            return render_template('person_detail.html', value=msg)
    return render_template('404.html')


@app.route('/people')
def people():
    data = [(i.id_person, i.name, i.last_name) for i in model]
    print(data)
    return render_template('people.html', value=data)


if __name__ == '__main__':
    app.run()
