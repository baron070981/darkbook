from kivy.config import Config
Config.set('graphics','width','302')
Config.set('graphics','height','575')

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.theming import ThemeManager as tm

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.lang import Builder

import os
from pprint import pprint

import variables as var
from logintoapp import LoginScreen
import generaldata
import singleperioddata
import adddata


import variables as var
import DBHelper as dbh
import processingdatadisplay as pdd


var.dbase = dbh.DBHelper()
var.alldataDB = var.dbase.get_all_data()
var.dp = pdd.DataProcess()
var.dp.set_alldata(var.alldataDB)



class ScreenManag(ScreenManager):
    inputpassword = ObjectProperty(None)
    generaldata = ObjectProperty(None)
    period = ObjectProperty(None)
    newdataid = ObjectProperty(None)


class DarkbookApp(MDApp):
    Builder.load_file('dialogscreen.kv')
    contentdialog = ObjectProperty()
    
    def __init__(self):
        super(DarkbookApp,self).__init__()
    
    
    def build(self):
        self.theme_cls.primary_palette =  "Blue"
        self.theme_cls.primary_hue =  "900"
        self.theme_cls.theme_style = "Dark" 
        return ScreenManag()

    def on_stop(self):
        var.dbase.close()
        var.dbpassw.close()
    
    

if __name__ == '__main__':
    DarkbookApp().run()




