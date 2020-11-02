import os
import sqlite3
import sys
from random import randint as rint
from pprint import pprint
from datetime import datetime as dtm
import datetime
import re
from dataclasses import dataclass

import variables as var




class DBHelper:
    # получить все данные сразу
    # получить даты
    # получить суммы
    # 
    def __init__(self, dbname = 'data.db'):
        self.__dbname = dbname
        self.__TABLE = 'moneytab'
        self.__DATE = 'date'
        self.__MANY = 'money'
        self.__ID = 'id'
        self.__CONN = sqlite3.connect(self.__dbname)
        self.__CURSOR = self.__CONN.cursor()
        self.__lastid = 0
        self.createdb()

    
    # создается база если ее нет
    # если есть и она не пустая, получается последний id
    def createdb(self):
        # создается бд если не существует
        self.__CURSOR.execute("""CREATE TABLE IF NOT EXISTS moneytab
                                 (id INTEGER PRIMARY KEY, 
                                  date text,
                                  money real)
                              """)
        # получение последнего id
        self.__get_ids()
    
    
    # получает последний id и сохраняет в self.__lastid
    def __get_ids(self):
        rows = self.__CURSOR.execute("SELECT * FROM moneytab ORDER BY id")
        temp = rows.fetchall()
        if len(temp) > 0:
            self.__lastid = int(temp[-1][0])
    
    
    # добавление данных в базу
    # datetm - datetime
    # moneyfloat - float rub.kop
    def add_data(self, datetm, moneyfloat):
        datestr = str(datetm.year)+'.'+str(datetm.month)+'.'+str(datetm.day)
        self.__CURSOR.execute("INSERT INTO moneytab\
                                (date,money)\
                                 VALUES (?,?)", 
                                (datestr,moneyfloat))
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
        return self.__lastid
    
    
    # удаление данных по id
    def deletedata(self, numid):
        delid = str(numid)
        self.__CURSOR.execute("DELETE FROM moneytab WHERE id=?",(delid,))
        self.__CONN.commit()
        self.__get_ids()
    
    
    # форматирует кортеж с данными из бд
    # в список формата [idd:int, date:datetime.date, money:float]
    def __formatdata(self, data):
        idd = data[0]
        tmp = list(map(int, data[1].split('.')))+[0,0,0]
        mdate = datetime.date(tmp[0],tmp[1],tmp[2])
        money = float(data[2])
        return list([idd,mdate,money])
    
    
    # получение списка всех данных из базы
    # возвращает список объектов Datas
    def get_all_data(self):
        tmpdata = self.__CURSOR.execute("SELECT * FROM moneytab ORDER BY id").fetchall()
        def foo(dt):
            r = list(map(self.__formatdata,dt))
            return r
        def foo2(dlst):
            return var.Datas(dlst[0],dlst[1],dlst[2])
        lst = foo(tmpdata)
        lst.sort(key = lambda x: x[1])
        lst = list(map(foo2, lst))
        return lst
    
    
    # получение данных из одного столбца namecolumn. [id,date] или  [id,money]
    def get_column_data(self, namecolumn):
        if namecolumn == 'date':
            tmpdata = self.__CURSOR.execute("SELECT id,date FROM \
                                             moneytab ORDER BY id").fetchall()
        elif namecolumn == 'many':
            tmpdata = self.__CURSOR.execute("SELECT id,money FROM \
                                             moneytab ORDER BY id").fetchall()
        else:
            return None
        def __dmap(st):
            return list([st[0],st[1]])
        return list(map(__dmap, tmpdata))
    
    
    # используется в get_datemoney()
    def __dmmap(self, st):
            res = list(st)
            return list([res[0],res[1],res[2]])
    
    
    # получение списка данных из столбцов date и money
    def get_datemoney(self):
        tmpdata = self.__CURSOR.execute("SELECT id,date,money FROM \
                                         moneytab ORDER BY id").fetchall()
        return list(map(self.__dmmap, tmpdata))
    
    
    # возвращает текущую дату.
    # используется при ошибке даты
    def __now(self):
        dt = datetime.datetime.now()
        return datetime.date(dt.year,dt.month,dt.day)
    
    
    # принимает обект datetime.date
    # возвращает строку с датой
    def __toString(self, datedt):
        return datetime.strftime('%Y.%m.%d')
    
    
    # изменение данных в бд по id
    def update_data(self, ids, datedt=None,money=0.0):
        if datedt == None:
            datedt = self.__now()[0]
        datestr = self.__toString(datedt)
        self.__CURSOR.execute("UPDATE moneytab SET date=(?),\
                                                time=(?),\
                                                money=(?)\
                                                WHERE id=(?)",(datestr,money,ids,))
        self.__CONN.commit()












