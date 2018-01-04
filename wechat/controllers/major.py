# -*- coding: utf-8 -*-
from wechat.models.major_model import MajorModel


class MajorController(object):
    @staticmethod
    def get_major_info(major_id):
        try:
            major = MajorModel()
            return major.get_major_info_by_id(major_id=major_id)
        except Exception:
            raise

    @staticmethod
    def get_major_info_by_college_id(college_id):
        try:
            major = MajorModel()
            return major.get_major_info_by_college_id(college_id=college_id)
        except Exception:
            raise

    @staticmethod
    def add_major_info(**kwargs):
        try:
            major = MajorModel()
            major.add_major_info(**kwargs)
        except Exception:
            raise

    @staticmethod
    def delete_major_info(major_id):
        try:
            major = MajorModel()
            major.delete_major_by_id(major_id=major_id)
        except Exception:
            raise

    @staticmethod
    def update_major_info(**kwargs):
        try:
            major = MajorModel()
            major.update_major_by_id(**kwargs)
        except Exception:
            raise