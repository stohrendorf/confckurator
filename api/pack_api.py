from flask.blueprints import Blueprint
from flask_restful import Resource, marshal, Api
from marshmallow import fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from werkzeug.exceptions import NotFound

from api.common import make_id_response, make_empty_response
from api.marshalling import pack_fields
from db import make_session, Pack

pack_blueprint = Blueprint('pack_blueprint', __name__, url_prefix='/api/pack')
pack_api = Api(pack_blueprint)


@pack_api.resource('/<int:pack_id>')
class PackResource(Resource):
    @staticmethod
    def get(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).first()  # type: Pack
            if data is None:
                raise NotFound("Requested pack does not exist")

            return marshal(data, pack_fields)

    @staticmethod
    def delete(pack_id):
        with make_session() as session:
            data = session.query(Pack).filter(Pack.id == pack_id).first()  # type: Pack
            if data is None:
                raise NotFound("Requested pack does not exist")

            session.delete(data)
            return make_empty_response()


@pack_api.resource('/')
class PackList(Resource):
    @staticmethod
    def get():
        with make_session() as session:
            return marshal(session.query(Pack).all(), pack_fields)

    put_args = {
        'name': fields.String(required=True,
                              validate=(validate.Length(min=1, max=255), validate.Regexp('[^/]+')),
                              trim=True)
    }

    @staticmethod
    @use_kwargs(put_args)
    def put(name):
        pack = Pack(name=name.strip())
        with make_session() as session:
            session.add(pack)
            session.commit()
            return make_id_response(pack.id)


def get_pack_api_blueprint():
    return pack_blueprint
