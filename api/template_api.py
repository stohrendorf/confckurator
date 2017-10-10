import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from db import make_session, Template, Variable

template_blueprint = Blueprint('template_blueprint', __name__, url_prefix='/api')
template_api = Api(template_blueprint)

variable_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

template_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tags': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    })),
    'variables': fields.List(fields.Nested(variable_fields))
}


class TemplateResource(Resource):
    def get(self, template_id):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).all()  # type: list[Template]
            if len(data) != 1:
                return {'error': "Requested template does not exist"}, werkzeug.exceptions.Gone.code

            return marshal(data[0], template_fields)

    def delete(self, template_id):
        with make_session() as session:
            data = session.query(Template).filter(Template.id == template_id).all()  # type: list[Template]
            if len(data) != 1:
                return {'error': "Requested template does not exist"}, werkzeug.exceptions.Gone.code

            session.delete(data[0])
            return {}


template_api.add_resource(TemplateResource, '/template/<int:template_id>')


class TemplateList(Resource):
    def get(self):
        with make_session() as session:
            return marshal(session.query(Template).all(), template_fields)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('text')
        args = parser.parse_args()

        template = Template(name=args['name'], text=args['text'])
        with make_session() as session:
            session.add(template)
            session.commit()
            return {'id': template.id}


template_api.add_resource(TemplateList, '/template')


class TemplateVariableList(Resource):
    def get(self, template_id):
        with make_session() as session:
            return marshal(session.query(Variable).filter(Variable.template_id == template_id).all(), variable_fields)

    def post(self, template_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('description')
        args = parser.parse_args()

        variable = Variable(template_id=template_id, name=args['name'], description=args['description'])
        with make_session() as session:
            session.add(variable)
            session.commit()
            return {'id': variable.id}


template_api.add_resource(TemplateVariableList, '/template/<int:template_id>/variable')


def get_template_api_blueprint():
    return template_blueprint
