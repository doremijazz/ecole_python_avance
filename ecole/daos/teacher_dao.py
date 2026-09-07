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
                sql = " INSERT INTO student (first_name, last_name, age, hiring_date) VALUES (%s, %s, %s)"

                cursor.execute(
                    sql,
                    (
                        teacher.first_name,
                        teacher.last_name,
                        teacher.age,
                        teacher.hiring_date
                    )
                )

                Dao.connection.commit()


                return cursor.lastrowid
        except Exception as error:
            print(f"Erreur dans la création du cours : {error}")
            return 0

    def update(self, teacher: Teacher) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE teacher SET first_name=%s, last_name=%s, age=%s, hiring_date=%s WHERE id_teacher=%s"
                cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.hiring_date, teacher.id))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Erreur dans l'update du cours : {error}")
            return False

    def delete(self, id_teacher: int) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM teacher WHERE id_teacher=%s"
                cursor.execute(sql, (id_teacher,))
                Dao.connection.commit()
                return True
        except Exception as error:
            print(f"Erreur dans l'update du cours : {error}")
            return False

