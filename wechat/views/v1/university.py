# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import traceback
from wechat.controllers.university import UniversityController
from flask import request
from wechat.exceptions import InvalidRequestException
LOG = logging.getLogger("wechat")


class UniversityPost(Resource):
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
        args_dict['province_id'] = args.get('province_id', None)
        args_dict['university_id'] = args.get('university_id', None)
        args_dict['university_name'] = args.get('university_name', None)
        args_dict['enable'] = args.get('enable', True)
        LOG.info("Call url:/api/v1/university, method:POST, args:%s" % args_dict)
        try:
            if not (args_dict['province_id'] and args_dict['university_id'] and
                    args_dict['university_name']):
                InvalidRequestException("The argument is not null")
            university = UniversityController()
            university.add_university_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/university, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class UniversityGet(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self, province_id):
        LOG.info("Call url:/api/v1/university, method:GET, province_id:%s" % province_id)
        try:
            university = UniversityController()
            ret_dict = university.get_university_info(province_id=province_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/university, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class UniversityPutDelete(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def put(self, province_id, university_id):
        args = request.json
        args_dict = dict()
        args_dict['province_id'] = province_id
        args_dict['id'] = university_id
        args_dict['university_id'] = args.get('university_id', None)
        args_dict['university_name'] = args.get('university_name', None)
        args_dict['enable'] = args.get('enable', True)
        LOG.info("Call url:/api/v1/university, method:PUT, args:%s" % args_dict)
        try:
            if not (args_dict['university_name'] and args_dict['university_id']):
                InvalidRequestException("The argument is not null")
            university = UniversityController()
            university.update_university_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/university, method:PUT, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def delete(self, province_id, university_id):
        LOG.info("Call url:/api/v1/province, method:DELETE, province_id:%s" % province_id)
        try:
            university = UniversityController()
            university.delete_university_info(university_id=university_id)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class PutPicExample(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def post(self):
        import base64
        from io import BytesIO
        from PIL import Image
        try:
            print dir(request)
            print request.files
            # print request.data
            files = request.files
            args = request.args
            args_dict = dict()
            args_dict['picture'] = files.get('file', None)
            args_dict['md5'] = args.get('md5', None)
            print args_dict['md5']
            print args_dict['picture'].stream
            # args_dict['picture'] = base64.b64decode(args_dict['picture'])
            image = Image.open(args_dict['picture'].stream)
            image.save('./new-example.jpg')

        except Exception:
            print traceback.format_exc()