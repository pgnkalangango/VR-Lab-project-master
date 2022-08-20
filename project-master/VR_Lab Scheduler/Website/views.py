from wsgiref.validate import validator
from flask_wtf import FlaskForm
from sqlalchemy.orm.attributes import flag_modified
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, Schedule
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

#Route to show and push new bookings to the database
@views.route('/schedule', methods=['POST', 'GET'])
def schedule():
    if request.method == "POST":
        date1 = request.form['startdatetime']
        date2 = request.form['enddatetime']
        eqp = request.form['userName']
        postit = Schedule(names=date1, yuh=date2, name=eqp)
        db.session.add(postit)
        db.session.commit()
        flash('Booking made!', category='success')
    return render_template("schedule.html", user=current_user)

#shows all existing bookings/schedules
@views.route('/schedule-list')
def schedule_list():
    sList = Schedule.query.all()
    return render_template("schedule_list.html", tasks=sList, user=current_user)

@views.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    taskToDelete = Schedule.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        sList = Schedule.query.all()
        return render_template("schedule_list.html",tasks=sList, user=current_user)
    except:
        flash("errorrr")

@views.route('/updateSched/<int:id>', methods=['POST', 'GET'])
def updateSched(id):
    taskToUpdate = Schedule.query.get_or_404(id)
    if request.method == 'POST':
        taskToUpdate.names == request.form['userName']
        taskToUpdate.yuh == request.form['startdatetime']
        taskToUpdate.name == request.form['enddatetime']
        try:
            db.session.merge(taskToUpdate)
            db.session.flush()
            db.session.commit()
            sList = Schedule.query.all()
            return render_template("schedule_list.html",tasks=sList, user=current_user)
        except:
            return "ERRORSSSS"
    else:
        return render_template("updateSched.html",tasks=taskToUpdate, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})