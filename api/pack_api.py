from flask.blueprints import Blueprint
from flask_restful import Resource, reqparse, marshal, Api
from sqlalchemy import and_
from typing import List
from werkzeug.exceptions import NotFound, Conflict

from api.common import make_id_response, make_empty_response
from api.marshalling import pack_fields
from db import make_session, Pack, Value, Template

pack_blueprint = Blueprint('pack_blueprint', __name__, url_prefix='/api/pack')
pack_api = Api(pack_blueprint)


class PackResource(Resource):
    @staticmethod
    def get(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: List[Pack]
            if len(data) != 1:
                raise NotFound("Requested pack does not exist")

            return marshal(data[0], pack_fields)

    @staticmethod
    def delete(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: List[Pack]
            if len(data) != 1:
                raise NotFound("Requested pack does not exist")

            session.delete(data[0])
            return make_empty_response()


# noinspection PyTypeChecker
pack_api.add_resource(PackResource, '/<int:pack_id>')


class PackList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Pack).all(), pack_fields)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, trim=True)
        args = parser.parse_args(strict=True)

        pack = Pack(name=args['name'])
        with make_session() as session:
            session.add(pack)
            session.commit()
            return make_id_response(pack.id)


# noinspection PyTypeChecker
pack_api.add_resource(PackList, '/')


class PackVariableResource(Resource):
    @staticmethod
    def post(pack_id, variable_id):
        parser = reqparse.RequestParser()
        parser.add_argument('environment_id', required=False, type=int, nullable=True, store_missing=False)
        parser.add_argument('data', required=True)
        args = parser.parse_args(strict=True)

        with make_session() as session:
            environment_id = args['environment_id'] if 'environment_id' in args else None
            print(environment_id)
            if environment_id is None:
                value = session.query(Value).filter(
                    and_(Value.variable_id == variable_id,
                         Value.pack_id == pack_id)).first()
            else:
                value = session.query(Value).filter(
                    and_(Value.variable_id == variable_id,
                         Value.environment_id == environment_id,
                         Value.pack_id == pack_id)).first()

            if value is None:
                value = Value(pack_id=pack_id, environment_id=environment_id, variable_id=variable_id,
                              data=args['data'])
                session.add(value)
            else:
                value.data = args['data']

            session.commit()
            return make_empty_response()

    @staticmethod
    def delete(pack_id, variable_id):
        parser = reqparse.RequestParser()
        parser.add_argument('environment_id', required=False, type=int, nullable=True)
        args = parser.parse_args(strict=True)

        with make_session() as session:
            environment_id = args['environment_id']
            if environment_id is None:
                value = session.query(Value).filter(
                    and_(Value.variable_id == variable_id,
                         Value.pack_id == pack_id)).first()
            else:
                value = session.query(Value).filter(
                    and_(Value.variable_id == variable_id,
                         Value.environment_id == environment_id,
                         Value.pack_id == pack_id)).first()

            if value is None:
                raise NotFound("Requested value does not exist in the specified pack")

            session.delete(value)
            return make_empty_response()


# noinspection PyTypeChecker
pack_api.add_resource(PackVariableResource, '/<int:pack_id>/variable/<int:variable_id>')


class PackTemplateResource(Resource):
    @staticmethod
    def post(pack_id, template_id):
        with make_session() as session:
            pack = session.query(Pack).filter(Pack.id == pack_id).first()
            if pack is None:
                raise NotFound("Requested pack not found")

            template = session.query(Template).filter(Template.id == template_id).first()
            if template is None:
                raise NotFound("Requested template not found")

            if template in pack.get_templates():
                raise Conflict("Requested template is already attached to requested pack")

            for variable in template.variables:
                value = Value(variable=variable, environment=None, pack=pack, data="")
                session.add(value)

        return make_empty_response()

    @staticmethod
    def delete(pack_id, template_id):
        with make_session() as session:
            pack = session.query(Pack).filter(Pack.id == pack_id).first()
            if pack is None:
                raise NotFound("Requested pack not found")

            template = session.query(Template).filter(Template.id == template_id).first()
            if template is None:
                raise NotFound("Requested template not found")

            if template not in pack.get_templates():
                raise NotFound("Requested template is not attached to requested pack")

            for variable in template.variables:
                for value in pack.values:
                    if value.variable == variable:
                        print("Del {}".format(repr(value)))
                        session.delete(value)

        return make_empty_response()


# noinspection PyTypeChecker
pack_api.add_resource(PackTemplateResource, '/<int:pack_id>/template/<int:template_id>')


def get_pack_api_blueprint():
    return pack_blueprint
