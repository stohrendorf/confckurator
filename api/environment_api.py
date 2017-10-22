from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from marshmallow import fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound, Conflict

from api.common import make_id_response, make_empty_response
from api.marshalling import environment_fields
from db import make_session, Environment

environment_blueprint = Blueprint('environment_blueprint', __name__, url_prefix='/api/environment')
environment_api = Api(environment_blueprint)


@environment_api.resource('/')
class EnvironmentList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            print(session.query(Environment).all())
            return marshal(session.query(Environment).all(), environment_fields)

    put_args = {
        'name': fields.String(required=True,
                              validate=(validate.Length(min=1, max=255), validate.Regexp('[^/]+')),
                              trim=True)
    }

    @staticmethod
    @use_kwargs(put_args)
    def put(name: str):
        environment = Environment(name=name.strip())
        with make_session() as session:
            session.add(environment)
            session.commit()
            return make_id_response(environment.id)


@environment_api.resource('/<int:environment_id>')
class EnvironmentResource(Resource):
    @staticmethod
    def get(environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).first()  # type: Environment
            if data is None:
                raise NotFound("Requested environment does not exist")

            return marshal(data[0], environment_fields)

    @staticmethod
    def delete(environment_id):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).first()  # type: Environment
            if data is None:
                raise NotFound("Requested environment does not exist")
            if data.in_use():
                raise Conflict("Requested environment is in use")

            session.delete(data)
            return make_empty_response()

    patch_args = {
        'name': fields.String(required=True,
                              validate=(validate.Length(min=1, max=255), validate.Regexp('[^/]+')),
                              trim=True)
    }

    @staticmethod
    @use_kwargs(patch_args)
    def patch(environment_id, name):
        with make_session() as session:
            data = session.query(Environment).filter(Environment.id == environment_id).first()  # type: Environment
            if data is None:
                raise NotFound("Requested environment does not exist")

            data.name = name

            return make_empty_response()


def get_environment_api_blueprint():
    return environment_blueprint
