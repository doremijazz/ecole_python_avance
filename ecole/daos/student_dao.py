from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class StudentDao(Dao[Student]):
    def read(self, id_student: int) -> Optional[Student]:
        student: Optional[Student]
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM student WHERE id_student=%s"
            cursor.execute(sql, (id_student,))
            record = cursor.fetchone()

        if record is not None:
            student = Student(
                record["first_name"],
                record["last_name"],
                record["age"]
            )
            student.id = record["id_student"]
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

