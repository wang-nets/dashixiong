# -*- coding: utf-8 -*-
from wechat.models.models_base import Students
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm.exc import NoResultFound
from wechat.models.province_model import ProvinceModel
from wechat.models.university_model import UniversityModel
from wechat.models.college_mode import CollegeModel
from wechat.models.major_model import MajorModel
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
                student_info = session.query(Students).filter(Students.id == student_id).all()
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
            LOG.error("Call get_student_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get student info error")

    @staticmethod
    def get_student_info_by_student_id(student_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            student_dict = dict()
            student_info = session.query(Students).filter(Students.student_id == student_id).one()
            major_id = student_info.major_id
            student_dict['is_upload'] = True
            student_dict['major_id'] = major_id
            return student_dict
        except NoResultFound:
            student_dict['is_upload'] = False
            student_dict['major_id'] = 0
            return student_dict
        except Exception:
            LOG.error("Call get_student_info_by_id error:%s" % traceback.format_exc())
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

                major = MajorModel()
                student_info_dict['major_info'] = major.get_major_info_by_id(major_id=major_id)[0]
                college = CollegeModel()
                student_info_dict['college_info'] = college.\
                    get_college_info_by_id(college_id=student_info_dict['major_info']['college_id'])[0]
                university = UniversityModel()
                student_info_dict['university_info'] = university.\
                    get_university_info_by_id(university_id=student_info_dict['college_info']['university_id'])[0]
                province = ProvinceModel()
                student_info_dict['province_info'] = province.\
                    get_province_info_by_id(province_id=student_info_dict['university_info']['province_id'])[0]
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
            LOG.error("Call get_student_info_by_id error:%s" % traceback.format_exc())
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
            return student_obj.id
        except DBOperateException:
            raise
        except Exception:
            LOG.error("Call add_student_info error:%s" % traceback.format_exc())
            raise DBOperateException("Add student info error")

    @staticmethod
    def delete_student_by_id(student_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            session.query(Students).filter(Students.student_id == student_id).delete()
            session.commit()
        except Exception:
            LOG.error("Call delete_student_by_id error:%s" % traceback.format_exc())
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
            LOG.error("Call update_student_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update student info error")