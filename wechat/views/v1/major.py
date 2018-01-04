# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import traceback
from wechat.controllers.major import MajorController
from flask import request
from wechat.exceptions import InvalidRequestException
LOG = logging.getLogger("wechat")


class MajorPost(Resource):
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
        args_dict['major_id'] = args.get('major_id', None)
        args_dict['college_id'] = args.get('college_id', None)
        args_dict['major_name'] = args.get('major_name', None)
        args_dict['year'] = args.get('year', None)
        args_dict['enrollment'] = args.get('enrollment', None)
        args_dict['exempt'] = args.get('exempt', None)
        LOG.info("Call url:/api/v1/major, method:POST, major_id:%s, college_id:%s, major_name:%s, "
                 "year:%s, enrollment:%s, exempt:%s" % (args_dict['major_id'],
                                                        args_dict['college_id'],
                                                        args_dict['major_name'],
                                                        args_dict['year'],
                                                        args_dict['enrollment'],
                                                        args_dict['exempt']))
        try:
            if not (args_dict['major_id'] and args_dict['college_id'] and args_dict['major_name'] and
                    args_dict['year'] and args_dict['enrollment'] and args_dict['exempt']):
                InvalidRequestException("The argument is not null")
            major = MajorController()
            major.add_major_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/college, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class MajorGet(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self, college_id):
        LOG.info("Call url:/api/v1/major, method:GET, college_id:%s" % college_id)
        try:
            major = MajorController()
            ret_dict = major.get_major_info_by_college_id(college_id=college_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/major, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class MajorPutDelete(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def put(self, college_id, major_id):
        LOG.info("Call url:/api/v1/major, method:PUT, college_id:%s, major_id:%s" % (college_id,
                                                                                     major_id))
        try:
            args = request.json
            args_dict = dict()
            args_dict['major_id'] = args.get('major_id', None)
            args_dict['college_id'] = args.get('college_id', None)
            args_dict['major_name'] = args.get('major_name', None)
            args_dict['year'] = args.get('year', None)
            args_dict['enrollment'] = args.get('enrollment', None)
            args_dict['enable'] = args.get('enable', True)
            args_dict['exempt'] = args.get('exempt', None)
            args_dict['id'] = major_id
            if not (args_dict['major_id'] and args_dict['college_id'] and args_dict['major_name'] and
                    args_dict['year'] and args_dict['enrollment'] and args_dict['exempt'] and args_dict['enable']):
                InvalidRequestException("The argument is not null")
            major = MajorController()
            major.update_major_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/major, method:PUT, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def delete(self, college_id, major_id):
        LOG.info("Call url:/api/v1/major, method:DELETE, college_id:%s, major_id:%s" % (college_id,
                                                                                        major_id))
        try:
            major = MajorController()
            major.delete_major_info(major_id=major_id)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/major, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

