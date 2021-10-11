from flask import Blueprint, render_template

events = Blueprint('events', __name__)


@events.route('/events', methods=['GET'])
def events_page():
    return render_template("events.html")