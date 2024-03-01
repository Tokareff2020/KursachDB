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
            cursor = connection.cursor()
            return cursor

    def execute(self, request: str) -> None:
        try:
            cursor = self.connect()
            cursor.execute(request)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def execute_fetchall(self, request: str) -> list:
        try:
            cursor = self.connect()
            cursor.execute(request)
            result = cursor.fetchall()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return []
        return result


class TeachersController:

    def create(self, fields: dict):
        """Функция для создания записи"""

    def read(self, fields: dict):
        """Просмотр записи
        :param fields: - данные преподавателя
        :return: сведения о предметах преподавателя"""

    def update(self, fields: dict):
        """Изменения данных о преподавателе
        :param fields: - словарь с изменениями
        :return: новые сведения о преподавателе"""

    def delete(self, fields: dict):
        """Удаление данных о преподавателе
        :param fields: - данные преподавателя
        :return: сообщение об успешном удалении"""

    def connect_with_subject(self, fields: dict):
        """Закрепление преподавателя за предметом
        :param fields: - данные преподавателя, данные предмета
        :return: сведения о предметах преподавателя"""


class SubjectController:

    def create(self, fields: dict):
        """Функция для создания записи"""

    def read(self, field: str):
        """Просмотр записи
        :param field: - название предмета
        :return: сведения о преподавателях, закрепленных за предметом"""

    def update(self, fields: dict):
        """Изменения данных о дисциплине
        :param fields: - словарь с изменениями
        :return: новые сведения о дисциплине"""

    def delete(self, fields: dict):
        """Удаление данных о дисциплине
        :param fields: - данные дисциплины
        :return: сообщение об успешном удалении"""

    def connect_with_teacher(self, fields: dict):
        """Закрепление предмета за преподавателем
        :param fields: - данные преподавателя, данные предмета
        :return: сведения о предметах преподавателя"""

