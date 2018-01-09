# -*- coding: utf-8 -*-
from wechat.models.student_model import StudentModel


class StudentController(object):
    @staticmethod
    def get_student_info(student_id):
        try:
            student = StudentModel()
            return student.get_student_info_by_id(student_id=student_id)
        except Exception:
            raise

    @staticmethod
    def get_student_info_by_student_id(student_id):
        try:
            student = StudentModel()
            return student.get_student_info_by_student_id(student_id=student_id)
        except Exception:
            raise

    @staticmethod
    def get_student_info_by_major_id(major_id, student_id):
        try:
            student = StudentModel()
            return student.get_student_info_by_major_id(major_id=major_id, student_id=student_id)
        except Exception:
            raise

    @staticmethod
    def add_student_info(**kwargs):
        try:
            student = StudentModel()
            student.add_student_info(**kwargs)
        except Exception:
            raise

    @staticmethod
    def delete_student_info(student_id):
        try:
            student = StudentModel()
            student.delete_student_by_id(student_id=student_id)
        except Exception:
            raise

    @staticmethod
    def update_student_info(**kwargs):
        try:
            student = StudentModel()
            student.update_student_by_id(**kwargs)
        except Exception:
            raise