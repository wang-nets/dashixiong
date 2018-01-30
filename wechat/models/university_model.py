# -*- coding: utf-8 -*-
from wechat.models.models_base import Universities, Colleges
from wechat.models.college_mode import CollegeModel
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
import traceback
import logging

LOG = logging.getLogger("wechat")


class UniversityModel(object):
    @staticmethod
    def get_university_info_by_province_id(province_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if province_id:
                university_info = session.query(Universities).filter(Universities.province_id == province_id).all()
            else:
                university_info = session.query(Universities).all()
            university_info_list = list()
            for university in university_info:
                university_dict = dict()
                university_dict['id'] = university.id
                university_dict['university_id'] = university.university_id
                university_dict['province_id'] = university.province_id
                university_dict['university_name'] = university.university_name
                university_dict['enable'] = university.enable
                university_info_list.append(university_dict)
            LOG.info("Call get_university_info_by_province_id university_list:%s " % university_info_list)
            return university_info_list
        except Exception:
            LOG.error("Call get_university_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get university info error")

    @staticmethod
    def get_university_info_by_id(university_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if university_id:
                university_info = session.query(Universities).filter(Universities.id == university_id).all()
            else:
                university_info = session.query(Universities).all()
            university_info_list = list()
            for university in university_info:
                university_dict = dict()
                university_dict['id'] = university.id
                university_dict['university_id'] = university.university_id
                university_dict['province_id'] = university.province_id
                university_dict['university_name'] = university.university_name
                university_dict['enable'] = university.enable
                university_info_list.append(university_dict)
            return university_info_list
        except Exception:
            LOG.error("Call get_university_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get university info error")

    @staticmethod
    def get_university_id_by_name(university_name):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:

            university_id = session.query(Universities.id).\
                filter(Universities.university_name == university_name).scalar()

            return university_id
        except Exception:
            LOG.error("Call get_university_id_by_name error:%s" % traceback.format_exc())
            raise DBOperateException("Get university info error")

    @staticmethod
    def add_university_info(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            university_count = session.query(Universities).\
                filter(Universities.university_name == kwargs["university_name"]).count()
            if university_count != 0:
                raise DBOperateException("Duplicated information input, please check")
            university_obj = Universities(province_id=kwargs["province_id"],
                                          university_id=kwargs["university_id"],
                                          university_name=kwargs["university_name"],
                                          enable=True)
            session.add(university_obj)
            session.commit()
            return university_obj.id
        except DBOperateException:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            LOG.error("Call add_university_info error:%s" % traceback.format_exc())
            raise DBOperateException("Add university info error")

    @staticmethod
    def delete_university_by_id(university_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            """
            删除学校之前先删除学校内所有学院
            """
            # college_ids = session.query(Colleges.id).filter(Colleges.university_id == university_id).all()
            # college_object = CollegeModel()
            # result = True
            # for c_id in college_ids:
            #     del_result = college_object.delete_college_by_id(college_id=c_id)
            #     if not del_result:
            #         LOG.info("Call delete_university_by_id, execute del college failed! college_id:%s" % c_id)
            #     result = result and del_result
            # if result:
            #     session.query(Universities).filter(Universities.id == university_id).delete()
            #     session.commit()
            #     return True
            # else:
            #     LOG.info("Call delete_university_by_id, execute del college failed!")
            #     return False
            session.query(Universities).filter(Universities.id == university_id).delete()
            session.commit()
        except Exception:
            session.rollback()
            LOG.error("Call delete_university_by_id error:%s" % traceback.format_exc())
            # raise DBOperateException("Delete university info error")
            # return False

    @staticmethod
    def update_university_by_id(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            university_info = session.query(Universities).filter(Universities.id == kwargs['id']).one()
            university_info.university_id = kwargs['university_id']
            university_info.university_name = kwargs['university_name']
            university_info.enable = kwargs['enable']
            session.commit()
        except Exception:
            session.rollback()
            LOG.error("Call update_university_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update university info error")