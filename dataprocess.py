
import os
import sqlite3
import sys
from random import randint as rint
from pprint import pprint
from datetime import datetime as dtm
import datetime
import re
from dataclasses import dataclass


@dataclass
class Datas:
    mdate:object = datetime.date(dtm.now().year,
                                 dtm.now().month,
                                 dtm.now().day,
                            )
    mtime:object = datetime.datetime.today().time()
    idd:int = -1
    many:float = 0.0


@dataclass
class StringDatas:
    idd:str = '-1'
    mdate:str = '0000.00.00'
    mtime:str = '00.00'
    many:str = '0.0'





class DBHelper:
    # получить все данные сразу
    # получить даты
    # получить суммы
    # 
    def __init__(self, dbname = 'data.db'):
        self.__dbname = dbname
        self.__TABLE = 'manys'
        self.__DATE = 'date'
        self.__TIME = 'time'
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
        self.__CURSOR.execute("""CREATE TABLE IF NOT EXISTS manys
                                 (id INTEGER AUTOINCRIMENT PRIMARY KEY, 
                                  date text, 
                                  time text, 
                                  many real)
                              """)
        self.get_ids()
    
    
    # получает последний id
    def get_ids(self):
        rows = self.__CURSOR.execute("SELECT * FROM manys ORDER BY id")
        temp = rows.fetchall()
        if len(temp) > 0:
            self.__lastid = int(temp[-1][0])
    
    
    # добавление данных в базу
    def add_data(self, datestr, timestr, manyfloat):
        self.__CURSOR.execute("INSERT INTO manys\
                                  (date,time,many)\
                                   VALUES (?,?,?)", 
                                  (datestr,timestr,manyfloat))
        self.__CONN.commit()
        self.__lastid = self.__CURSOR.lastrowid
    
    
    def readerall(self):
        for row in self.__CURSOR.execute("SELECT rowid, * FROM manys"):
            pprint(row)
    
    
    # закрытие базы
    def close(self):
        self.__CONN.close()
    
    
    @property
    def ids(self):
        print(self.__lastid)
    
    
    # удаление данных по id
    def deletedata(self, numid):
        delid = str(numid)
        self.__CURSOR.execute("DELETE FROM manys WHERE id=?",(delid,))
        self.__CONN.commit()
        self.get_ids()
    
    
    # получение списка всех данных из базы
    def get_all_data(self):
        tmpdata = self.__CURSOR.execute("SELECT * FROM manys ORDER BY id").fetchall()
        def foo(dt):
            r = list(map(list,dt))
            return r
        return  foo(tmpdata)
    
    
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
    
    
    def update_data(self, ids, date=None,time=None,many=0.0):
        if date == None:
            date = self.__now()[0]
        if time == None:
            time = self.__now()[1]
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
    
    
    # принимает список строк с данными
    # в формате [ 'id', 'yyyy.mm.dd', 'HH.MM.SS', '$$.$$' ]
    # возвращает объект Datas
    def newDataObject(self, datastrlist):
        ok = True
        data = Datas()
        try:
            d = list(map(int,datastrlist[1].split('.')))+[0,0,0]
            data.mdate = datetime.date(d[0],d[1],d[2])
        except:
            return None
        try:
            d = list(map(int,datastrlist[2].split('.')))+[0,0,0]
            data.mtime = datetime.time(d[0],d[1],d[2])
        except:
            return None
        data.idd = int(datastrlist[0])
        data.many = float(datastrlist[3])
        return data
    
    
    # принимает двумерный список строк с данными
    # возвращает объект список объектов Datas
    def get_datas(self, datastrlist):
        lst = list(map(self.newDataObject,datastrlist))
        return lst
    
    
    # принимает список строк с данными
    # в формате [ 'id', 'yyyy.mm.dd', 'HH.MM.SS', '$$.$$' ]
    # возвращает объект StringDatas
    def get_stringdata(self, datastrlist):
        data       = StringDatas()
        data.idd   = str(datastrlist[0])
        data.mdate = str(datastrlist[1])
        data.mtime = str(datastrlist[2])
        data.many  = str(datastrlist[3])
        return data
    
    
    # список строк из StringDatas
    def get_lst_from_stringdata(self, sd=StringDatas):
        return list([sd.idd, sd.mdate, sd.mtime, sd.many])
    
    
    # список строк из Datas
    def get_lst_from_datas(self, d=Datas):
        return [str(d.idd),str(d.mdate),str(d.mtime),str(d.many)]
    
    
    # преобразует StringDatas в Datas
    def convert_stringdata(self, sd=StringDatas):
        s = self.get_lst_from_stringdata(sd)
        return self.newDataObject(s)
    
    
    # преобразует Datas в StringDatas
    def convert_datas(self, d=Datas):
        s = self.get_lst_from_datas(d)
        return self.get_stringdata(s)
    
    
    def compare_datas(self, dt1:Datas, dt2:Datas):
        if dt1.mdate > dt2.mdate:
            t = dt1
            dt1 = dt2
            dt2 = t
        return dt1,dt2
    
    
    # сортирует список объектов Datas по дате
    def sort_datas(self, DatasArray:list):
        return list(map(self.compare_datas, DatasArray))
    
    
    # принимает двумерный список с данными
    # в формате [ [Datas], [Datas] ]
    # возвращает список словарей
    def get_viewdatas(self, dataobjects:[]):
        viewdata = list()
        if len(dataobjects) == 0:
            return None
        t = dataobjects[0]
        for data in dataobjects:
            d = dict()
            idd = str(data.idd)
            mdate = str(data.mdate)
            mtime = str(data.mtime)
            many = str(data.many)
            s = mdate+'    '+many
            res = dict({'text':s,'integer':idd})
            viewdata.append(d)
        
        return viewdata
    
    
    def add_viewdata(self, viewdata, datastrlist):
        
        return viewdata
    
    
    
def println(string):
    print(string)
    print()


def pprintln(string):
    pprint(string)
    print()

if __name__ == '__main__':
    
    userdata = DBHelper()
    dp = DataProcess()
    
    res = userdata.get_all_data()
    pprint(res)
    datas = dp.get_datas(res)
    pprint(datas)
    datas = dp.sort_datas(datas)
    
    
    userdata.close()
    
    
    
    
    
    
    
    
    
