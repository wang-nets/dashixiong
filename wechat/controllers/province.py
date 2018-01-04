# -*- coding: utf-8 -*-
from wechat.models.province_model import ProvinceModel


class ProvinceController(object):
    @staticmethod
    def get_province_info(province_id):
        try:
            province = ProvinceModel()
            return province.get_province_info_by_id(province_id=province_id)
        except Exception:
            raise

    @staticmethod
    def add_province_info(**kwargs):
        try:
            province = ProvinceModel()
            province.add_province_info(**kwargs)
        except Exception:
            raise

    @staticmethod
    def delete_province_info(province_id):
        try:
            province = ProvinceModel()
            province.delete_province_by_id(province_id=province_id)
        except Exception:
            raise

    @staticmethod
    def update_province_info(**kwargs):
        try:
            province = ProvinceModel()
            province.update_province_by_id(**kwargs)
        except Exception:
            raise