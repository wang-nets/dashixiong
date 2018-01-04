# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import traceback
from wechat.controllers.province import ProvinceController
from flask import request
from wechat.exceptions import InvalidRequestException
LOG = logging.getLogger("wechat")


class ProvincePost(Resource):
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
        args_dict['province_name'] = args.get('province_name', None)
        args_dict['enable'] = args.get('enable', True)
        LOG.info("Call url:/api/v1/province, method:POST, province_name:%s, enable:%s" %
                 (args_dict['province_name'], args_dict['enable']))
        try:
            if not args_dict['province_name']:
                InvalidRequestException("The argument is not null")
            province = ProvinceController()
            province.add_province_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class ProvinceGetPutDelete(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self, province_id):
        LOG.info("Call url:/api/v1/province, method:GET, province_id:%s" % province_id)
        try:
            province = ProvinceController()
            ret_dict = province.get_province_info(province_id=province_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def put(self, province_id):
        LOG.info("Call url:/api/v1/province, method:PUT, province_id:%s" % province_id)
        try:
            args = request.json
            args_dict = dict()
            args_dict['province_name'] = args.get('province_name', None)
            args_dict['enable'] = args.get('enable', True)
            args_dict['id'] = province_id
            if not args_dict['province_name']:
                InvalidRequestException("The argument is not null")
            province = ProvinceController()
            province.update_province_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:PUT, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def delete(self, province_id):
        LOG.info("Call url:/api/v1/province, method:DELETE, province_id:%s" % province_id)
        try:
            province = ProvinceController()
            province.delete_province_info(province_id=province_id)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/province, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

