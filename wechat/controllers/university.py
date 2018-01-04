# -*- coding: utf-8 -*-
from wechat.models.university_model import UniversityModel


class UniversityController(object):
    @staticmethod
    def get_university_info(province_id):
        try:
            university = UniversityModel()
            return university.get_university_info_by_province_id(province_id=province_id)
        except Exception:
            raise

    @staticmethod
    def add_university_info(**kwargs):
        try:
            university = UniversityModel()
            university.add_university_info(**kwargs)
        except Exception:
            raise

    @staticmethod
    def delete_university_info(university_id):
        try:
            university = UniversityModel()
            university.delete_university_by_id(university_id=university_id)
        except Exception:
            raise

    @staticmethod
    def update_university_info(**kwargs):
        try:
            university = UniversityModel()
            university.update_university_by_id(**kwargs)
        except Exception:
            raise