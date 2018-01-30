# -*- coding: utf-8 -*-
from wechat.models.models_base import Provinces, Universities
from wechat.models.university_model import UniversityModel
from wechat.models import DbEngine
from wechat.exceptions import DBOperateException
import traceback
import logging

LOG = logging.getLogger("wechat")


class ProvinceModel(object):
    @staticmethod
    def get_province_info_by_id(province_id=None):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            if province_id:
                province_info = session.query(Provinces).filter(Provinces.id == province_id).all()
            else:
                province_info = session.query(Provinces).all()
            province_info_list = list()
            for province in province_info:
                province_dict = dict()
                province_dict['province_name'] = province.province_name
                province_dict['enable'] = province.enable
                province_dict['id'] = province.id
                province_info_list.append(province_dict)
            LOG.info("Call get_province_info_by_id province_list:%s, province_id:%s" % (province_info_list,
                                                                                        province_id))
            return province_info_list
        except Exception:
            LOG.error("Call get_province_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Get province info error")

    @staticmethod
    def get_province_id_by_name(province_name):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            province_id = session.query(Provinces.id).filter(Provinces.province_name == province_name).scalar()

            LOG.info("Call get_province_id_by_name province_id:%s" % province_id    )
            return province_id
        except Exception:
            LOG.error("Call get_province_id_by_name error:%s" % traceback.format_exc())
            raise DBOperateException("Get province info error")

    @staticmethod
    def add_province_info(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            province_count = session.query(Provinces).\
                filter(Provinces.province_name == kwargs['province_name']).count()
            if province_count != 0:
                raise DBOperateException("Duplicated information input, please check")
            province_obj = Provinces(province_name=kwargs["province_name"],
                                     enable=True)
            session.add(province_obj)
            session.commit()
            return province_obj.id
        except DBOperateException:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            LOG.error("Call get_province_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Add province info error")

    @staticmethod
    def delete_province_by_id(province_id):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            """
            删除省份前先删除省份内相关学校
            """
            # university_ids = session.query(Universities.id).filter(Universities.province_id == province_id).all()
            # university_object = UniversityModel()
            # result = True
            # for u_id in university_ids:
            #     del_result = university_object.delete_university_by_id(university_id=u_id)
            #     result = result and del_result
            # if result:
            #     session.query(Provinces).filter(Provinces.id == province_id).delete()
            #     session.commit()
            #     return True
            # else:
            #     return False
            session.query(Provinces).filter(Provinces.id == province_id).delete()
            session.commit()
        except Exception:
            session.rollback()
            LOG.error("Call get_province_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Delete province info error")
            # return False

    @staticmethod
    def update_province_by_id(**kwargs):
        engine = DbEngine.get_instance()
        session = engine.get_session(autocommit=False, expire_on_commit=True)
        try:
            province_info = session.query(Provinces).filter(Provinces.id == kwargs['id']).one()
            province_info.province_name = kwargs['province_name']
            province_info.enable = kwargs['enable']
            session.commit()
        except Exception:
            session.rollback()
            LOG.error("Call get_province_info_by_id error:%s" % traceback.format_exc())
            raise DBOperateException("Update province info error")