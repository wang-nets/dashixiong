# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import traceback
from wechat.controllers.college import CollegeController
from flask import request
from wechat.exceptions import InvalidRequestException
LOG = logging.getLogger("wechat")


class CollegePost(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def post(self):
        args = request.json
        args_dict = dict()
        args_dict['college_id'] = args.get('college_id', None)
        args_dict['university_id'] = args.get('university_id', None)
        args_dict['college_name'] = args.get('college_name', None)
        LOG.info("Call url:/api/v1/college, method:POST, college_id:%s, university_id:%s, college_name:%s" %
                 (args_dict['college_id'], args_dict['university_id'], args_dict['college_name']))
        try:
            if not (args_dict['college_name'] and args_dict['university_id'] and args_dict['college_id']):
                InvalidRequestException("The argument is not null")
            college = CollegeController()
            college.add_college_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/college, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class CollegeGet(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self, university_id):
        LOG.info("Call url:/api/v1/college, method:GET, university_id:%s" % university_id)
        try:
            college = CollegeController()
            ret_dict = college.get_college_info_by_university_id(university_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/college, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class CollegePutDelete(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def put(self, university_id, college_id):
        LOG.info("Call url:/api/v1/college, method:PUT, university_id:%s, college_id:%s" % (university_id,
                                                                                            college_id))
        try:
            args = request.json
            args_dict = dict()
            args_dict['college_name'] = args.get('college_name', None)
            args_dict['college_id'] = args.get('college_id', None)
            args_dict['enable'] = args.get('enable', True)
            args_dict['university_id'] = university_id
            args_dict['id'] = college_id
            if not (args_dict['college_name'] and args_dict['college_id']):
                InvalidRequestException("The argument is not null")
            college = CollegeController()
            college.update_college_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/college, method:PUT, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def delete(self, university_id, college_id):
        LOG.info("Call url:/api/v1/college, method:DELETE, college_id:%s, university_id:%s" % (college_id,
                                                                                               university_id))
        try:
            college = CollegeController()
            college.delete_college_info(college_id=college_id)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/college, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

