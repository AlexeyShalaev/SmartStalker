import pymysql
from config import settings

class AppDB():
    def __init__(self):
        """ Соединение с базой данных """
        try:
            self.connection = pymysql.connect(
                host=settings['host'],
                port=3306,
                user=settings['user'],
                password=settings['password'],
                database=settings['database'],
                cursorclass=pymysql.cursors.DictCursor
            )
            # print("[+] Успешное подключение к БД")
        except Exception as ex:
            print("[x] Ошибка соединения с базой данных | {0}".format(ex))

    def GetData(self):
        """ Получение всех данных из таблицы """
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM `predprof`"
            cursor.execute(sql)
            res = cursor.fetchall()

        except Exception as ex:
            print("[x] Ошибка получения данных из таблицы | {0}".format(ex))
        return res

    def AddData(self, data):
        """ Добавление данных в таблицу """
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO `predprof`(`data`) VALUES (%s)"
            cursor.execute(sql, (data))
            self.connection.commit()
        except Exception as ex:
            print("[x] Ошибка данных данных в таблицу | {0}".format(ex))

    def DeleteData(self, data_id):
        """ Удаление определенных данных из таблицы """
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM `predprof` WHERE `id` = %s"
            cursor.execute(sql, (data_id))
            self.connection.commit()
        except Exception as ex:
            print("[x] Ошибка определенных удаления данных из таблицы | {0}".format(ex))

    def DeleteAllData(self):
        """ Удаление данных из таблицы """
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM `predprof`"
            cursor.execute(sql)
            self.connection.commit()
        except Exception as ex:
            print("[x] Ошибка удаления данных из таблицы | {0}".format(ex))

    def __del__(self):
        """ Закрываем соединение с базой данных """
        try:
            self.connection.cursor().close()
            self.connection.close()
            # print("[-] Закрываю соединение с БД")
        except Exception as ex:
            print('[x] Ошибка при закрытии соединения с БД | {0}'.format(ex))

