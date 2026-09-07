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
            cursor.execute(sql, (id_student,))
            record = cursor.fetchone()

        if record is not None:
            student = Student(
                record["first_name"],
                record["last_name"],
                record["age"]
            )
            student.id = record["student_nbr"]
        else:
            student = None
        return student

    def create(self, student: Student) -> int:
        try:
            with Dao.connection.cursor() as cursor:
                sql = " INSERT INTO student (first_name, last_name, age) VALUES (%s, %s, %s)"

                cursor.execute(
                    sql,
                    (
                        student.first_name,
                        student.last_name,
                        student.age
                    )
                )

                Dao.connection.commit()


                return cursor.lastrowid

        except Exception as error:
            print(f"Erreur dans la création du cours : {error}")
            return 0

    def update(self, student: Student) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = " UPDATE student SET first_name = %s, last_name = %s, age = %s "
                cursor.execute(sql, (student.first_name, student.last_name, student.age))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Erreur lors de la modification de l'étudiant : {error}")
            return False

    def delete(self, id_student: int) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = " DELETE FROM student WHERE id_student = %s "
                cursor.execute(sql, (id_student,))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Ereur lors de la suppression du cours : {error}")
            return False

