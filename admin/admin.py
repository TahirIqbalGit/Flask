from flask import Blueprint, render_template, request, url_for, redirect, session
from models import db, User, Course, Enrolled

# import bcrypt

admin = Blueprint('admin', __name__, static_url_path='/admin', template_folder='templates',
                  static_folder='static')
login = Blueprint('login', __name__)
signup = Blueprint('signup', __name__)
logout = Blueprint('logout', __name__)


@admin.route("/profile", methods=['GET', 'POST'])
def profile():
    if ('email' in session) and ('password' in session):
        user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
        return render_template("admin.html", user=user)
    else:
        return redirect(url_for("login.login_page"))


@admin.route("/profile/edit-profile", methods=['GET', 'POST'])
def edit_profile():
    req = request.form
    if request.method == "POST":

        return redirect(url_for("admin.profile"))
    else:
        user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
        if user:
            user.status = "Active"
            return render_template("edit-profile.html", user=user)
        else:
            return redirect(url_for("login.login_page"))


# FOR STUDENTS
@admin.route("/profile/enrolled-course", methods=['GET'])
def enrolled_course():
    user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
    courses = Enrolled.query.filter(Enrolled.student_id == user.id). \
        filter(Enrolled.course_id == Course.id).all()
    if user:
        return render_template("enrolled-courses.html", user=user, courses=courses)
    else:
        return redirect(url_for("login.login_page"))


@admin.route("/profile/enrolled-course/<id>/check", methods=['GET', 'POST'])
def unenroll_course(id):
    print("Un-Enroll Site")
    if request.method == "POST":
        student = User.query.filter(User.email == session.get('email'),
                                    User.password == session.get('password')).first()
        un_enroll = Enrolled.query.filter(Enrolled.id == id).filter(
            Enrolled.student_id == student.id).first()
        print("Lets see", un_enroll)
        check = request.form.get("check")
        print("Here is Check", check)
        if check == "Un-Enroll":
            # Update to Un-Enroll
            print("Course Un Enrolled")
            un_enroll.enrollment = False
            # un_enroll.student_id = student.id
            # un_enroll.course_id = un_enroll.course_id
            db.session.commit()
            return redirect(url_for('admin.unenroll_course', id=un_enroll.id))
            # return "<h1>Course Remove</h1>"
        if check == "Mark as Complete":
            # Update to Mark Course as Complete
            print("Course Completed")
            return redirect(url_for('admin.unenroll_course', id=un_enroll.id))
            # return "<h1>Course Complete</h1>"
    return redirect(url_for('admin.enrolled_course'))


# FOR TEACHERS
@admin.route("/profile/add-course", methods=['GET', 'POST'])
def add_course():
    req = request.form
    if request.method == "POST":
        # Validating Empty Fields
        missing = list()
        # Getting Immutable Multi Dict Data
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            return redirect(url_for("admin.add_course"))
        else:
            title = req.get("title")
            category = req.get("category")
            price = req.get("price")
            summary = req.get("summary")
            requirements = req.get("requirements")
            duration = req.get("duration")
            lectures = req.get("lectures")
            quizzes = req.get("quizzes")
            print(title, category, price, summary, requirements, duration, lectures,
                  quizzes, sep=', ')

            user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
            record = Course(title=title, category=category, price=price, summary=summary, requirements=requirements,
                            duration=duration, lectures=lectures, quizzes=quizzes, user_id=user.id)
            db.session.add(record)
            db.session.commit()
            return redirect(url_for("admin.profile"))
    else:
        user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
        if user:
            return render_template("add-course.html", user=user)
        else:
            return redirect(url_for("login.login_page"))


@login.route('/login', methods=['GET', 'POST'])
def login_page():
    req = request.form
    print(req)

    if request.method == "POST":
        # Validating Empty Fields
        missing = list()
        # Getting Immutable Multi Dict Data
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            comment = f"Missing field: {',  '.join(missing)}".title()
            return render_template("thanks.html", comment=comment, miss=True)
        else:
            email = req.get("email")
            password = req.get("password")
            print(email, password)
            session['email'] = email
            session["password"] = password

            # user = User.query.filter(User.email == email, User.password == password).first()
            return redirect(url_for('admin.profile'))
    else:
        if ("email" in session) and ("password" in session):
            # user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
            return redirect(url_for("admin.profile"))
        else:
            return render_template("login.html")


@logout.route('/logout', methods=['GET', 'POST'])
def logout_page():
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for("login.login_page"))  # route and function name


@signup.route('/signup', methods=['GET', 'POST'])
def signup_page():
    req = request.form
    print(req)
    # if method post in index
    # if "email" in session:
    #     return redirect(url_for("logged_in"))
    if request.method == "POST":
        # Validating Empty Fields
        missing = list()
        # Getting Immutable Multi Dict Data
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            comment = f"Missing field: {',  '.join(missing)}".title()
            return render_template("thanks.html", comment=comment, miss=True)
        else:
            # getting form data
            fname = req.get("firstname")
            lname = req.get("lastname")
            email = req.get("email")
            password = req.get("password")
            rpassword = req.get("repeatpassword")
            print(fname, lname, email, password, rpassword)
            if password != rpassword:
                print("Password doesn't match")
            else:
                # adding record in database
                record = User(first_name=fname, last_name=lname, email=email, password=password)
                db.session.add(record)
                db.session.commit()
                session['email'] = email
                session["password"] = password
                return render_template("thanks.html", success=True)

        #     # hash the password and encode it
        #     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    else:
        return render_template("signup.html")
