# -*- coding: utf-8 -*-
import csv
from wechat.exceptions import DBOperateException
from wechat.models.province_model import ProvinceModel
from wechat.models.university_model import UniversityModel
from wechat.models.college_mode import CollegeModel
from wechat.models.major_model import MajorModel
import traceback
import logging

LOG = logging.getLogger("wechat")


def handle_name(student_name):
    if not isinstance(student_name, unicode):
        student_name = unicode(student_name.decode("utf-8"))
    handled_name = student_name[0]
    for _ in student_name[1:]:
        handled_name += "*"
    return handled_name


def import_data(csv_file):
    try:
        reader = csv.DictReader(open(csv_file, "rU"))
        for row in reader:
            info_dict = dict()
            info_dict['province_name'] = row['province_name'].decode('gbk').encode('utf-8')
            info_dict['university_name'] = row['university_name'].decode('gbk').encode('utf-8')
            info_dict['college_name'] = row['college_name'].decode('gbk').encode('utf-8')
            info_dict['major_id'] = row['major_id'].decode('gbk').encode('utf-8')
            info_dict['major_name'] = row['major_name'].decode('gbk').encode('utf-8')
            info_dict['year'] = row['year'].decode('gbk').encode('utf-8')
            info_dict['enrollment'] = row['enrollment'].decode('gbk').encode('utf-8')
            info_dict['exempt'] = row['exempt'].decode('gbk').encode('utf-8')
            try:
                province_model = ProvinceModel()
                info_dict['province_id'] = province_model.\
                    get_province_id_by_name(province_name=info_dict['province_name'])
                if not info_dict['province_id']:
                    """province_id为空，数据库没有province数据"""
                    info_dict['province_id'] = province_model.add_province_info(**info_dict)
                university_model = UniversityModel()
                info_dict['university_id'] = university_model.\
                    get_university_id_by_name(university_name=info_dict['university_name'])
                if not info_dict['university_id']:
                    info_dict['university_id'] = "000000"
                    info_dict['university_id'] = university_model.add_university_info(**info_dict)
                college_model = CollegeModel()
                info_dict['college_id'] = college_model.get_college_id_by_name(college_name=info_dict['college_name'])
                if not info_dict['college_id']:
                    info_dict['college_id'] = "000000"
                    info_dict['college_id'] = college_model.add_college_info(**info_dict)

            except DBOperateException:
                continue
    except Exception as e:
        LOG.error("Import csv data to database error:%s" % traceback.format_exc())