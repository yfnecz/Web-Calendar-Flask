import sys
from flask import Flask, jsonify, abort, request
from flask_restful import Resource, Api, reqparse, inputs
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

    def to_json(self):
        return {"id": self.id, "event": self.event, "date": str(self.date)}


db.create_all()


class EventAddList(Resource):
    def get(self):
        start = request.args.get('start_time')
        end = request.args.get('end_time')
        events = Event.query.all()
        if start is not None:
            events = [event for event in events if str(event.date) >= start]
        if end is not None:
            events = [event for event in events if str(event.date) <= end]
        events = [event.to_json() for event in events]
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


class EventsTodayResponse(Resource):
    def get(self):
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        events = [event.to_json() for event in events]
        return jsonify(events)


class EventGetDelete(Resource):
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event.to_json()

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"}


api.add_resource(EventGetDelete, '/event/<int:event_id>')
api.add_resource(EventAddList, '/event/')
api.add_resource(EventsTodayResponse, '/event/today')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
