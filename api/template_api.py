import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from db import make_session, Template

template_blueprint = Blueprint('template_blueprint', __name__, url_prefix='/api')
template_api = Api(template_blueprint)

template_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'tags': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    })),
    'variables': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }))
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


def get_template_api_blueprint():
    return template_blueprint
