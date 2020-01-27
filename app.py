# Imports
from flask import Flask
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from flask_graphql import GraphQLView
from flask_cors import CORS
import os
from db import db
from env import admin_default_pass, admin_seeder

basedir = os.path.abspath(os.path.dirname(__file__))

# app initialization
app = Flask(__name__)
CORS(app)
app.debug = True

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "somesecret"

# seeders


class AdminSeeder(Command):
    "prints hello world"

    def run(self):
        from models.user import User
        if admin_seeder & admin_seeder == True:
            user = User(username='admin')
            user.set_password(
                admin_default_pass if admin_default_pass else '123456')
            db.session.add(user)
            db.session.commit()
        else:
            print('admin_seeder is inactive, checkout the env.py')


# Modules
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('seed_admin', AdminSeeder())


# Routes


@app.route('/')
def index():
    return '<p>Stats may be?</p>'


if __name__ == '__main__':
    from schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # for having the GraphiQL interface
        )
    )
    manager.run()
