import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

from db import make_session, Pack

pack_blueprint = Blueprint('pack_blueprint', __name__, url_prefix='/api')
pack_api = Api(pack_blueprint)

pack_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'values': fields.List(fields.Nested({
        'variable_id': fields.Integer,
        'environment_id': fields.Integer,
        'pack_id': fields.Integer
    }))
}


class PackResource(Resource):
    def get(self, pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: list[Pack]
            if len(data) != 1:
                return {'error': "Requested pack does not exist"}, werkzeug.exceptions.Gone.code

            return marshal(data[0], pack_fields)

    def delete(self, pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: list[Pack]
            if len(data) != 1:
                return {'error': "Requested pack does not exist"}, werkzeug.exceptions.Gone.code

            session.delete(data[0])
            return {}


pack_api.add_resource(PackResource, '/pack/<int:pack_id>')


class PackList(Resource):
    def get(self):
        with make_session() as session:
            return marshal(session.query(Pack).all(), pack_fields)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()

        pack = Pack(name=args['name'])
        with make_session() as session:
            session.add(pack)
            session.commit()
            return {'id': pack.id}


pack_api.add_resource(PackList, '/pack')


def get_pack_api_blueprint():
    return pack_blueprint
