from models.address import Address
from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address : AddressDao) -> int:
        try:
            with Dao.connection.cursor() as cursor:
                sql = "INSERT INTO address (street, city, postal_code) VALUES (%s, %s, %s)"
                cursor.execute(
                    sql,
                    (address.street, address.city, address.postal_code))
                Dao.connection.commit()

                return cursor.lastrowid
        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur dans la création du cours : {error}")
            return 0

    def read(self, int: id) -> Optional[Address]:
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address = %s"
            cursor.execute(sql, (id))
            record = cursor.fetchone()
            if record is not None:
                address = Address(record['street'], record['city'], record['postal_code'])
                address.id = record['id_address']
            else:
                address = None

        return address

    def update(self, address: AddressDao) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE address SET street = %s, city = %s, postal_code = %s WHERE id_address = %s"
                cursor.execute(sql, (address.street, address.city, address.postal_code))
                Dao.connection.commit()
                return True

        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur pendant la modification de l'address : {error}")
            return False

    def delete(self, address: AddressDao) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM address WHERE id_address = %s"
                cursor.execute(sql, (address.id))
                Dao.connection.commit()
                return True
        except Exception as error:
            Dao.connection.rollback()
            print(f"Erreur pendant la supression de l'address : {error}")
            return False





