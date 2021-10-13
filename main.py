from flask import Flask
from models import db
from views.home import home
from views.about import about
from views.courses import courses, courses_view
from views.events import events
from views.teachers import teachers, teachers_view
from views.blog import blog
from views.contact import contact
from admin.admin import login, signup, logout, admin
from views.shop import shop

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@localhost/{database}"
# ba9ae764e59af3:834d6bc9@us-cdbr-east-04.cleardb.com/heroku_a0fdeca9b5d4d8d?reconnect=true
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://ba9ae764e59af3:834d6bc9@us-cdbr-east-04.cleardb.com" \
                                        "/heroku_a0fdeca9b5d4d8d"
app.config['SECRET_KEY'] = "secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.register_blueprint(home)
app.register_blueprint(about)
app.register_blueprint(courses)
app.register_blueprint(courses_view)
app.register_blueprint(events)
app.register_blueprint(teachers)
app.register_blueprint(teachers_view)
app.register_blueprint(blog)
app.register_blueprint(shop)
app.register_blueprint(contact)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(logout)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)

