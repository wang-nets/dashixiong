# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import traceback
from wechat.controllers.province import ProvinceController
LOG = logging.getLogger("wechat")


class ProvinceApi(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self):
        self.req_parse.add_argument('province_id', type=str, default=None, location='args')

        args = self.req_parse.parse_args()
        province_id = args.pop('province_id', None)
        LOG.info("Call url:/api/v1/province, method:GET, province_id:%s" % province_id)
        try:
            province = ProvinceController()
            ret_dict = province.get_province_info(province_id=province_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return 200, self.ret_dict
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return 500, self.ret_dict

    def post(self):
        self.req_parse.add_argument('province_name', type=str, default=None, location='args')
        self.req_parse.add_argument('enable', type=str, default=True, location='args')
        args = self.req_parse.parse_args()
        args_dict = dict()
        args_dict['province_name'] = args.pop('province_name', None)
        args_dict['enable'] = args.pop('enable', True)
        LOG.info("Call url:/api/v1/province, method:POST, province_name:%s, enable:%s" %
                 (args_dict['province_name'], args_dict['enable']))
        try:
            province = ProvinceController()
            province.add_province_info(**args_dict)
            self.ret_dict['success'] = "true"
            return 200, self.ret_dict
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return 500, self.ret_dict

    def patch(self):
        self.req_parse.add_argument('province_id', type=str, default=None, location='args')
        self.req_parse.add_argument('province_name', type=str, default=None, location='args')
        self.req_parse.add_argument('enable', type=str, default=None, location='args')
        args = self.req_parse.parse_args()
        args_dict = dict()
        args_dict['id'] = args.pop('province_id', None)
        args_dict['province_name'] = args.pop('province_name', None)
        args_dict['enable'] = args.pop('province_name', True)
        LOG.info("Call url:/api/v1/province, method:PATCH, province_id:%s, province_name:%s, enable:%s" %
                 (args_dict['id'], args_dict['province_name'], args_dict['enable']))
        try:
            province = ProvinceController()
            province.update_province_info(**args_dict)
            self.ret_dict['success'] = "true"
            return 200, self.ret_dict
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:PATCH, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return 500, self.ret_dict

    def delete(self):
        self.req_parse.add_argument('province_id', type=str, default=None, location='args')

        args = self.req_parse.parse_args()
        province_id = args.pop('province_id', None)

        LOG.info("Call url:/api/v1/province, method:DELETE, province_id:%s" % province_id)
        try:
            province = ProvinceController()
            province.delete_province_info(province_id=province_id)
            self.ret_dict['success'] = "true"
            return 200, self.ret_dict
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return 500, self.ret_dict


class UniversityApi(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self):
        self.req_parse.add_argument('province_id', type=str, default=None, location='args')

        args = self.req_parse.parse_args()
        province_id = args.pop('province_id', None)
        try:
            pass
        except Exception as e:
            self.ret_dict['msg'] = e.message
            return 500, self.ret_dict


    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

class MajorAPI(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass


class ProvinceApi(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass


class StudentApi(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass