

from kivy.config import Config
Config.set('graphics','width','302')
Config.set('graphics','height','575')

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem

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

import os
from pprint import pprint

import datainput
from DBHelper import DBHelper
import configdata as conf
import processingdatadisplay as pdd
import variables as var


user = conf.UserConfig() # 
dbh = DBHelper()
dp = pdd.DataProcess()


class InputScreen(Screen):
    welcomeinfo = StringProperty('welcome to application')
    info = StringProperty('Info string')
    
    def check_password(self):
        pass
    


class DataListScreen(Screen):
    def on_enter(self):
        print('Datalistscreen...')
    #pass
    
    
class MonthDataListScreen(Screen):
    def on_enter(self):
        print('Monthdatalist')


class NewData(Screen):
    periodsview = ObjectProperty(None)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)


    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)


    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]), ' in datalist screen.' )
        else:
            print("selection removed for {0}".format(rv.data[index]), ' in apply_selection.')


class PeriodsView(RecycleView):
    def __init__(self,**kwargs):
        super(PeriodsView,self).__init__(**kwargs)
        dbh.createdb()
        var.alldataDB = dbh.get_all_data()
        dbh.close()
        self.data = dp.viewmonthsyear(var.alldataDB)
    

class SelectableRecycleBoxLayout2(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''



class SelectableLabel2(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel2, self).refresh_view_attrs(
            rv, index, data)
    

    def on_touch_down(self, touch):
        if super(SelectableLabel2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class MonthView(RecycleView):
    monthview = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(MonthView,self).__init__(**kwargs)
        
    

class ScreenManag(ScreenManager):
    input_screen = ObjectProperty(None)
    datalistscreen = ObjectProperty(None)
    monthdatascreen = ObjectProperty(None)
    newdataid = ObjectProperty(None)




class BlackbuchApp(MDApp):
    
    def __init__(self):
        super(BlackbuchApp,self).__init__()
        
    
    def build(self):
        self.theme_cls.primary_palette =  "Red"
        self.theme_cls.theme_style = "Dark" 
        return ScreenManag()











if __name__ == "__main__":
    BlackbuchApp().run()
    
    
    
    
    
    
    
    
    
    




