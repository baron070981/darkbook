import re
import datetime


import variables as var


class DataInput:
    def __init__(self):
        pass
    
    
    def __check_year(self,year):
        yearstr = str(year)
        pattern = r'\d+'
        res = ''.join( re.findall(pattern,yearstr) )
        if len(res) < 4:
            return -1
        return int(res[:4])
    
    
    def __check_month(self, month):
        monthstr = str(month)
        if not monthstr:
            return -1
        pattern = r'\d+'
        res = ''.join(re.findall(pattern, monthstr))
        if len(res) == 0:
            return -1
        res = int(res)
        if res > 12 or res < 1:
            return -1
        return int(res)
    
    
    def __check_day(self, day):
        daystr = str(day)
        if not daystr:
            return -1
        pattern = r'\d+'
        res = ''.join(re.findall(pattern, daystr))
        if not res:
            return -1
        res = int(res)
        if res > 31 or res < 1:
            return -1
        return res
    
    
    def __check_many(self, many):
        try:
            res = float(many)
        except:
            return None
        return res
    
    
    def get_datas(self, yearstr, monthstr, daystr, manystr):
        datas = var.Datas()
        year = self.__check_year(yearstr)
        month = self.__check_month(monthstr)
        day = self.__check_day(daystr)
        many = self.__check_many(manystr)
        if year == -1 or month==-1 or day == -1 or many == None:
            print('Type error...')
            print(year,month,day,many)
            return datas, False
        datas.mdate = datetime.date(year,month,day)
        datas.many = many
        return datas, True









if __name__ == '__main__':
    d = DataInput()
    print(d.get_data_text('2020','1','5','2.98'))






