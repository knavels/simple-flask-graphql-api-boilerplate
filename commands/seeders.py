from flask_script import Command
from db import db
from env import admin_default_pass, admin_seeder


class AdminSeeder(Command):
    "prints hello world"

    def run(self):
        from models.user import User
        if admin_seeder & admin_seeder == True:
            password = admin_default_pass if admin_default_pass else '123456'
            user = User(username='admin')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print("admin user with password '{}' created successfully".format(password))
        else:
            print('admin_seeder is inactive, check the env.py')
