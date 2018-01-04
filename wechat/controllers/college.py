# -*- coding: utf-8 -*-
from wechat.models.college_mode import CollegeModel


class CollegeController(object):
    @staticmethod
    def get_college_info_by_university_id(university_id):
        try:
            college = CollegeModel()
            return college.get_college_info_by_university_id(university_id=university_id)
        except Exception:
            raise

    @staticmethod
    def get_college_info(college_id):
        try:
            college = CollegeModel()
            return college.get_college_info_by_id(college_id=college_id)
        except Exception:
            raise

    @staticmethod
    def add_college_info(**kwargs):
        try:
            college = CollegeModel()
            college.add_college_info(**kwargs)
        except Exception:
            raise

    @staticmethod
    def delete_college_info(college_id):
        try:
            college = CollegeModel()
            college.delete_college_by_id(college_id=college_id)
        except Exception:
            raise

    @staticmethod
    def update_college_info(**kwargs):
        try:
            college = CollegeModel()
            college.update_college_by_id(**kwargs)
        except Exception:
            raise