from kivy.app import App
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

from kivy.config import Config

import os
import configdata as conf
import dataprocess


Config.set('graphics','width','302')
Config.set('graphics','height','575')

user = conf.UserConfig()
dp = dataprocess.DataProcess()
dbh = dataprocess.DBHelper()
alldata = dbh.get_all_data()



class InputScreen(Screen):
    welcomeinfo = StringProperty('')
    info = StringProperty('Info string')
    
    def check_password(self):
        pass
    


class DataListScreen(Screen):
    
    def into_create_data(self):
        print('NEW')


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

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            print(self.index)
        else:
            print("selection removed for {0}".format(rv.data[index]))




class PeriodsView(RecycleView):
    def __init__(self,**kwargs):
        super(PeriodsView,self).__init__(**kwargs)
        # self.data = [ { 'text':'10.01.2020-09.02.2020' }, 
                      # { 'text':'10.02.2020-09.03.2020' }, 
                      # { 'text':'10.03.2020-09.04.2020' }, 
                      # { 'text':'10.04.2020-09.05.2020' }, 
                      # { 'text':'10.05.2020-09.06.2020' }, 
                      # { 'text':'10.06.2020-09.07.2020' }, 
                      # { 'text':'10.07.2020-09.08.2020' }, 
                      # { 'text':'10.08.2020-09.09.2020' }, 
                      # { 'text':'10.09.2020-09.10.2020' }, 
                      # { 'text':'10.10.2020-09.11.2020' }, 
                      # { 'text':'10.11.2020-09.12.2020' }, 
                      # { 'text':'10.12.2020-09.01.2021' }, 
                      # { 'text':'10.01.2020-09.02.2021' }, 
                      # { 'text':'10.02.2020-09.03.2021' }, 
                      # { 'text':'10.03.2020-09.04.2021' }, 
                      # { 'text':'10.04.2020-09.05.2021' }, 
                      # { 'text':'10.05.2020-09.06.2021' }, 
                      # { 'text':'10.06.2020-09.07.2021' }, 
                      # { 'text':'10.07.2020-09.08.2021' }, 
                      # { 'text':'10.08.2020-09.09.2021' }, 
                      # { 'text':'10.09.2020-09.10.2021' }, 
                    # ]
        self.data = dp.get_viewdatas(alldata)
    
    
    def into_dataview(self):
        pass



class ScreenManag(ScreenManager):
    pass


class BlackbuchApp(App):
    
    def __init__(self):
        super(BlackbuchApp,self).__init__()
        
    def build(self):
        return ScreenManag()











if __name__ == "__main__":
    BlackbuchApp().run()
    
    
    
    
    
    
    
    
    
    

