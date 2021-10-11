from flask import Blueprint, render_template

teachers = Blueprint('teachers', __name__)
teachers_view = Blueprint('teacher_view', __name__)


@teachers.route('/teachers')
def teachers_page():
    return render_template("teachers.html")


@teachers_view.route('/teachers-single')
def teachers_view_page():
    return render_template("teachers-single.html")
