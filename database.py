from abc import abstractmethod, ABC

import psycopg2
from psycopg2 import Error


class DatabaseController:

    @staticmethod
    def connect() -> psycopg2.connect:
        """Подключение к БД"""
        connection = psycopg2.connect(user="postgres",
                                      password="1111",
                                      host="127.0.0.1",
                                      port="5432",
                                      dbname='curriculum')
        with connection:
            return connection

    def execute(self, request: str) -> None:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(request)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def execute_with_commit(self, request: str) -> None:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(request)
            connection.commit()
            return cursor.rowcount
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def execute_fetchone(self, request: str) -> list:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(request)
            result = cursor.fetchone()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return []
        return result[0]

    def execute_fetchall(self, request: str) -> list:
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(request)
            result = cursor.fetchall()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return []
        return result


class TeachersController(DatabaseController):

    def create(self, fields: dict):
        """предполагая, что пример fields = {"id": 1,
                                            "name": 'Куликов',
                                            "surname": 'Емельян',
                                             "patronymic": 'Евгеньевич'}
        """
        new_id = self.execute_fetchone('SELECT id FROM teachers ORDER BY id DESC LIMIT 1;') + 1
        insert_query = (f"""INSERT INTO teachers (id, surname, name, patronymic) VALUES
        ('{new_id} ', ' {fields["name"]} ', '{fields["surname"]}', '{fields["patronymic"]}');""")
        self.execute_with_commit(insert_query)
        result = self.read_all()
        return result

    def read(self, field: int):
        """Просмотр записи
        :param field: - ID преподавателя
        :return: сведения о предметах этого преподавателя"""
        insert_query = (f"""SELECT si.name, si.classes_type, si.planned_workload, si.actual_workload
                            FROM subject_info si
                            JOIN subjects ON si.id = subjects.subject_id
                            JOIN teachers ON subjects.teacher_id = teachers.id
                            WHERE teachers.id = '{field}'; """
                        )

        result = self.execute_fetchall(insert_query)
        return result

    def read_all(self):
        request = (f'SELECT * FROM teachers;')
        result = self.execute_fetchall(request)
        return result

    def update(self, fields: dict):
        """Изменения данных о преподавателе
        :param fields: - словарь с изменениями
        :return: новые сведения о преподавателе"""
        insert_query = (f"""UPDATE teachers
                            SET surname = '{fields["surname"]}',
                            name = '{fields["name"]}',
                            patronymic = '{fields["patronymic"]}'
                            WHERE id = {fields["id"]}; """
                        )
        self.execute_with_commit(insert_query)
        for i in self.read_all():
            if i[1] == fields['name']:
                return i

    def delete(self, teacher_id: int):
        """Удаление данных о преподавателе
        :param teacher_id: - ID преподавателя
        :return: сообщение об успешном удалении"""
        insert_query = (f"""DELETE FROM subjects WHERE teacher_id = {teacher_id};
                            DELETE FROM teachers WHERE id = {teacher_id}; """
                        )
        self.execute_with_commit(insert_query)
        return self.read_all()

    def connect_with_subject(self, fields: dict):
        """Закрепление преподавателя за предметом
        :param fields: - данные преподавателя, данные предмета
        :return: сведения о занятии у преподавателя"""
        new_id = self.execute_fetchone('SELECT id FROM subjects ORDER BY id DESC LIMIT 1;') + 1
        insert_query = (f"""INSERT INTO subjects (id, teacher_id, subject_id)
                            VALUES ({new_id}, {fields["teacher_id"]}, {fields["subject_id"]});"""
                        )
        self.execute_with_commit(insert_query)
        new_row = self.execute_fetchall(f'SELECT * FROM subjects WHERE subjects.id = {new_id};')
        return new_row


class SubjectController(DatabaseController):

    def create(self, fields: dict):
        """Функция для создания записи"""
        new_id = self.execute_fetchone('SELECT id FROM subject_info ORDER BY id DESC LIMIT 1;') + 1
        insert_query = (f"""INSERT INTO subject_info (id, name, classes_type, planned_workload, actual_workload)
                            Values ('{new_id} ',
                                    '{fields["name"]}',
                                    '{fields["classes_type"]}',
                                    '{fields["planned_workload"]}',
                                    '{fields["actual_workload"]}' );""")
        self.execute_with_commit(insert_query)
        return self.read_all()[-1]

    def read(self, field: int):
        """Просмотр записи
        :param field: - ID предмета
        :return: сведения о предметах у преподавателя"""
        insert_query = (f"""SELECT * FROM subject_info si
                            WHERE si.id = {field}; """
                        )

        result = self.execute_fetchall(insert_query)
        return result

    def read_all(self):
        """Просмотр всех записей в таблице"""
        request = (f'SELECT * FROM subject_info;')
        result = self.execute_fetchall(request)
        return result

    def update(self, fields: dict):
        """Изменения данных о дисциплине
        :param fields: - словарь с изменениями
        :return: новые сведения о дисциплине"""
        insert_query = (f"""UPDATE subject_info
                            SET name = '{fields["name"]}',
                            classes_type = '{fields["classes_type"]}',
                            planned_workload = {fields["planned_workload"]},
                            actual_workload = {fields["actual_workload"]}
                            WHERE id = {fields["id"]}; """
                        )
        self.execute_with_commit(insert_query)
        for i in self.read_all():
            if i[0] == fields['id']:
                return i

    def delete(self, subject_id: int):
        """Удаление данных о дисциплине
        :param subject_id: - ID дисциплины
        :return: сообщение об успешном удалении"""
        insert_query = (f"""DELETE FROM subjects WHERE subject_id = {subject_id};
                            DELETE FROM subject_info WHERE id = {subject_id}; """
                        )
        self.execute_with_commit(insert_query)
        return self.read_all()

    def connect_with_teacher(self, fields: dict):
        """Закрепление предмета за преподавателем
        :param fields: - данные преподавателя, данные предмета
        :return: сведения о занятии у преподавателя"""
        new_id = self.execute_fetchone('SELECT id FROM subjects ORDER BY id DESC LIMIT 1;') + 1
        insert_query = (f"""INSERT INTO subjects (id, teacher_id, subject_id)
                            VALUES ({new_id}, {fields["teacher_id"]}, {fields["subject_id"]});"""
                        )
        self.execute_with_commit(insert_query)
        new_row = self.execute_fetchall(f'SELECT * FROM subjects WHERE subjects.id = {new_id};')
        return new_row