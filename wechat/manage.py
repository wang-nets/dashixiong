# -*- coding: utf-8 -*-
from flask_script import Manager, Command, Option, prompt_bool
from wechat import app
from wechat.models import DbEngine, MODEL_BASE

try:
    from gunicorn.app.base import BaseApplication
    from gunicorn.six import iteritems

    GUNICORN = True
except ImportError:
    # Gunicorn does not yet support Windows.
    # See issue #524. https://github.com/benoitc/gunicorn/issues/524
    # For dev on Windows, make this an optional import.
    print('Could not import gunicorn, skipping.')
    GUNICORN = False

manager = Manager(app)


@manager.command
def init_db():
    """ create the database. """
    """
    from wechat.models.models_base import Provinces, Universities, Majors, Students, Colleges
    """
    engine = DbEngine.get_instance().get_engine()
    MODEL_BASE.metadata.create_all(engine)


@manager.command
def drop_db():
    """ drop the database"""
    if prompt_bool(
            "Are you sure you want to lose all your data"):
        """
        from wechat.models.models_base import Provinces, Universities, Majors, Students
        """

        engine = DbEngine.get_instance().get_engine()
        MODEL_BASE.metadata.drop_all(engine)


class APIServer(Command):
    def __init__(self, host='0.0.0.0', port=app.config.get('API_PORT'), workers=12):
        self.address = "{}:{}".format(host, port)
        self.workers = workers

    def get_options(self):
        return (
            Option('-b', '--bind',
                   dest='address',
                   type=str,
                   default=self.address),
            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def run(self, workers, address):
        if not GUNICORN:
            print('GUNICORN not installed. Try `runserver` to use the Flask debug server instead.')
        else:
            class FlaskApplication(BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super(FlaskApplication, self).__init__()

                def load_config(self):
                    config = dict([(key, value) for key, value in iteritems(self.options)
                                   if key in self.cfg.settings and value is not None])
                    for key, value in iteritems(config):
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return self.application

            options = {
                'bind': address,
                'workers': workers,
                'timeout': 1800
            }
            FlaskApplication(app, options).run()


def main():
    manager.add_command("run_api_server", APIServer())
    manager.run()


if __name__ == "__main__":
    main()
