import jinja2
import jinja2.sandbox
from flask.blueprints import Blueprint
from flask_restful import Resource, Api
from werkzeug.exceptions import InternalServerError, NotFound

from db import make_session, Template, Pack, Environment

instance_blueprint = Blueprint('instance_blueprint', __name__, url_prefix='/api/instance')
instance_api = Api(instance_blueprint)


def instantiate(pack: Pack, template: Template, environment: Environment):
    values = {}
    for variable in template.variables:
        value = variable.get_value(pack, environment)
        if value is None:
            raise InternalServerError(
                "The following variable is missing a value: {}".format(variable.name))

        values[variable.name] = value.data

    tpl_env = jinja2.sandbox.SandboxedEnvironment(undefined=jinja2.StrictUndefined)
    tpl_instance = tpl_env.from_string(template.text)  # type: jinja2.Template

    try:
        return tpl_instance.render(values)
    except jinja2.exceptions.UndefinedError as e:
        raise InternalServerError("Could not render the template: {}".format(e.message))


class InstanceTemplate(Resource):
    @staticmethod
    def get(pack_id, environment_id):
        with make_session() as session:
            pack = session.query(Pack).filter(Pack.id == pack_id).first()  # type: Pack
            if pack is None:
                raise NotFound('Requested pack not found')

            environment = session.query(Environment).filter(
                Environment.id == environment_id).first()  # type: Environment
            if environment is None:
                raise NotFound('Requested environment not found')

            result = []

            for template in pack.get_templates():
                result.append({'name': template.name,
                               'text': instantiate(pack, template, environment)})

            return result


# noinspection PyTypeChecker
instance_api.add_resource(InstanceTemplate, '/<int:pack_id>/<int:environment_id>')


def get_instance_api_blueprint():
    return instance_blueprint
