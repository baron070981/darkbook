from dataclasses import dataclass
from datetime import datetime as dtm
import datetime
from kivymd.uix.dialog import MDDialog


dbpassw = None
dbdata = None

fakedata = [{'text':'data 1'},{'text':'data 1'},{'text':'data 1'},
            {'text':'data 1'},{'text':'data 1'},{'text':'data 1'},
            {'text':'data 1'},{'text':'data 1'},{'text':'data 1'},
            {'text':'data 1'},{'text':'data 1'},{'text':'data 1'},
            {'text':'data 1'},{'text':'data 1'},{'text':'data 1'},
            ]


@dataclass
class Datas:
    idd:int = -1
    mdate:object = datetime.date(dtm.now().year,
                                 dtm.now().month,
                                 dtm.now().day,
                            )
    money:float = 0.0

alldataDB = None
month = ''
year = ''

idd = 0

dbase = None
dp = None

TOUCH = False
dialog = None


