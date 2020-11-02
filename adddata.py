from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField



from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.lang import Builder


import variables as var
import datainput


#Builder.load_file('adddatascreen.kv')

if var.dbase == None and var.dp == None:
    import DBHelper as dbh
    import processingdatadisplay as pdd
    var.dbase = dbh.DBHelper()
    var.alldataDB = var.dbase.get_all_data()
    var.dp = pdd.DataProcess()
    var.dp.set_allperiodsdata()

class AddingNewData(Screen):
    periodsview = ObjectProperty(None)
    td = var.dp.get_now_str()
    yeartext = td[0]
    monthtext = td[1]
    daytext = td[2]
    manytext = td[3]
    
    def get_data_from_texts(self):
        year = MDApp.get_running_app().root.ids.newdataid.input_year.text.strip()
        month = MDApp.get_running_app().root.ids.newdataid.input_month.text.strip()
        day = MDApp.get_running_app().root.ids.newdataid.input_day.text.strip()
        many = MDApp.get_running_app().root.ids.newdataid.input_many.text.strip()
        
        td = var.dp.get_now_str()
        MDApp.get_running_app().root.ids.newdataid.input_year.text = td[0]
        MDApp.get_running_app().root.ids.newdataid.input_month.text = td[1]
        MDApp.get_running_app().root.ids.newdataid.input_day.text = td[2]
        MDApp.get_running_app().root.ids.newdataid.input_many.text = td[3]
        d,s = datainput.DataInput().get_datas(year,month,day,many)
        
        var.dbase.add_data(d.mdate, d.many)
        self.update_data()
        MDApp.get_running_app().root.ids.generaldata.ids.generaldataview.update_data()
    
    
    def update_data(self):
        var.alldataDB = var.dbase.get_all_data()
        var.dp.set_allperiodsdata(var.alldataDB)



if __name__ == '__main__':
    class Test(MDApp):
        #generaldataview = ObjectProperty(None)
        Builder.load_file('adddatascreen.kv')
        def __init__(self):
            super(Test,self).__init__()
        
        def build(self):
            return AddingNewData()
    Test().run()








