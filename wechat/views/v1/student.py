# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
import logging
import datetime
import traceback
from wechat.controllers.student import StudentController
from flask import request
from wechat.exceptions import InvalidRequestException
LOG = logging.getLogger("wechat")


class StudentPost(Resource):
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
        args_dict['student_id'] = args.get('student_id', None)
        args_dict['name'] = args.get('name', None)
        args_dict['year'] = args.get('year', None)
        args_dict['subject_1'] = args.get('subject_1', None)
        args_dict['subject_2'] = args.get('subject_2', None)
        args_dict['subject_3'] = args.get('subject_3', None)
        args_dict['subject_4'] = args.get('subject_4', None)
        args_dict['total'] = args.get('total', None)
        args_dict['picture'] = args.get('picture', True)
        LOG.info("Call url:/api/v1/major, method:POST, major_id:%s, student_id:%s, name:%s, "
                 "year:%s, subject_1:%s, subject_2:%s, subject_3:%s, subject_4:%s, total:%s"
                 "have_picture:%s" % (args_dict['major_id'],
                                      args_dict['student_id'],
                                      args_dict['name'],
                                      args_dict['year'],
                                      args_dict['subject_1'],
                                      args_dict['subject_2'],
                                      args_dict['subject_3'],
                                      args_dict['subject_4'],
                                      args_dict['total'],
                                      args_dict['picture']))

        try:
            if not (args_dict['major_id'] and args_dict['student_id'] and args_dict['name'] and
                    args_dict['year'] and args_dict['subject_1'] and args_dict['subject_2'] and
                    args_dict['subject_3'] and args_dict['subject_4'] and args_dict['total'] and
                    args_dict['picture']):
                InvalidRequestException("The argument is not null")
            student = StudentController()
            student.add_student_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/student, method:POST, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class StudentGet(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def get(self, major_id, student_id):
        LOG.info("Call url:/api/v1/student, method:GET, major_id:%s, student_id:%s" % (major_id, student_id))
        try:
            student = StudentController()
            ret_dict = student.get_student_info_by_major_id(major_id=major_id, student_id=student_id)
            self.ret_dict['data'] = ret_dict
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/student, method:GET, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500


class StudentPutDelete(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.ret_dict = {
            'success': 'false',
            'data': '',
            'msg': ''
        }

    def put(self, major_id, student_id):
        LOG.info("Call url:/api/v1/student, method:PUT, major_id:%s, student_id:%s" % (major_id,
                                                                                       student_id))
        try:
            args = request.json
            args_dict = dict()

            args_dict['student_id'] = student_id
            args_dict['major_id'] = major_id
            args_dict['name'] = args.get('name', None)
            args_dict['year'] = args.get('year', None)
            args_dict['subject_1'] = args.get('subject_1', None)
            args_dict['subject_2'] = args.get('subject_2', None)
            args_dict['subject_3'] = args.get('subject_3', None)
            args_dict['subject_4'] = args.get('subject_4', None)
            args_dict['total'] = args.get('total', None)
            args_dict['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            args_dict['create_user'] = args.get('create_user', "system")
            args_dict['have_picture'] = args.get('have_picture', True)

            if not (args_dict['student_id'] and args_dict['major_id'] and args_dict['name'] and
                    args_dict['year'] and args_dict['subject_1'] and args_dict['subject_1'] and
                    args_dict['subject_1'] and args_dict['subject_2'] and args_dict['subject_3'] and
                    args_dict['subject_4'] and args_dict['total'] and args_dict['create_user']):
                InvalidRequestException("The argument is not null")
            student = StudentController()
            student.update_student_info(**args_dict)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/student, method:PUT, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

    def delete(self, major_id, student_id):
        LOG.info("Call url:/api/v1/student, method:DELETE, major_id:%s, student_id:%s" % (major_id,
                                                                                          student_id))
        try:
            student = StudentController()
            student.delete_student_info(student_id=student_id)
            self.ret_dict['success'] = "true"
            return self.ret_dict, 200
        except Exception as e:
            LOG.error("Call url:/api/v1/student, method:DELETE, error:%s" % traceback.format_exc())
            self.ret_dict['msg'] = e.message
            return self.ret_dict, 500

