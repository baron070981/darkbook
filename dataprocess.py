
import os
import sqlite3
import sys
from random import randint as rint
from pprint import pprint
from datetime import datetime as dtm
import datetime
import re
from dataclasses import dataclass


'''
создание базы
получение данных из базы
изменение данных в базе
удаление данных из базы

1.
на вход: Datas или список Datas
на выход: Datas или список Datas
1.
на вход: список строк с данными
на выход: список строк с данными

'''

@dataclass
class Datas:
    idd:int = -1
    mdate:object = datetime.date(dtm.now().year,
                                 dtm.now().month,
                                 dtm.now().day,
                            )
    many:float = 0.0




class DBHelper:
    # получить все данные сразу
    # получить даты
    # получить суммы
    # 
    def __init__(self, dbname = 'data.db'):
        self.__dbname = dbname
        self.__TABLE = 'manys'
        self.__DATE = 'date'
        self.__MANY = 'many'
        self.__ID = 'id'
        self.__CONN = sqlite3.connect(self.__dbname)
        self.__CURSOR = self.__CONN.cursor()
        self.__lastid = 0
        self.createdb()

    
    # создается база если ее нет
    # если есть, получается последний id
    def createdb(self):
        print("Create new database...")
        # создается бд если не существует
        self.__CURSOR.execute("""CREATE TABLE IF NOT EXISTS manys
                                 (id INTEGER PRIMARY KEY, 
                                  date text,
                                  many real)
                              """)
        # получение последнего id
        self.__get_ids()
    
    
    # получает последний id
    def __get_ids(self):
        rows = self.__CURSOR.execute("SELECT * FROM manys ORDER BY id")
        temp = rows.fetchall()
        if len(temp) > 0:
            self.__lastid = int(temp[-1][0])
    
    
    # добавление данных в базу
    # datetm - datetime
    # manyfloat - float rub.kop
    def add_data(self, datetm, manyfloat):
        datestr = str(datetm.year)+'.'+str(datetm.month)+'.'+str(datetm.day)
        self.__CURSOR.execute("INSERT INTO manys\
                                (date,many)\
                                 VALUES (?,?)", 
                                (datestr,manyfloat))
        # сохранение данных
        self.__CONN.commit()
        # изменение последнего id
        self.__lastid = self.__CURSOR.lastrowid
    
    
    # закрытие базы
    def close(self):
        self.__CONN.close()
    
    
    # вывод последнего id
    @property
    def ids(self):
        print(self.__lastid)
    
    
    # удаление данных по id
    def deletedata(self, numid):
        delid = str(numid)
        self.__CURSOR.execute("DELETE FROM manys WHERE id=?",(delid,))
        self.__CONN.commit()
        self.get_ids()
    
    
    # форматирует кортеж с данными из бд
    # в список формата [idd:int, date:datetime.date, many:float]
    def __formatdata(self, data):
        idd = data[0]
        tmp = list(map(int, data[1].split('.')))+[0,0,0]
        mdate = datetime.date(tmp[0],tmp[1],tmp[2])
        many = float(data[2])
        return list([idd,mdate,many])
    
    
    # получение списка всех данных из базы
    # возвращает список объектов Datas
    def get_all_data(self):
        tmpdata = self.__CURSOR.execute("SELECT * FROM manys ORDER BY id").fetchall()
        def foo(dt):
            r = list(map(self.__formatdata,dt))
            return r
        def foo2(dlst):
            return Datas(dlst[0],dlst[1],dlst[2])
        lst = foo(tmpdata)
        lst.sort(key = lambda x: x[1])
        lst = list(map(foo2, lst))
        return lst
    
    
    # получение данных из одного столбца namecolumn. [id,date] или  [id,many]
    def get_column_data(self, namecolumn):
        if namecolumn == 'date':
            tmpdata = self.__CURSOR.execute("SELECT id,date FROM \
                                             manys ORDER BY id").fetchall()
        elif namecolumn == 'many':
            tmpdata = self.__CURSOR.execute("SELECT id,many FROM \
                                             manys ORDER BY id").fetchall()
        else:
            return None
        def __dmap(st):
            return list([st[0],st[1]])
        return list(map(__dmap, tmpdata))
    
    
    # используется в get_datemany()
    def __dmmap(self, st):
            res = list(st)
            return list([res[0],res[1],res[2]])
    
    
    # получение списка данных из столбцов date и many
    def get_datemany(self):
        tmpdata = self.__CURSOR.execute("SELECT id,date,many FROM \
                                         manys ORDER BY id").fetchall()
        return list(map(self.__dmmap, tmpdata))
    
    
    def __now(self):
        d = datetime.datetime.now()
        return d.strftime("%Y.%m.%d"),d.strftime("%H.%M.%S")
    
    
    def update_data(self, ids, date=None,many=0.0):
        if date == None:
            date = self.__now()[0]
        self.__CURSOR.execute("UPDATE manys SET date=(?),\
                                                time=(?),\
                                                many=(?)\
                                                WHERE id=(?)",(date,time,many,ids,))
        self.__CONN.commit()



class DataProcess:
    def __init__(self):
        self.datas = list()
        self.datastrings = list()
        self.__periodsname = {1:'январь',2:'февраль',3:'март',
                              4:'апрель',5:'май',6:'июнь',7:'июль',
                              8:'август',9:'сентябрь',10:'октябрь',
                              11:'ноябрь',12:'декабрь',}
        self.periods = list()
    
    
    
def println(string):
    print(string)
    print()


def pprintln(string):
    pprint(string)
    print()

if __name__ == '__main__':
    
    userdata = DBHelper()
    dp = DataProcess()
    
    d = datetime.date(2020,2,10)
    userdata.add_data(d,28.00)
    
    # получаю данные из бд
    alldata = userdata.get_all_data()
    pprint(alldata)
    
    
    userdata.close()
    
    
    
    
    
    
    
    
    
