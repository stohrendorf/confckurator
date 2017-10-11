from typing import List

import werkzeug.exceptions
from flask.blueprints import Blueprint
from flask_restful import Resource, Api, reqparse, marshal

from api.common import make_id_response, make_empty_response
from api.marshalling import pack_fields
from db import make_session, Pack

pack_blueprint = Blueprint('pack_blueprint', __name__, url_prefix='/api')
pack_api = Api(pack_blueprint)


class PackResource(Resource):
    @staticmethod
    def get(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: List[Pack]
            if len(data) != 1:
                return {'error': "Requested pack does not exist"}, werkzeug.exceptions.NotFound.code

            return marshal(data[0], pack_fields)

    @staticmethod
    def delete(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).all()  # type: List[Pack]
            if len(data) != 1:
                return {'error': "Requested pack does not exist"}, werkzeug.exceptions.NotFound.code

            session.delete(data[0])
            return make_empty_response()


# noinspection PyTypeChecker
pack_api.add_resource(PackResource, '/pack/<int:pack_id>')


class PackList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Pack).all(), pack_fields)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, trim=True)
        args = parser.parse_args()

        pack = Pack(name=args['name'])
        with make_session() as session:
            session.add(pack)
            session.commit()
            return make_id_response(pack.id)


# noinspection PyTypeChecker
pack_api.add_resource(PackList, '/pack')


def get_pack_api_blueprint():
    return pack_blueprint
