from flask.blueprints import Blueprint
from flask_restful import Resource, reqparse, marshal, Api
from typing import List
from werkzeug.exceptions import NotFound

from api.common import make_id_response, make_empty_response
from api.marshalling import environment_fields
from db import make_session, Environment

environment_blueprint = Blueprint('environment_blueprint', __name__, url_prefix='/api/environment')
environment_api = Api(environment_blueprint)


class EnvironmentResource(Resource):
    @staticmethod
    def get(environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).all()  # type: List[Environment]
            if len(data) != 1:
                raise NotFound("Requested environment does not exist")

            return marshal(data[0], environment_fields)

    @staticmethod
    def delete(environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).all()  # type: List[Environment]
            if len(data) != 1:
                raise NotFound("Requested environment does not exist")

            session.delete(data[0])
            return make_empty_response()


# noinspection PyTypeChecker
environment_api.add_resource(EnvironmentResource, '/<int:environment_id>')


class EnvironmentList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            print(session.query(Environment).all())
            return marshal(session.query(Environment).all(), environment_fields)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, trim=True)
        args = parser.parse_args(strict=True)

        environment = Environment(name=args['name'], text=args['text'])
        with make_session() as session:
            session.add(environment)
            session.commit()
            return make_id_response(environment.id)


# noinspection PyTypeChecker
environment_api.add_resource(EnvironmentList, '/')


def get_environment_api_blueprint():
    return environment_blueprint
