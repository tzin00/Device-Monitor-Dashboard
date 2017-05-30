import os
import socket
from flask_script import Command
from app import db
from config import config


class Setup(Command):
    """
    Initial setup of the application. Creates the database and upload folder.
    """
    def run(self):
        # Get the environment config
        env = os.getenv('FLASK_CONFIG') or 'default'
        
        # Get the database path to verify
        try:
            db_path = config[env].SQLALCHEMY_DATABASE_URI[10:]
        except KeyError:
            print('Incorrect environment set! Options are: development, testing, or production')
            return
        # Get the uploads path to verify
        upload_path = config[env].UPLOAD_FOLDER
        if os.path.isfile(db_path):
            print('Database has already been created')
        else:
            print('Database not found, creating new database')
            db.create_all()
        if os.path.isdir(upload_path):
            print('Uploads folder has already been created')
        else:
            print('Uploads folder not found, creating...')
            os.mkdir(upload_path, 0o777)
        print('Initial setup complete!')
        try:
            import gunicorn
        except ModuleNotFoundError:
            print('Gunicorn is recommended to use with this application\nYou can install with "pip install gunicorn"')
            print('You can run the development server by using "python manage.py runserver"')
        print('Server setup complete!\nRun the server by entering "gunicorn -c gunicorn_conf.py manage:app" on the '
              'command line')
        
        
class Test(Command):
    
    def run(self):
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
