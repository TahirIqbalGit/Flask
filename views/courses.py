from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db, Course, User, Enrolled

courses = Blueprint('courses', __name__)
courses_view = Blueprint('courses_view', __name__)


@courses.route('/courses', methods=['GET', 'POST'])
def courses_page():
    course = Course.query.all()
    teacher = User.query.all()
    # for c in course:
    #     print(c.user_id)
    #     teacher = User.query.filter(User.id == c.user_id)
    #     print(teacher)
    return render_template("courses.html", course=course, teacher=teacher)


@courses_view.route('/courses/<title>', methods=['GET', 'POST'])
def courses_view_page(title):
    try:
        course = Course.query.filter(Course.title == title).first()
        # teacher = User.query.filter(course.user_id == User.id).first()
        student = User.query.filter(User.email == session.get('email'), User.password == session.get('password')).first()
        is_enrolled = Enrolled.query.filter(Enrolled.student_id == student.id, Enrolled.course_id == course.id).first()
        if request.method == "POST":
            if student:
                if not is_enrolled.enrollment:
                    is_enrolled.enrollment = True
                    db.session.commit()
                    return redirect(url_for("courses_view.courses_view_page", title=course.title))
                else:
                    enroll_record = Enrolled(enrollment=True, student_id=student.id, course_id=course.id)
                    db.session.add(enroll_record)
                    db.session.commit()
                    # return render_template("courses-single.html", course=course, is_enrolled=is_enrolled)
                    return redirect(url_for("courses_view.courses_view_page", title=course.title))
            else:
                # return render_template("courses-single.html", course=course, is_enrolled=is_enrolled)
                return redirect(url_for("login.login_page"))
        else:
            return render_template("courses-single.html", course=course, is_enrolled=is_enrolled.enrollment)
    except:
        if request.method == "POST":
            return redirect(url_for("login.login_page"))
        # elif student:
        #     return render_template("courses-single.html", course=course, is_enrolled=is_enrolled.enrollment)
        elif not course:
            return redirect(url_for("courses.courses_page"))
        else:
            return render_template("courses-single.html", course=course, is_enrolled=False)

