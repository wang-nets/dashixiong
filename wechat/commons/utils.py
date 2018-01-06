# -*- coding: utf-8 -*-


def handle_name(student_name):
    if not isinstance(student_name, unicode):
        student_name = unicode(student_name.decode("utf-8"))
    handled_name = student_name[0]
    for _ in student_name[1:]:
        handled_name += "*"
    return handled_name