from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    date_created = db.Column(db.DATE, default=datetime.now())
    status = db.Column(db.Boolean, default=False, nullable=False)
    account = db.Column(db.String(12), default='student', nullable=False)


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(2000), nullable=False)
    review = db.Column(db.String(250))
    duration = db.Column(db.String(50))
    lectures = db.Column(db.Integer, nullable=False)
    quizzes = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # To use user table column call as, Course.user.id etc etc
    user = db.relationship("User", backref=db.backref("user", uselist=False))


class Instructor(db.Model):
    __tablename__ = "instructor"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    about = db.Column(db.String(250))
    facebook = db.Column(db.String(100), unique=True)
    instagram = db.Column(db.String(100), unique=True)
    twitter = db.Column(db.String(100), unique=True)
    linkedin = db.Column(db.String(100), unique=True)
    github = db.Column(db.String(100), unique=True)
    stackoverflow = db.Column(db.String(100), unique=True)
    course_id = db.Column(db.Integer, ForeignKey('course.id'))


class Enrolled(db.Model):
    __tablename__ = "enrolled"
    id = db.Column(db.Integer, primary_key=True)
    enrollment = db.Column(db.Boolean, nullable=False)
    student_id = db.Column(db.Integer, ForeignKey('user.id'))
    # user = db.relationship("User", backref=db.backref("user"))
    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    course = db.relationship("Course", backref=db.backref("course"))
