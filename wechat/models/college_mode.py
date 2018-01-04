# -*- coding: utf-8 -*-
from wechat.models.models_base import Colleges
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
import traceback
import logging

LOG = logging.getLogger("wechat")


class CollegeModel(object):
    @staticmethod
    def get_college_info_by_id(college_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if college_id:
                college_info = session.query(Colleges).filter(Colleges.id == college_id).one()
            else:
                college_info = session.query(Colleges).all()

            college_info_list = list()
            for college in college_info:
                college_dict = dict()
                college_dict['id'] = college.id
                college_dict['college_id'] = college.college_id
                college_dict['college_name'] = college.college_name
                college_dict['university_id'] = college.university_id
                college_dict['enable'] = college.enable
                college_info_list.append(college_dict)
            return college_info_list
        except Exception:
            LOG.info("Call get_college_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get college info error")

    @staticmethod
    def get_college_info_by_university_id(university_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if university_id:
                college_info = session.query(Colleges).filter(Colleges.university_id == university_id).all()
            else:
                college_info = session.query(Colleges).all()
            college_info_list = list()
            for college in college_info:
                college_dict = dict()
                college_dict['id'] = college.id
                college_dict['college_id'] = college.college_id
                college_dict['college_name'] = college.college_name
                college_dict['university_id'] = college.university_id
                college_dict['enable'] = college.enable
                college_info_list.append(college_dict)
            return college_info_list
        except Exception:
            LOG.info("Call get_college_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get college info error")

    @staticmethod
    def add_college_info(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            college_count = session.query(Colleges).filter(Colleges.college_id == kwargs["college_id"]).count()
            if college_count != 0:
                raise DBOperateException("Duplicated information input, please check")
            college_obj = Colleges(college_id=kwargs["college_id"],
                                   university_id=kwargs["university_id"],
                                   college_name=kwargs["college_name"],
                                   enable=True)
            session.add(college_obj)
            session.commit()
        except DBOperateException:
            raise
        except Exception:
            LOG.info("Call add_college_info error:%s" % traceback.format_exc())
            raise DBOperateException("Add college info error")

    @staticmethod
    def delete_college_by_id(college_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            session.query(Colleges).filter(Colleges.id == college_id).delete()
            session.commit()
        except Exception:
            LOG.info("Call delete_college_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Delete college info error")

    @staticmethod
    def update_college_by_id(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            college_info = session.query(Colleges).filter(Colleges.id == kwargs['id']).one()
            college_info.college_id = kwargs['college_id']
            college_info.university_id = kwargs['university_id']
            college_info.college_name = kwargs['college_name']
            college_info.enable = kwargs['enable']
            session.commit()
        except Exception:
            LOG.info("Call update_college_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update college info error")