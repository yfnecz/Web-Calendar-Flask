import sys
from flask import Flask, request
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('Writing', type=str, help='This is what You will see on The Wall')


@app.route('/')
def index():
    return 'Hello World!'


class HelloWorldResource(Resource):
    def get(self):
        return {"message": "Hello from the REST API!"}


class EventsResponse(Resource):
    def get(self):
        return {"data":"There are no events for today!"}

api.add_resource(HelloWorldResource, '/hello')
api.add_resource(EventsResponse, '/event/today')

class HelloArgs(Resource):
    def get(self):
       data = parser.parse_args()
       return {'data_from_url': data}


# api.add_resource(HelloArgs, '/h/')


@app.route('/data/<megavar>')
def main_view(megavar):
    return f'Your data from URL: {megavar}'


class Hello(Resource):
    def post(self):
        # let's assume we're expecting to receive a JSON body
        # containing key 'message'
        data = request.json
        message = data['message']
        return {"response": "message received"}



if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        #app.run(debug=True)
        app.run()
