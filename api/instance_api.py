import jinja2
import jinja2.sandbox
from flask.blueprints import Blueprint
from flask_restful import Resource, Api
from werkzeug.exceptions import InternalServerError, NotFound

from db import make_session, Template, Pack

instance_blueprint = Blueprint('instance_blueprint', __name__, url_prefix='/api/instance')
instance_api = Api(instance_blueprint)


def instantiate(pack: Pack, template: Template, environment_id):
    values = {}
    for variable in template.variables:
        value_default = None

        for value in variable.values:
            if value.pack_id != pack.id:
                continue

            if value.environment_id is None:
                value_default = value.data

            if environment_id is None or value.environment_id != environment_id:
                continue

            values[variable.name] = value.data

        if variable.name not in values:
            if value_default is None:
                raise InternalServerError(
                    "The following variable is missing a default value: {}".format(variable.name))

            values[variable.name] = value_default

    tpl_env = jinja2.sandbox.SandboxedEnvironment(undefined=jinja2.StrictUndefined)
    tpl_instance = tpl_env.from_string(template.text)  # type: jinja2.Template

    try:
        return tpl_instance.render(values)
    except jinja2.exceptions.UndefinedError as e:
        raise InternalServerError("Could not render the template: {}".format(e.message))


class InstanceTemplate(Resource):
    @staticmethod
    def get(pack_id, environment_id=None):
        with make_session() as session:
            pack = session.query(Pack).filter(Pack.id == pack_id).first()  # type: Pack
            if pack is None:
                raise NotFound('Requested pack not found')

            result = {}

            for value in pack.values:
                template_name = value.variable.template.name
                if template_name not in result:
                    result[template_name] = {'name': template_name,
                                             'text': instantiate(pack, value.variable.template, environment_id)}

        return result


# noinspection PyTypeChecker
instance_api.add_resource(InstanceTemplate, '/<int:pack_id>/<int:environment_id>')


def get_instance_api_blueprint():
    return instance_blueprint
