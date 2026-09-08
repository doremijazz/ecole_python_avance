
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class TeacherDao(Dao[Teacher]):
    def read(self, id_teacher: int) -> Optional[Teacher]:
        teacher: Optional[Teacher]
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT
                    teacher.id_teacher,
                    person.first_name,
                    person.last_name,
                    person.age,
                    teacher.hiring_date
                FROM teacher
                INNER JOIN person
                    ON teacher.id_person = person.id_person
                WHERE teacher.id_teacher = %s
            """
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()

        if record is not None:
            teacher = Teacher(
                record["first_name"],
                record["last_name"],
                record["age"],
                record["hiring_date"]
            )
            teacher.id = record["id_teacher"]
        else:
            teacher = None
        return teacher

    def create(self, teacher: Teacher) -> int:
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
                        teacher.first_name,
                        teacher.last_name,
                        teacher.age
                    )
                )

                id_person = cursor.lastrowid

                sql = " INSERT INTO teacher (id_teacher, hiring_date, id_person) VALUES (%s, %s, %s)"

                cursor.execute(
                    sql,
                    (
                        teacher.id,
                        teacher.hiring_date,
                        id_person
                    )
                )

                Dao.connection.commit()


                return cursor.lastrowid
        except Exception as error:
            print(f"Erreur dans la création de l'enseignant : {error}")
            return 0

    def update(self, teacher: Teacher) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                                UPDATE person
                                INNER JOIN teacher
                                    ON person.id_person = teacher.id_person
                                SET person.first_name = %s,
                                    person.last_name = %s,
                                    person.age = %s,
                                    teacher.hiring_date = %s
                                WHERE teacher.id_teacher = %s
                            """
                cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.hiring_date, teacher.id))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Erreur dans l'update du cours : {error}")
            return False

    def delete(self, id_teacher: int) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql_select = "SELECT id_person FROM teacher WHERE id_teacher = %s"
                cursor.execute(sql_select, (id_teacher,))
                record = cursor.fetchone()
                sql = "DELETE FROM teacher WHERE id_teacher=%s"
                cursor.execute(sql, (id_teacher,))

                id_max = cursor.lastrowid
                sql_increment = "ALTER TABLE teacher AUTO_INCREMENT = %s;"
                cursor.execute(sql_increment, (id_max,))

                sql_supr2 = "DELETE FROM person WHERE id_person = %s"
                cursor.execute(sql_supr2, (record["id_person"],))
                Dao.connection.commit()

                id_max = cursor.lastrowid
                sql_increment = "ALTER TABLE person AUTO_INCREMENT = %s;"
                cursor.execute(sql_increment, (id_max,))
                return True
        except Exception as error:
            print(f"Erreur dans l'update du cours : {error}")
            return False

    def show_courses(self, teacher : Teacher) -> list:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_teacher=%s"
            cursor.execute(sql, (teacher.id,))
            courses = cursor.fetchall()
            from daos.course_dao import CourseDao
            course_dao = CourseDao()
            for course in courses:
                course = course_dao.read(course["id_course"])

                if course is not None:
                    print(course)