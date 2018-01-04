# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, VARCHAR, Float, Boolean, DateTime
from sqlalchemy.schema import ForeignKey
from wechat.models import MODEL_BASE
from sqlalchemy.orm import relationship


class Provinces(MODEL_BASE):
    """
    省份表
    """
    __tablename__ = "provinces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    province_name = Column(VARCHAR(64), index=True, nullable=False, unique=True)
    enable = Column(Boolean, nullable=False)
    university = relationship("Universities")


class Universities(MODEL_BASE):
    """
    大学表
    """
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    university_id = Column(VARCHAR(64), index=True, nullable=False, unique=True)
    university_name = Column(VARCHAR(128), index=True, nullable=False, unique=True)
    enable = Column(Boolean, nullable=False)
    major = relationship("Colleges")


class Colleges(MODEL_BASE):
    """
    学院表
    """
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    college_id = Column(VARCHAR(64), index=True, nullable=False)
    college_name = Column(VARCHAR(128), index=True, nullable=False)
    enable = Column(Boolean, nullable=False)
    major = relationship("Majors")


class Majors(MODEL_BASE):
    """
    专业表
    major_name：专业名称
    college_id：学院id
    major_id：专业id
    year：年份
    enrollment：录取人数
    exempt：免推人数
    """
    __tablename__ = "majors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    major_name = Column(VARCHAR(128), index=True, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    major_id = Column(VARCHAR(64), index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    enrollment = Column(Integer, nullable=False)
    exempt = Column(Integer, nullable=False)
    enable = Column(Boolean, nullable=False)
    student = relationship("Students")


class Students(MODEL_BASE):
    """
    学生成绩表
    student_id：学生id
    name：姓名
    year：报考专业
    subject_1：专业一成绩
    subject_2：专业二成绩
    subject_3：专业三成绩
    subject_4：专业四成绩
    total：总分
    have_picture：是否有照片
    """
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(VARCHAR(128), index=True, nullable=False, unique=True)
    name = Column(VARCHAR(64), index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    major_id = Column(Integer, ForeignKey("majors.id"))
    subject_1 = Column(Float, index=True, nullable=False)
    subject_2 = Column(Float, index=True, nullable=False)
    subject_3 = Column(Float, index=True, nullable=False)
    subject_4 = Column(Float, index=True, nullable=False)
    total = Column(Float, nullable=False)
    create_time = Column(DateTime, nullable=False)
    create_user = Column(VARCHAR(128), nullable=False)
    have_picture = Column(Boolean, nullable=False)