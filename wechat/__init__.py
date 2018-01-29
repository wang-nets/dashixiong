# -*- coding: utf-8 -*-
from flask import Flask
import os
import stat
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import sys
from flask_cors import CORS
from logging import Formatter, handlers
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from logging.config import dictConfig
from logging import DEBUG

app = Flask(__name__)

CORS(app)

# If DASHIXIONG_SETTINGS is set, then use that.
# Otherwise, use env-config/config.py
if os.environ.get('DASHIXIONG_SETTINGS'):
    app.config.from_envvar('DASHIXIONG_SETTINGS')
else:
    # find env-config/config.py
    from os.path import dirname, join, isfile
    path = dirname(dirname(__file__))
    path = join(path, 'env-config')
    path = join(path, 'config.py')

    if isfile(path):
        app.config.from_pyfile(path)
    else:
        print('PLEASE SET A CONFIG FILE WITH DASHIXIONG_SETTINGS OR PUT ONE AT env-config/config.py')
        exit(-1)


@app.route('/health_check')
def health_check():
    return 'ok'


api = Api(app)

from wechat.views.v1.province import ProvincePost, ProvinceGetPutDelete
api.add_resource(ProvincePost, '/api/v1/province')
api.add_resource(ProvinceGetPutDelete, '/api/v1/<int:province_id>/province')

from wechat.views.v1.university import UniversityGet, UniversityPost, UniversityPutDelete
api.add_resource(UniversityPost, '/api/v1/university')
api.add_resource(UniversityGet, '/api/v1/<int:province_id>/university')
api.add_resource(UniversityPutDelete, '/api/v1/<int:province_id>/university/<int:university_id>')

from wechat.views.v1.college import CollegePost, CollegeGet, CollegePutDelete
api.add_resource(CollegePost, '/api/v1/college')
api.add_resource(CollegeGet, '/api/v1/<int:university_id>/college')
api.add_resource(CollegePutDelete, '/api/v1/<int:university_id>/college/<int:college_id>')

from wechat.views.v1.major import MajorPost, MajorGet, MajorPutDelete
api.add_resource(MajorPost, '/api/v1/major')
api.add_resource(MajorGet, '/api/v1/<int:college_id>/major')
api.add_resource(MajorPutDelete, '/api/v1/<int:college_id>/major/<int:major_id>')

from wechat.views.v1.student import StudentPost, StudentGet, StudentPutDelete, StudentUploadGet
api.add_resource(StudentPost, '/api/v1/student')
api.add_resource(StudentGet, '/api/v1/<int:major_id>/student/<string:student_id>')
api.add_resource(StudentPutDelete, '/api/v1/<int:major_id>/student/<string:student_id>')
api.add_resource(StudentUploadGet, '/api/v1/student/<string:student_id>')

from wechat.views.v1.student import PicPost
api.add_resource(PicPost, '/api/v1/picture')

from wechat.views.v1.student import WechatClass
api.add_resource(WechatClass, '/api/v1/openid/<string:res_code>')

db = SQLAlchemy(app)
# Logging


# Use this handler to have log rotator give newly minted logfiles +gw perm
class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        # Rotate the file first.
        handlers.RotatingFileHandler.doRollover(self)

        # Add group write to the current permissions.
        try:
            curr_mode = os.stat(self.baseFilename).st_mode
            os.chmod(self.baseFilename, curr_mode | stat.S_IWGRP)
        except OSError:
            pass


handlers.GroupWriteRotatingFileHandler = GroupWriteRotatingFileHandler


def setup_logging():
    """
    Logging in security_monkey can be configured in two ways.

    1) Vintage: Set LOG_FILE and LOG_LEVEL in your config.
    LOG_FILE will default to stderr if no value is supplied.
    LOG_LEVEL will default to DEBUG if no value is supplied.

        LOG_LEVEL = "DEBUG"
        LOG_FILE = "/var/log/security_monkey/securitymonkey.log"

    2) Set LOG_CFG in your config to a PEP-0391 compatible
    logging configuration.

        LOG_CFG = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s %(levelname)s: %(message)s '
                        '[in %(pathname)s:%(lineno)d]'
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'filename': '',
                    'maxBytes': 10485760,
                    'backupCount': 100,
                    'encoding': 'utf8'
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                }
            },
            'loggers': {
                'wechat': {
                    'handlers': ['file', 'console'],
                    'level': 'DEBUG'
                },
            }
        }
    """
    if not app.debug:
        if app.config.get('LOG_CFG'):
            # initialize the Flask logger (removes all handlers)
            _ = app.logger
            dictConfig(app.config.get('LOG_CFG'))
        else:
            # capability with previous config settings
            # Should have LOG_FILE and LOG_LEVEL set
            if app.config.get('LOG_FILE') is not None:
                handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000000, backupCount=100)
            else:
                handler = StreamHandler(stream=sys.stderr)

            handler.setFormatter(
                Formatter('%(asctime)s %(levelname)s: %(message)s '
                          '[in %(pathname)s:%(lineno)d]')
            )
            app.logger.setLevel(app.config.get('LOG_LEVEL', DEBUG))
            app.logger.addHandler(handler)


setup_logging()