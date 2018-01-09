# -*- coding: utf-8 -*-
from wechat.models.models_base import Majors
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
import traceback
import logging

LOG = logging.getLogger("wechat")


class MajorModel(object):
    @staticmethod
    def get_major_info_by_id(major_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            major_info_list = list()
            if major_id:
                major_info = session.query(Majors).filter(Majors.id == major_id).all()
            else:
                major_info = session.query(Majors).all()
            for major in major_info:
                major_dict = dict()
                major_dict['id'] = major.id
                major_dict['major_name'] = major.major_name
                major_dict['college_id'] = major.college_id
                major_dict['major_id'] = major.major_id
                major_dict['year'] = major.year
                major_dict['enrollment'] = major.enrollment
                major_dict['exempt'] = major.exempt
                major_dict['enable'] = major.enable
            major_info_list.append(major_dict)
            return major_info_list
        except Exception:
            LOG.error("Call get_major_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get major info error")

    @staticmethod
    def get_major_info_by_college_id(college_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if college_id:
                major_info = session.query(Majors).filter(Majors.college_id == college_id).all()
            else:
                major_info = session.query(Majors).all()
            major_info_list = list()
            for major in major_info:
                major_dict = dict()
                major_dict['id'] = major.id
                major_dict['major_name'] = major.major_name
                major_dict['college_id'] = major.college_id
                major_dict['major_id'] = major.major_id
                major_dict['year'] = major.year
                major_dict['enrollment'] = major.enrollment
                major_dict['exempt'] = major.exempt
                major_dict['enable'] = major.enable
                major_info_list.append(major_dict)
            return major_info_list
        except Exception:
            LOG.error("Call get_major_info_by_college_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get major info error")

    @staticmethod
    def add_major_info(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            major_count = session.query(Majors).filter(Majors.major_id == kwargs["major_id"]).count()
            if major_count != 0:
                raise DBOperateException("Duplicated information input, please check")
            major_obj = Majors(major_id=kwargs["major_id"],
                               college_id=kwargs["college_id"],
                               major_name=kwargs["major_name"],
                               year=kwargs['year'],
                               enrollment=kwargs['enrollment'],
                               exempt=kwargs['exempt'],
                               enable=True)
            session.add(major_obj)
            session.commit()
        except DBOperateException:
            raise
        except Exception:
            LOG.error("Call add_major_info error:%s" % traceback.format_exc())
            raise DBOperateException("Add major info error")

    @staticmethod
    def delete_major_by_id(major_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            session.query(Majors).filter(Majors.id == major_id).delete()
            session.commit()
        except Exception:
            LOG.error("Call delete_major_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Delete major info error")

    @staticmethod
    def update_major_by_id(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            major_info = session.query(Majors).filter(Majors.id == kwargs['id']).one()
            major_info.major_id = kwargs['major_id']
            major_info.college_id = kwargs['college_id']
            major_info.major_name = kwargs['major_name']
            major_info.year = kwargs['year']
            major_info.enrollment = kwargs['enrollment']
            major_info.exempt = kwargs['exempt']
            major_info.enable = kwargs['enable']
            session.commit()
        except Exception:
            LOG.error("Call update_major_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update major info error")