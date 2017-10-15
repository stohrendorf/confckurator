import re

from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from marshmallow import fields
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound, Conflict, InternalServerError

from api.common import make_id_response, make_empty_response
from api.marshalling import template_fields, variable_fields, template_fields_with_text
from db import make_session, Template, Variable

template_blueprint = Blueprint('template_blueprint', __name__, url_prefix='/api/template')
template_api = Api(template_blueprint)


class TemplateResource(Resource):
    get_args = {
        'with_text': fields.Boolean(required=False, missing=False, location='query'),
        'template_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(get_args)
    def get(template_id, with_text):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if data is None:
                raise NotFound("Requested template does not exist")

            return marshal(data, template_fields_with_text if with_text else template_fields)

    post_args = {
        'text': fields.String(required=True),
        'template_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(post_args)
    def post(template_id, text):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if data is None:
                raise NotFound("Requested template does not exist")

            data.text = text

            return make_id_response(template_id)

    @staticmethod
    def delete(template_id):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if data is None:
                raise NotFound("Requested template does not exist")

            for variable in data.variables:
                if len(variable.values) > 0:
                    raise Conflict("Cannot delete the template because one or more values are referencing it")

            session.delete(data)
            return make_empty_response()


# noinspection PyTypeChecker
template_api.add_resource(TemplateResource, '/<int:template_id>')


class TemplateList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Template).all(), template_fields)

    post_args = {
        'name': fields.String(required=True),
        'text': fields.String(required=True)
    }

    @staticmethod
    @use_kwargs(post_args)
    def post(name, text):
        try:
            with make_session() as session:
                if session.query(session.query(Template).filter(Template.name == name.strip()).exists()).scalar():
                    raise Conflict("A template with the same name already exists")

                template = Template(name=name.strip(), text=text)
                session.add(template)
                session.commit()
                return make_id_response(template.id)
        except IntegrityError:
            raise InternalServerError("Could not create the requested template")


# noinspection PyTypeChecker
template_api.add_resource(TemplateList, '/')


class TemplateVariableList(Resource):
    @staticmethod
    def get(template_id):
        with make_session() as session:
            return marshal(session.query(Variable).filter(Variable.template_id == template_id).all(), variable_fields)

    post_args = {
        'name': fields.String(required=True, validate=validate.Regexp(re.compile('^[a-zA-Z_][a-zA-Z0-9_]*$'))),
        'description': fields.String(required=False, missing='')
    }

    @staticmethod
    @use_kwargs(post_args)
    def post(template_id, name, description):
        with make_session() as session:
            template = session.query(Template).filter(Template.id == template_id).first()
            variable = Variable(template=template, name=name.strip(), description=description.strip())
            session.add(variable)
            session.commit()
            return make_id_response(variable.id)


# noinspection PyTypeChecker
template_api.add_resource(TemplateVariableList, '/<int:template_id>/variable/')


class TemplateVariable(Resource):
    @staticmethod
    def delete(template_id, variable_id):
        with make_session() as session:
            data = session.query(Variable).filter(
                and_(Variable.template_id == template_id, Variable.id == variable_id)).first()  # type: Variable
            if data is None:
                raise NotFound("Requested variable does not exist in template")

            if len(data.values) > 0:
                raise Conflict("Cannot delete the variable because one or more values are referencing it")

            session.delete(data)
            return make_empty_response()

    post_args = {
        'description': fields.String(required=True)
    }

    @staticmethod
    @use_kwargs(post_args)
    def post(template_id, variable_id, description):
        with make_session() as session:
            data = session.query(Variable).filter(
                and_(Variable.template_id == template_id, Variable.id == variable_id)).first()  # type: Variable
            if data is None:
                raise NotFound("Requested variable does not exist in template")

            data.description = description.strip()

            return make_empty_response()


# noinspection PyTypeChecker
template_api.add_resource(TemplateVariable, '/<int:template_id>/variable/<int:variable_id>')


def get_template_api_blueprint():
    return template_blueprint
