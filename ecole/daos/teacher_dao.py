from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class StudentDao(Dao[Teacher]):
    def read(self, id_teacher: int) -> Optional[Teacher]:
        student: Optional[Teacher]
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher WHERE id_student=%s"
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()

        if record is not None:
            teacher = Teacher(
                record["first_name"],
                record["last_name"],
                record["age"]
            )
            student.id = record["id_teacher"]
        else:
            teacher = None
        return teacher