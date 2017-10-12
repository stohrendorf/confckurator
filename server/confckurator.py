from flask import Flask, redirect

from api import get_pack_api_blueprint, get_template_api_blueprint, get_environment_api_blueprint
from db import make_session, Pack, Template, Variable, Value, Environment, boot_database, Tag

app = Flask(__name__)


@app.route('/')
def home_redirect():
    return redirect('/static/')


@app.route('/static/')
def home():
    return app.send_static_file('index.html')


def seed_data():
    with make_session() as session:
        tag = Tag(name="nice")
        session.add(tag)
        template = Template(name="test", text="whoa = {{xxx_var}}", tags=[tag])
        session.add(template)
        variable = Variable(name="xxx_var", description="me gusta", template=template)
        session.add(variable)
        env = Environment(name="rotlicht")
        session.add(env)
        pack = Pack(name="fun")
        session.add(pack)
        value = Value(variable=variable, environment=env, pack=pack, data="injection")
        session.add(value)


app.register_blueprint(get_pack_api_blueprint())
app.register_blueprint(get_template_api_blueprint())
app.register_blueprint(get_environment_api_blueprint())

if __name__ == '__main__':
    app.testing = True
    app.config['database'] = 'sqlite:///:memory:'

    boot_database(app)
    if app.testing:
        seed_data()
    app.run()
