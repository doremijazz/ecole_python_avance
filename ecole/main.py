#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

import daos
from models.address import Address
from models.course import Course
from models.person import Person
from models.student import Student
from models.teacher import Teacher

from daos.dao import Dao

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

    print("""
        --------------------------
        TEST FONCTIONALITEES
        --------------------------
        """)
    while(True):
        choix_1 = input("Choisir une fonctionalités :  "
                        "1.Afficher tous les cours, "
                        "2.Afficher tous les éléves")
        if choix_1 == "1":
            test_show_courses()
            choix_2 = input("Voulez vous selectionner un cours o/n")
            if choix_2 == "o":
                while (True):
                    course_id = input("Saisissez le numéro du cours")
                    choix_3 = input("1. Afficher les élves, 2.Modifier,"
                                    " 3.Suprimer, 4.Sortir du menu")
                    if choix_3 == "1":
                        CourseDao().show_student(course_id)
                    elif choix_3 == "4":
                        break
        elif choix_1 == "2":
            StudentDao().show_students()
            choix_4 = input("Voulez vous selectionner un cours o/n")
            if choix_4 == "o":
                while (True):
                    student_id = input("Saisissez le numéro de l'étudiant")
                    print(StudentDao().read(student_id))
                    choix_5 = input("1.Modifier,"
                                    " 2.Suprimer, 3.Sortir du menu")
                    if choix_5 == "1":
                        pass
                    elif choix_5 == "4":
                        break





def initialize_student_counter() -> None:
    with Dao.connection.cursor() as cursor:
        sql = """
            SELECT COALESCE(MAX(student_nbr), 0) AS max_student_nbr
            FROM student
        """

        cursor.execute(sql)
        record = cursor.fetchone()

    Student.students_nb = record["max_student_nbr"]

def initialize_person_counter() -> None:
    with Dao.connection.cursor() as cursor:
        sql = """
            SELECT COALESCE(MAX(id_person), 0) AS max_id_person
            FROM person
        """

        cursor.execute(sql)
        record = cursor.fetchone()

    Person.person_id = record["max_id_person"]

def test_course_dao() -> None:
    print("\n===== TEST COURSE DAO =====")

    dao = CourseDao()

    teacher_dao = TeacherDao()
    teacher = teacher_dao.read(1)

    student_dao = StudentDao()
    student = student_dao.read(1)
    # CREATE
    course = Course(
        "Informatique",
        date(2026, 9, 7),
        date(2026, 10, 7),
    )
    course.teacher = teacher
    course.student = [student]
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
    delete_success = dao.delete(course)
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
    delete_success = dao.delete(address)
    print("DELETE :", delete_success)

    # READ après suppression
    address_read = dao.read(address.id)
    print("READ après DELETE :", address_read)


def test_student_dao() -> None:
    print("\n===== TEST STUDENT DAO =====")
    initialize_student_counter()
    initialize_person_counter()
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
    initialize_person_counter()
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

def test_show_courses() -> None:
    print("\n===== TEST SHOW COURSES =====")

    print("\n### Show Student courses ###")
    student_dao = StudentDao()
    student = student_dao.read(1)

    if student is not None:
        student_dao.show_courses(student)
    else:
        print("Étudiant introuvable")

    print("\n### Show Teacher courses ###")
    teacher_dao = TeacherDao()
    teacher = teacher_dao.read(1)
    if teacher is not None:
        teacher_dao.show_courses(teacher)
    else:
        print("Enseignant introuvable")

    print("\n### Show courses for director ###")
    course_dao = CourseDao()
    course_dao.show_courses()

if __name__ == '__main__':
    main()
