# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
from daos import student_dao
from daos.teacher_dao import TeacherDao
from models import course
from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

from models.student import Student


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try :
            if course.teacher is None:
                print("Erreur : le cours doit avoir un enseignant")
                return 0

            if course.teacher.id is None:
                print("Erreur : l'enseignant doit déjà exister en BD")
                return 0

            with Dao.connection.cursor() as cursor:
                sql = " INSERT INTO course (name, start_date, end_date, id_teacher) VALUES (%s, %s, %s, %s)"

                cursor.execute(
                    sql,
                    (
                        course.name,
                        course.start_date,
                        course.end_date,
                        course.teacher.id
                    )
                )

                Dao.connection.commit()


                return cursor.lastrowid
        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur dans la création du cours : {error}")
            return 0

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
            teacher_dao = TeacherDao()
            course.teacher = teacher_dao.read(record["id_teacher"])
        else:
            course = None

        return course

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = " UPDATE course SET name=%s, start_date=%s, end_date=%s WHERE id_course=%s"
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id))
                Dao.connection.commit()
                return True
        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur pendant la modification du cours : {error}")
            return False


        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = " DELETE FROM course WHERE id_course=%s"
                cursor.execute(sql, (course.id))
                id_max = cursor.lastrowid
                sql_increment = "ALTER TABLE course AUTO_INCREMENT = %s;"
                cursor.execute(sql_increment, (id_max,))
                Dao.connection.commit()
                return True
        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur pendant la supression du cours : {error}")
            return False

    def show_courses(self):
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course ORDER BY id_course"
            cursor.execute(sql)
            records = cursor.fetchall()
            course_dao = CourseDao()
            for record in records:
                course = course_dao.read(record["id_course"])

                if course is not None:
                    print(course)

    def show_student(self, id_course: int):
        with Dao.connection.cursor() as cursor:
            sql = "SELECT student_nbr FROM takes WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            records = cursor.fetchall()
            # Import local pour éviter l'import circulaire
            from daos.student_dao import StudentDao

            student_dao = StudentDao()
            if len(records) == 0:
                print("Aucun étudiant ne suit ce cours.")
                return

            for record in records:
                student_nbr = record["student_nbr"]
                student = student_dao.read(student_nbr)

                if student is not None:
                    print(student)
                else:
                    print(f"Étudiant n° {student_nbr} introuvable")

