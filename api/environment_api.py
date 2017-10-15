from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from typing import List

from marshmallow import fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
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

    new_environment_args = {
        'name': fields.String(required=True, validate=validate.Length(min=1, max=255), trim=True)
    }

    @staticmethod
    @use_kwargs(new_environment_args)
    def post(name: str):
        environment = Environment(name=name.strip())
        with make_session() as session:
            session.add(environment)
            session.commit()
            return make_id_response(environment.id)


# noinspection PyTypeChecker
environment_api.add_resource(EnvironmentList, '/')


def get_environment_api_blueprint():
    return environment_blueprint
