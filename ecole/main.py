#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

import daos
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher

from daos.address_dao import AddressDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
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

    print("""
    --------------------------
    Tests des DAO de l'école
    --------------------------
    """)

    test_course_dao()
    test_address_dao()
    test_student_dao()
    test_teacher_dao()


def test_course_dao() -> None:
    print("\n===== TEST COURSE DAO =====")

    dao = CourseDao()

    # CREATE
    course = Course(
        "Informatique",
        date(2026, 9, 7),
        date(2026, 10, 7)
    )

    course.id = dao.create(course)
    print("CREATE :", course.id)

    # READ
    course_read = dao.read(course.id)
    print("READ :", course_read)

    # UPDATE
    course.name = "Python avancé"
    update_success = dao.update(course)
    print("UPDATE :", update_success)

    # READ après modification
    course_read = dao.read(course.id)
    print("READ après UPDATE :", course_read)

    # DELETE
    delete_success = dao.delete(course.id)
    print("DELETE :", delete_success)

    # READ après suppression
    course_read = dao.read(course.id)
    print("READ après DELETE :", course_read)


def test_address_dao() -> None:
    print("\n===== TEST ADDRESS DAO =====")

    dao = AddressDao()

    # CREATE
    address = Address(
        "10 rue des Tests",
        "Toulouse",
        "31000"
    )

    address.id = dao.create(address)
    print("CREATE :", address.id)

    # READ
    address_read = dao.read(address.id)
    print("READ :", address_read)

    # UPDATE
    address.street = "20 avenue de Python"
    address.city = "Blagnac"
    address.postal_code = "31700"

    update_success = dao.update(address)
    print("UPDATE :", update_success)

    # READ après modification
    address_read = dao.read(address.id)
    print("READ après UPDATE :", address_read)

    # DELETE
    delete_success = dao.delete(address.id)
    print("DELETE :", delete_success)

    # READ après suppression
    address_read = dao.read(address.id)
    print("READ après DELETE :", address_read)


def test_student_dao() -> None:
    print("\n===== TEST STUDENT DAO =====")

    dao = StudentDao()

    # CREATE
    student = Student(
        "Etudiant",
        "Test",
        20
    )

    student.id = dao.create(student)
    print("CREATE :", student.id)

    # READ
    student_read = dao.read(student.id)
    print("READ :", student_read)

    # UPDATE
    student.first_name = "Élève"
    student.last_name = "Modifié"
    student.age = 21

    update_success = dao.update(student)
    print("UPDATE :", update_success)

    # READ après modification
    student_read = dao.read(student.id)
    print("READ après UPDATE :", student_read)

    # DELETE
    delete_success = dao.delete(student.id)
    print("DELETE :", delete_success)

    # READ après suppression
    student_read = dao.read(student.id)
    print("READ après DELETE :", student_read)


def test_teacher_dao() -> None:
    print("\n===== TEST TEACHER DAO =====")

    dao = TeacherDao()

    # CREATE
    teacher = Teacher(
        "Professeur",
        "Test",
        35,
        date(2026, 9, 7)
    )

    teacher.id = dao.create(teacher)
    print("CREATE :", teacher.id)

    # READ
    teacher_read = dao.read(teacher.id)
    print("READ :", teacher_read)

    # UPDATE
    teacher.first_name = "Enseignant"
    teacher.last_name = "Modifié"
    teacher.age = 36
    teacher.hiring_date = date(2026, 9, 8)

    update_success = dao.update(teacher)
    print("UPDATE :", update_success)

    # READ après modification
    teacher_read = dao.read(teacher.id)
    print("READ après UPDATE :", teacher_read)

    # DELETE
    delete_success = dao.delete(teacher.id)
    print("DELETE :", delete_success)

    # READ après suppression
    teacher_read = dao.read(teacher.id)
    print("READ après DELETE :", teacher_read)



if __name__ == '__main__':
    main()
