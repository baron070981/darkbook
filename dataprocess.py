
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


print()

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
    # если есть и она не пустая, получается последний id
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
    
    
    # получает последний id и сохраняет в self.__lastid
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
        return self.__lastid
    
    
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
    def update_data(self, ids, datedt=None,many=0.0):
        if datedt == None:
            datedt = self.__now()[0]
        datestr = self.__toString(datedt)
        self.__CURSOR.execute("UPDATE manys SET date=(?),\
                                                time=(?),\
                                                many=(?)\
                                                WHERE id=(?)",(datestr,many,ids,))
        self.__CONN.commit()


# класс обрабатывает данные
# форматирует для Recycleview
class DataProcess:
    def __init__(self):
        self.datas = list()
        self.__monthname = {1:'январь',2:'февраль',3:'март',
                              4:'апрель',5:'май',6:'июнь',7:'июль',
                              8:'август',9:'сентябрь',10:'октябрь',
                              11:'ноябрь',12:'декабрь',}
        self.__monthnums = {'январь':1,'февраль':2,'март':3,'апрель':4,
                            'май':5,'июнь':6,'июль':7,'август':8,
                            'сентябрь':9,'октябрь':10,'ноябрь':11,'декабрь':12,}
        self.allperiods = dict()
    
    
    def add_data(self, datas:Datas):
        self.datas.append(datas)
    
    
    
    def toString(self, datas:Datas):
        d = str(datas.mdate.year)+'.'+str(datas.mdate.month)+'.'+str(datas.mdate.day)
        return d+'   '+str(datas.many)
    
    
    def viewdates(self, dataslist:[Datas]):
        views = list()
        for data in dataslist:
            s = self.toString(data)
            idd = data.idd
            views.append({'text':s,'integer':idd})
        return views
    
    
    def periods(self, dataslist:[Datas]):
        self.allperiods = dict()
        for data in dataslist:
            self.allperiods[data.mdate.year] = dict()
        
        for data in dataslist:
            self.allperiods[data.mdate.year] = dict({data.mdate.month:dict()})
            
        for data in dataslist:
            self.allperiods[data.mdate.year][data.mdate.month] = dict({data.mdate.day:list()})
        
        for data in dataslist:
            self.allperiods[data.mdate.year][data.mdate.month][data.mdate.day].append([data.many,data.idd])
        return self.allperiods
    
    
    def viewmonthsyear(self):
        views = list()
        for year in self.allperiods:
            for month in self.allperiods[year]:
                views.append({'text':self.__monthname[month]+' / '+str(year)})
        return views
    
    
    def viewmonth(self, monthname, yearstr):
        views = list()
        year = yearstr
        month = self.__monthnums
        per = self.allperiods[year][self.__monthnums[monthname]]
        for data in per:
            for d in per[data]:
                views.append({'text':str(d[0]),'integer':d[1]})
        return views
    
    
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
    dp.periods(alldata)
    
    pprint(dp.viewmonthsyear())
    pprint(dp.viewmonth('февраль',2020))
    
    
    userdata.close()
    
    
    
    
    
    
    
    
    
