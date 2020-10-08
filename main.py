

from kivy.config import Config
Config.set('graphics','width','302')
Config.set('graphics','height','575')

from kivymd.app import MDApp
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

#
import os
import configdata as conf
import dataprocess
from pprint import pprint

from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

user = conf.UserConfig() # 
dp = dataprocess.DataProcess()
dbh = dataprocess.DBHelper()
alldata = dbh.get_all_data() # все данные из бд (список dataprocess.Datas)
alldatadp = dp.set_alldata(alldata) # копирование данных в DataProcess()
allperiods = dp.set_allperiodsdata() # получаю данные по всем периодам


class InputScreen(Screen):
    welcomeinfo = StringProperty('welcome to application')
    info = StringProperty('Info string')
    
    def check_password(self):
        pass
    


class DataListScreen(Screen):
    
    def into_create_data(self):
        print('NEW')
    
    

class MonthDataListScreen(Screen):
    #monthview = ObjectProperty(None)
    
    pass


class NewData(Screen):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)


    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)


    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


# App.get_running_app().root.

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]), ' in datalist screen.' )
            print( "Screen: ", MDApp.get_running_app().root.current )
            n = rv.data[index]['text'].split('/')[:2]
            dp.get_monthinfo(n[1],n[0])
            try:
                MDApp.get_running_app().root.monthdatascreen.monthview.foo()
            except:
                pass
        else:
            print("selection removed for {0}".format(rv.data[index]), ' in apply_selection.')


class PeriodsView(RecycleView):
    def __init__(self,**kwargs):
        super(PeriodsView,self).__init__(**kwargs)
        
        data = dp.viewmonthsyear(alldata)
        if data == None or len(data) == 0:
            self.data = []
        else:
            self.data = data
    

class SelectableRecycleBoxLayout2(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''



class SelectableLabel2(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel2, self).refresh_view_attrs(
            rv, index, data)
    

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            print('On_touch_down 2...')
            #self.data2 = list()
        else:
            print("selection removed for {0}".format(rv.data[index]))


class MonthView(RecycleView):
    monthview = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(MonthView,self).__init__(**kwargs)
        #self.data = list()
        print('Monthintent init: ', dp.monthintent)
        #self.data = dp.viewmonthinfo(alldata, dp.monthintent[0],dp.monthintent[1])
        #self.data = [{'text':'data testing 1'}]
    
    def foo(self):
        print('Call from monthview...')
        self.data = dp.viewmonthinfo()
        #self.data = [{'text':'data testing 2'}]
    
    
    
    



class ScreenManag(ScreenManager):
    input_screen = ObjectProperty(None)
    datalistscreen = ObjectProperty(None)
    monthdatascreen = ObjectProperty(None)
    newdataid = ObjectProperty(None)




class BlackbuchApp(MDApp):
    
    def __init__(self):
        super(BlackbuchApp,self).__init__()
        
    def build(self):
        self.theme_cls.primary_palette = "Blue" 
        return ScreenManag()











if __name__ == "__main__":
    BlackbuchApp().run()
    
    
    
    
    
    
    
    
    
    




