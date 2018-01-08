# -*- coding: utf-8 -*-
from wechat.models.models_base import Students
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
from sqlalchemy import and_, or_, desc
from wechat import app
from wechat.commons.utils import handle_name
import datetime
import traceback
import logging

LOG = logging.getLogger("wechat")


class StudentModel(object):
    @staticmethod
    def get_student_info_by_id(student_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if student_id:
                student_info = session.query(Students).filter(Students.id == student_id).one()
            else:
                student_info = session.query(Students).all()
            student_info_list = list()
            for student in student_info:
                student_dict = dict()
                student_dict['id'] = student.id
                student_dict['major_id'] = student.major_id
                student_dict['student_id'] = student.student_id
                student_dict['name'] = student.name
                student_dict['year'] = student.year
                student_dict['subject_1'] = student.subject_1
                student_dict['subject_2'] = student.subject_2
                student_dict['subject_3'] = student.subject_3
                student_dict['subject_4'] = student.subject_4
                student_dict['total'] = student.total
                student_dict['create_time'] = student.create_time
                student_dict['create_user'] = student.create_user
                student_dict['have_picture'] = student.have_picture
                student_info_list.append(student_dict)
            return student_info_list
        except Exception:
            LOG.info("Call get_student_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get student info error")

    @staticmethod
    def get_student_info_by_major_id(major_id=None, student_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            student_info_dict = dict()
            if major_id:
                student_info = session.query(Students).filter(Students.major_id == major_id).\
                    order_by(desc(Students.total)).all()
                student_info_dict['count'] = session.query(Students).filter(Students.major_id == major_id).\
                    count()

            else:
                student_info = session.query(Students).order_by(desc(Students.total)).all()
            student_info_list = list()
            seq = 1
            for student in student_info:
                student_dict = dict()
                student_dict['seq'] = seq
                student_dict['id'] = student.id
                student_dict['major_id'] = student.major_id
                student_dict['student_id'] = student.student_id
                if student_dict['student_id'] == student_id:
                    student_info_dict['seq'] = seq
                student_dict['name'] = handle_name(student.name)
                student_dict['year'] = student.year
                student_dict['subject_1'] = student.subject_1
                student_dict['subject_2'] = student.subject_2
                student_dict['subject_3'] = student.subject_3
                student_dict['subject_4'] = student.subject_4
                student_dict['total'] = student.total
                student_dict['create_time'] = student.create_time.strftime('%Y-%m-%d %H:%M:%S')
                student_dict['create_user'] = student.create_user
                student_dict['have_picture'] = student.have_picture
                student_dict['pic_url'] = "%s/%s.jpg" % (app.config.get("IMAGE_URL"), student_dict['student_id'])
                seq += 1
                student_info_list.append(student_dict)
            student_info_dict['student_info'] = student_info_list
            return student_info_dict
        except Exception:
            LOG.info("Call get_student_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get student info error")

    @staticmethod
    def add_student_info(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            student_count = session.query(Students).filter(Students.student_id == kwargs["student_id"]).count()
            if student_count != 0:
                raise DBOperateException("Duplicated information input, please check")
            student_obj = Students(student_id=kwargs["student_id"],
                                   name=kwargs["name"],
                                   year=kwargs["year"],
                                   major_id=kwargs["major_id"],
                                   subject_1=kwargs["subject_1"],
                                   subject_2=kwargs["subject_2"],
                                   subject_3=kwargs["subject_3"],
                                   subject_4=kwargs["subject_4"],
                                   total=kwargs["total"],
                                   create_time=datetime.datetime.now(),
                                   create_user=kwargs["name"],
                                   have_picture=True)
            session.add(student_obj)
            session.commit()
        except DBOperateException:
            raise
        except Exception:
            LOG.info("Call add_student_info error:%s" % traceback.format_exc())
            raise DBOperateException("Add student info error")

    @staticmethod
    def delete_student_by_id(student_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            session.query(Students).filter(Students.student_id == student_id).delete()
            session.commit()
        except Exception:
            LOG.info("Call delete_student_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Delete student info error")

    @staticmethod
    def update_student_by_id(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            student_info = session.query(Students).filter(Students.student_id == kwargs['student_id']).one()
            student_info.name = kwargs['name']
            student_info.year = kwargs['year']
            student_info.major_id = kwargs['major_id']
            student_info.subject_1 = kwargs['subject_1']
            student_info.subject_2 = kwargs['subject_2']
            student_info.subject_3 = kwargs['subject_3']
            student_info.subject_4 = kwargs['subject_4']
            student_info.total = kwargs['total']
            student_info.create_time = kwargs['create_time']
            student_info.create_user = kwargs['create_user']
            student_info.have_picture = kwargs['have_picture']
            session.commit()
        except Exception:
            LOG.info("Call update_student_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update student info error")