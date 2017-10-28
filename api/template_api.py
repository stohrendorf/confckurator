import re

from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from marshmallow import fields, missing
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound, Conflict, InternalServerError

from api.common import make_id_response, make_empty_response
from api.marshalling import template_fields, variable_fields, template_fields_with_text
from audit import audit_log
from db import make_session, Template, Variable

template_blueprint = Blueprint('template_blueprint', __name__, url_prefix='/api/template')
template_api = Api(template_blueprint)


@template_api.resource('/')
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
    def put(name, text):
        audit_log('Create Template: {}', name)

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


@template_api.resource('/<int:template_id>')
class TemplateResource(Resource):
    get_args = {
        'with_text': fields.Boolean(required=False, missing=False, location='query'),
        'template_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(get_args)
    def get(template_id, with_text):
        with make_session() as session:
            template = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if template is None:
                raise NotFound("Requested template does not exist")

            return marshal(template, template_fields_with_text if with_text else template_fields)

    patch_args = {
        'name': fields.String(required=False),
        'text': fields.String(required=False),
        'variables': fields.Nested({
            'delete': fields.List(fields.Integer(required=True)),
            'update': fields.List(fields.Nested({
                'id': fields.Integer(required=True),
                'description': fields.String(required=False, missing=''),
                'name': fields.String(required=False, validate=validate.Regexp(re.compile('^[a-zA-Z_][a-zA-Z0-9_]*$')))
            })),
            'create': fields.List(fields.Nested({
                'name': fields.String(required=True, validate=validate.Regexp(re.compile('^[a-zA-Z_][a-zA-Z0-9_]*$'))),
                'description': fields.String(required=False, missing='')
            }))
        }),
        'template_id': fields.Integer(location='view_args')
    }

    @staticmethod
    @use_kwargs(patch_args)
    def patch(template_id, name, text, variables):
        audit_log('Update Template #{}: {}', template_id, name)

        with make_session() as session:
            template = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if template is None:
                raise NotFound("Requested template does not exist")

            if variables != missing:
                if 'delete' in variables:
                    for d in variables['delete']:
                        to_delete = session.query(Variable).filter(Variable.id == d)
                        if to_delete.first().in_use():
                            raise Conflict('Cannot delete variable because it is in use')
                        to_delete.delete()
                if 'update' in variables:
                    for u in variables['update']:
                        if 'description' in u:
                            variable = session.query(Variable) \
                                .filter(Variable.id == u['id']) \
                                .first()
                            variable.description = u['description'].strip()
                            if 'name' in u:
                                if variable.name != u['name'] and variable.in_use():
                                    raise Conflict('Cannot change name of a variable that\'s in use')
                                variable.name = u['name']
                if 'create' in variables:
                    for c in variables['create']:
                        if 'description' in c:
                            session.add(Variable(template=template,
                                                 name=c['name'].strip(),
                                                 description=c['description'].strip()))

            if text != missing:
                template.text = text

            if name != missing:
                template.name = name

            return make_id_response(template_id)

    @staticmethod
    def delete(template_id):
        audit_log('Delete Template #{}', template_id)

        with make_session() as session:
            template = session.query(Template).filter(Template.id == template_id).first()  # type: Template
            if template is None:
                raise NotFound("Requested template does not exist")

            for variable in template.variables:
                if variable.in_use():
                    raise Conflict("Cannot delete the template because one or more variables are in use")

            session.delete(template)
            return make_empty_response()


@template_api.resource('/<int:template_id>/variable/')
class TemplateVariableList(Resource):
    @staticmethod
    def get(template_id):
        with make_session() as session:
            return marshal(session.query(Variable).filter(Variable.template_id == template_id).all(), variable_fields)


def get_template_api_blueprint():
    return template_blueprint
