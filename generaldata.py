
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


from kivy.lang import Builder

from pprint import pprint

import variables as var
import DBHelper as dbh
import processingdatadisplay as pdd


var.dbase = dbh.DBHelper()
var.alldataDB = var.dbase.get_all_data()
var.dp = pdd.DataProcess()
var.dp.set_allperiodsdata()

class GeneralDataScreen(Screen):
    
    data1 = {'images/new.png':'new',
             'images/upd.png':'update',
             'images/exiticon.png':'exit'}
    
    def callback (self, instance):
            pprint(instance.icon)
            if instance.icon == 'images/new.png':
                MDApp.get_running_app().root.current = 'newdata'
                MDApp.get_running_app().root.ids.generaldata.ids.multibtn.close_stack()
            elif instance.icon == 'images/exiticon.png':
                MDApp.get_running_app().stop()
                MDApp.get_running_app().root.ids.generaldata.ids.multibtn.close_stack()
            elif instance.icon == 'images/upd.png':
                self.new_password()
                MDApp.get_running_app().root.current = 'loginscreen'
                MDApp.get_running_app().root.ids.generaldata.ids.multibtn.close_stack()
            else:
                pass
    
    def new_password(self):
        var.dbpassw.UPDATEPSSW = True
        return


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
            txt = rv.data[index]['text'].split('/')
            var.year, var.month = txt[1],txt[0]
        else:
            pass



class GeneralDataView(RecycleView):
    generaldataview = ObjectProperty(None)
    geeneraldata = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(GeneralDataView,self).__init__(**kwargs)
        var.dbase.createdb()
        var.alldataDB = var.dbase.get_all_data()
        #dbh.close()
        var.dp.set_allperiodsdata(var.alldataDB)
        self.data = []
        self.data = var.dp.viewmonthsyear(var.alldataDB)
        

    def update_data(self):
        var.dp.set_allperiodsdata(var.alldataDB)
        self.data = var.dp.viewmonthsyear(var.alldataDB)






if __name__ == '__main__':
 
    
    class Test(MDApp):
        #generaldataview = ObjectProperty(None)
        Builder.load_file('generaldatascreen.kv')
        def __init__(self):
            super(Test,self).__init__()
        
        def build(self):
            return GeneralDataScreen()
    Test().run()

