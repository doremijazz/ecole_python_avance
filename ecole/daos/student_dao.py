
from models import course
from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class StudentDao(Dao[Student]):
    def read(self, id_student: int) -> Optional[Student]:
        student: Optional[Student]
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT
                    student.student_nbr,
                    person.first_name,
                    person.last_name,
                    person.age
                FROM student
                INNER JOIN person
                    ON student.id_person = person.id_person
                WHERE student.student_nbr = %s
            """
            cursor.execute(sql, (id_student))
            record = cursor.fetchone()

        if record is not None:
            student = Student(
                record["first_name"],
                record["last_name"],
                record["age"]
            )
            student.student_nbr = record["student_nbr"]
        else:
            student = None
        return student

    def create(self, student: Student) -> int:
        try:
            with Dao.connection.cursor() as cursor:

                # 1. Création de la personne
                sql_person = """
                                INSERT INTO person (first_name, last_name, age)
                                VALUES (%s, %s, %s)
                            """

                cursor.execute(
                    sql_person,
                    (
                        student.first_name,
                        student.last_name,
                        student.age
                    )
                )

                id_person = cursor.lastrowid

                # 2. Création dans student
                sql_student = """
                    INSERT INTO student (student_nbr, id_person)
                    VALUES (%s, %s)
                """

                cursor.execute(sql_student, (student.student_nbr, id_person))

                id_student = cursor.lastrowid

                Dao.connection.commit()

                return student.student_nbr

        except Exception as error:
            print(f"Erreur dans la création de l'étudiant : {error}")
            return 0

    def update(self, student: Student) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                        UPDATE person
                        INNER JOIN student
                        ON person.id_person = student.id_person
                        SET person.first_name = %s,
                        person.last_name = %s,
                        person.age = %s
                        WHERE student_nbr = %s
                    """
                cursor.execute(sql, (student.first_name, student.last_name, student.age, student.student_nbr))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Erreur lors de la modification de l'étudiant : {error}")
            return False

    def delete(self, id_student: int) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql_select = "SELECT id_person FROM student WHERE student_nbr = %s"
                cursor.execute(sql_select, (id_student,))
                record = cursor.fetchone()

                sql_supr = " DELETE FROM takes WHERE student_nbr = %s"
                cursor.execute(sql_supr, (id_student,))

                sql = " DELETE FROM student WHERE student_nbr = %s"
                cursor.execute(sql, (id_student,))

                sql_supr2 = "DELETE FROM person WHERE id_person = %s"
                cursor.execute(sql_supr2, (record["id_person"],))

                id_max = cursor.lastrowid
                sql_increment = "ALTER TABLE person AUTO_INCREMENT = %s;"
                cursor.execute(sql_increment, (id_max,))

                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Ereur lors de la suppression du cours : {error}")
            return False

    def show_courses(self, student: Student) -> None:
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT id_course
                FROM takes
                WHERE student_nbr = %s
                ORDER BY id_course
            """
            print("Numéro recherché :", student.student_nbr)
            cursor.execute(sql, (student.student_nbr,))
            records = cursor.fetchall()
        from daos.course_dao import CourseDao
        course_dao = CourseDao()

        if len(records) == 0:
            print("Cet étudiant ne suit aucun cours.")
            return

        print(
            f"Cours suivis par "
            f"{student.first_name} {student.last_name} :"
        )

        for record in records:
            course = course_dao.read(record["id_course"])

            if course is not None:
                print(course)

    def show_students(self) -> None:
        with Dao.connection.cursor() as cursor:
            sql = """SELECT student_nbr FROM student ORDER BY id_person"""
            cursor.execute(sql)
            records = cursor.fetchall()
            student_dao = StudentDao()
            for record in records:
                student = student_dao.read(record["student_nbr"])

                if student is not None:
                    print(student)