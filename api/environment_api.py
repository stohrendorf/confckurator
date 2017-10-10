import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from db import make_session, Environment, Value

environment_blueprint = Blueprint('environment_blueprint', __name__, url_prefix='/api')
environment_api = Api(environment_blueprint)

environment_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'values': fields.List(fields.Nested({
        'variable_id': fields.Integer,
        'environment_id': fields.Integer,
        'pack_id': fields.Integer,
        'data': fields.String
    }))
}


class EnvironmentResource(Resource):
    def get(self, environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).all()  # type: list[Environment]
            if len(data) != 1:
                return {'error': "Requested environment does not exist"}, werkzeug.exceptions.Gone.code

            return marshal(data[0], environment_fields)

    def delete(self, environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).all()  # type: list[Environment]
            if len(data) != 1:
                return {'error': "Requested environment does not exist"}, werkzeug.exceptions.Gone.code

            session.delete(data[0])
            return {}


environment_api.add_resource(EnvironmentResource, '/environment/<int:environment_id>')


class EnvironmentList(Resource):
    def get(self):
        with make_session() as session:
            print(session.query(Environment).all())
            return marshal(session.query(Environment).all(), environment_fields)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('text')
        args = parser.parse_args()

        environment = Environment(name=args['name'], text=args['text'])
        with make_session() as session:
            session.add(environment)
            session.commit()
            return {'id': environment.id}


environment_api.add_resource(EnvironmentList, '/environment')


def get_environment_api_blueprint():
    return environment_blueprint
