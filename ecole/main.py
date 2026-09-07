#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
import daos
from daos.teacher_dao import TeacherDao
from daos.student_dao import StudentDao
from business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(2))
    print(school.get_course_by_id(9))

    teacher_dao = TeacherDao()
    teacher = teacher_dao.read(1)

    print(teacher)

    student_dao = StudentDao()
    student = student_dao.read(1)
    print(student)


if __name__ == '__main__':
    main()
