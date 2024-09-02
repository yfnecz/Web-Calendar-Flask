import sys
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()


@app.route('/')
def index():
    response = make_response('<h1>The Main Page, OK?</h1>')
    return response


class HelloWorldResource(Resource):
    def get(self):
        events = Event.query.all()
        events = [{"id": event.id, "event": event.event, "date": str(event.date)} for event in events]
        return jsonify(events)


    def post(self):
        args = parser.parse_args()
        event = Event(event=args['event'], date=args['date'])
        db.session.add(event)
        db.session.commit()
        return {"message": "The event has been added!",
                "event": event.event,
                "date": str(event.date)
                }


class EventsResponse(Resource):
    def get(self):
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        events = [{"id": event.id, "event": event.event, "date": str(event.date)} for event in events]
        return jsonify(events)


api.add_resource(HelloWorldResource, '/event/')
api.add_resource(EventsResponse, '/event/today')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
