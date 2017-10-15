from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from sqlalchemy import and_
from typing import List
from werkzeug.exceptions import NotFound, Conflict
from marshmallow import fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from api.common import make_id_response, make_empty_response
from api.marshalling import pack_fields
from db import make_session, Pack, Value, Template

pack_blueprint = Blueprint('pack_blueprint', __name__, url_prefix='/api/pack')
pack_api = Api(pack_blueprint)


@pack_api.resource('/<int:pack_id>')
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


@pack_api.resource('/')
class PackList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Pack).all(), pack_fields)

    new_pack_args = {
        'name': fields.String(required=True, validate=validate.Length(min=1, max=255), trim=True)
    }

    @staticmethod
    @use_kwargs(new_pack_args)
    def post(name):
        pack = Pack(name=name.strip())
        with make_session() as session:
            session.add(pack)
            session.commit()
            return make_id_response(pack.id)


@pack_api.resource('/<int:pack_id>/variable/<int:variable_id>')
class PackVariableResource(Resource):
    update_variable_args = {
        'environment_id': fields.Integer(required=False, missing=None),
        'data': fields.String(required=True),
        'pack_id': fields.Integer(location='view_args'),
        'variable_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(update_variable_args)
    def post(pack_id, variable_id, environment_id, data):
        with make_session() as session:
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
                              data=data)
                session.add(value)
            else:
                value.data = data

            session.commit()
            return make_empty_response()

    delete_variable_args = {
        'environment_id': fields.Integer(required=False, missing=None),
        'pack_id': fields.Integer(location='view_args'),
        'variable_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(delete_variable_args)
    def delete(pack_id, variable_id, environment_id):
        with make_session() as session:
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


@pack_api.resource('/<int:pack_id>/template/<int:template_id>')
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


def get_pack_api_blueprint():
    return pack_blueprint
