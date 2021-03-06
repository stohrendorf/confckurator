import yaml
from flask import Flask, redirect
from flask_login import LoginManager

from api import get_pack_api_blueprint, get_template_api_blueprint, get_environment_api_blueprint, \
    get_instance_api_blueprint
from db import make_session, Pack, Template, Variable, Value, Environment, boot_database, Instance

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home_redirect():
    return redirect('/static/frontend/')


@app.route('/static/frontend/')
def home():
    return app.send_static_file('frontend/index.html')


def load_template(filename: str):
    with open(filename) as file:
        template = yaml.load(file)

    tpl = Template(name=template['name'], text=template['text'])
    for varname, properties in template['variables'].items():
        tpl.variables.append(Variable(name=varname, description=properties['description']))

    with make_session() as session:
        session.add(tpl)


def seed_data():
    load_template('seeds/apache-vhost.template.yml')

    with make_session() as session:
        template = Template(name="test", text="whoa = {{xxx_var}};"
                                              " template={{_meta.template}};"
                                              " environment={{_meta.environment}};"
                                              " pack={{_meta.pack}}")
        session.add(template)
        variable = Variable(name="xxx_var", description="me gusta", template=template)
        session.add(variable)
        env = Environment(name="rotlicht")
        session.add(env)
        pack = Pack(name="fun")
        session.add(pack)
        instance = Instance(name="some/instance", pack=pack, template=template)
        value = Value(variable=variable, environment=env, instance=instance, data="injection")
        session.add(value)


app.register_blueprint(get_pack_api_blueprint())
app.register_blueprint(get_template_api_blueprint())
app.register_blueprint(get_environment_api_blueprint())
app.register_blueprint(get_instance_api_blueprint())

if __name__ == '__main__':
    app.testing = True
    app.config['database'] = 'sqlite:///:memory:'

    boot_database(app)
    if app.testing:
        seed_data()
    app.run()
