import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, reqparse, marshal, Api
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from api.common import make_id_response, make_empty_response
from api.marshalling import template_fields, variable_fields
from db import make_session, Template, Variable

template_blueprint = Blueprint('template_blueprint', __name__, url_prefix='/api')
template_api = Api(template_blueprint)


class TemplateResource(Resource):
    @staticmethod
    def get(template_id):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if data is None:
                return {'error': "Requested template does not exist"}, werkzeug.exceptions.NotFound.code

            return marshal(data, template_fields)

    @staticmethod
    def delete(template_id):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if data is None:
                return {'error': "Requested template does not exist"}, werkzeug.exceptions.NotFound.code

            for variable in data.variables:
                if len(variable.values) > 0:
                    return {'error': "Cannot delete the template because one or more values are referencing it"}, \
                           werkzeug.exceptions.Conflict.code
            session.delete(data)
            return make_empty_response()


# noinspection PyTypeChecker
template_api.add_resource(TemplateResource, '/template/<int:template_id>')


class TemplateList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Template).all(), template_fields)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, trim=True)
        parser.add_argument('text', required=True)
        args = parser.parse_args(strict=True)

        try:
            with make_session() as session:
                if session.query(session.query(Template).filter(Template.name == args['name']).exists()).scalar():
                    return {'error': "A template with the same name already exists"}, \
                           werkzeug.exceptions.Conflict.code

                template = Template(name=args['name'], text=args['text'])
                session.add(template)
                session.commit()
                return make_id_response(template.id)
        except IntegrityError:
            return {'error': "Could not create the requested template"}, werkzeug.exceptions.InternalServerError.code


# noinspection PyTypeChecker
template_api.add_resource(TemplateList, '/template')


class TemplateVariableList(Resource):
    @staticmethod
    def get(template_id):
        with make_session() as session:
            return marshal(session.query(Variable).filter(Variable.template_id == template_id).all(), variable_fields)

    @staticmethod
    def post(template_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, trim=True)
        parser.add_argument('description', required=False, trim=True, default='')
        args = parser.parse_args(strict=True)

        with make_session() as session:
            template = session.query(Template).filter(Template.id == template_id).first()
            variable = Variable(template=template, name=args['name'], description=args['description'])
            session.add(variable)
            session.commit()
            return make_id_response(variable.id)


# noinspection PyTypeChecker
template_api.add_resource(TemplateVariableList, '/template/<int:template_id>/variable')


class TemplateVariable(Resource):
    @staticmethod
    def delete(template_id, variable_id):
        with make_session() as session:
            data = session.query(Variable).filter(
                and_(Variable.template_id == template_id, Variable.id == variable_id)).first()  # type: Variable
            if data is None:
                return {'error': "Requested variable does not exist in template"}, werkzeug.exceptions.NotFound.code

            if len(data.values) > 0:
                return {'error': "Cannot delete the variable because one or more values are referencing it"}, \
                       werkzeug.exceptions.Conflict.code

            session.delete(data)
            return make_empty_response()


# noinspection PyTypeChecker
template_api.add_resource(TemplateVariable, '/template/<int:template_id>/variable/<int:variable_id>')


def get_template_api_blueprint():
    return template_blueprint
