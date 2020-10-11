
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
        self.MONTHSYERS = list()
        self.monthintent = ['2020', 'январь']
        self.alldata = list()
        self.allperiodsdata = dict()
        self.monthdata = dict()


    # сохранение данных в self.alldata
    def set_alldata(self, datas:[var.Datas]):
        self.alldata = datas.copy()
    
    
    # конвертация объекта variables.Datas в строку
    def __toString(self, datas:var.Datas):
        d = str(datas.mdate.year)+'.'+str(datas.mdate.month)+'.'+str(datas.mdate.day)
        return d+'   '+str(datas.many)
    
    
    # конвертация названия месяца в поядковый номер
    def __convertmonthname(self, monthname):
        return self.__monthnums[monthname]
    
    
    # конвертация номера месяца в название
    def __convertmonthnum(self, monthnum):
        return self.__monthname[monthnum]
    
    
    # получение периодов из списка данных variables.Datas
    def periods(self, datas:[var.Datas]=None):
        data = datas
        if data == None:
            data = self.alldata
        
        d = dict()
        for y in data:
            d[y.mdate.year] = dict()
        
        for y in d:
            for m in data:
                d[m.mdate.year][m.mdate.month] = list([0.0])
        
        for dt in data:
            d[dt.mdate.year][dt.mdate.month][0]+=dt.many
        
        return d
    
    
    # получения списка для отображения периодов
    def viewmonthsyear(self,datas:[var.Datas]=None):
        views = list()
        d = dict()
        
        per = self.periods(datas)
        for x in per:
            for y in per[x]:
                for z in per[x][y]:
                    s = self.__convertmonthnum(y)+'/'+str(x)+'/'+str(z)
                    views.append({'text':s})
        
        return views
    

    def set_allperiodsdata(self, datas:[var.Datas]=None):
        
        newdatas = datas
        if newdatas == None:
            newdatas = self.alldata
        
        per = self.periods(datas)
        print(per)
        d = dict()
        l = list()
        for data in newdatas:
            d[data.mdate.year] = dict()
        
        for data in newdatas:
            d[data.mdate.year][data.mdate.month] = dict()
        
        for data in newdatas:
            d[data.mdate.year][data.mdate.month][data.mdate.day] = list()
        
        for data in newdatas:
            d[data.mdate.year][data.mdate.month][data.mdate.day].append([data.idd,data.many])
        self.allperiodsdata = d.copy()
        return d


    def get_monthinfo(self, yearstr, monthdata):
        print('Get monthinfo()')
        year = int(yearstr)
        month = None
        if type(monthdata) != str:
            month = int(monthdata)
        else:
            month = self.__convertmonthname(monthdata)
        
        self.monthdata = self.allperiodsdata[year][month]
        #pprint(self.monthdata)

    def viewmonthinfo(self):
        views = list()
        print('View month info')
        for data in self.monthdata:
            for sub in self.monthdata[data]:
                s = str(data)+'  '+str(sub[1])
                views.append({'text':s,'integer':sub[0]})
        pprint(views)
        return views
    

if __name__ == '__main__':
    
    from DBHelper import DBHelper
    
    def println(string):
        print(string)
        print()
    def pprintln(string):
        pprint(string)
        print()
    
    
    
    userdata = DBHelper()
    dp = DataProcess()
    
    for i in range(40):
        d = datetime.date(2020,rint(1,12),rint(1,28))
        userdata.add_data(d,rint(700,10000))
    
    # получаю данные из бд
    # alldata = userdata.get_all_data()[:30]
    # pprint(alldata)
    
    # dp.set_alldata(alldata)
    
    
    # print()
    # per1 = dp.periods()
    # pprint(per1)
    
    # print()
    # vmy = dp.viewmonthsyear()
    # pprint(vmy)
    
    # print()
    # allperdata = dp.set_allperiodsdata()
    # pprint(allperdata)
    
    
    # dp.get_monthinfo(2017,'январь')
    
    # dp.viewmonthinfo()
    
    userdata.close()
    
    
    
    
    
    
    
    
    
