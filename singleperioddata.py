
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog

from kivy.uix.screenmanager import Screen
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

if var.dbase == None:
    var.dbase = dbh.DBHelper()
    var.alldataDB = var.dbase.get_all_data()
    

if var.dp == None:
    var.dp = pdd.DataProcess()
    var.dp.set_alldata(var.alldataDB)
    

class ContentDialog(BoxLayout):
    contentdialog = ObjectProperty(None)



class SinglePeriodDataScreen(Screen):
    dialog = None
    def on_enter(self):
        MDApp.get_running_app().root.ids.period.ids.periodview.upload_data(var.year,var.month)
    
    def on_leave(self):
        var.year, var.month = '','';
    
    def dialogshow(self):
        self.dialog=MDDialog(type='custom',content_cls=ContentDialog(),size_hint_x=0.9)
        self.dialog.ids.container.remove_widget(self.dialog.ids.title)
        self.dialog.ids.spacer_top_box.padding = ('5dp','5dp','5dp','5dp')
        self.dialog.ids.container.padding = (0,0,0,0)
        self.dialog.md_bg_color= (0, 0, 0, 1)
        self.dialog.open()
    
    def dialog_close(self):
        var.TOUCH = False
        self.dialog.dismiss(force=True)
        
    
    def deletedata(self):
        var.dbase.deletedata(int(var.idd))
        var.alldataDB = var.dbase.get_all_data()
        var.dp.set_alldata(var.alldataDB)
        var.dp.set_allperiodsdata(var.alldataDB)
        MDApp.get_running_app().root.ids.period.ids.periodview.upload_data(var.year,var.month)
        MDApp.get_running_app().root.ids.generaldata.ids.generaldataview.update_data()
        self.dialog_close()


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
        if is_selected and var.TOUCH:
            MDApp.get_running_app().root.ids.period.dialogshow()
            var.idd = rv.data[index]['integer']
        else:
            pass
    
    def foo(self):
        var.TOUCH = True



class SinglePeriodView(RecycleView):
    periodview = ObjectProperty(None)
    def __init__(self,**kwargs):
        super(SinglePeriodView,self).__init__(**kwargs)
    
    
    def upload_data(self,year,month):
        try:
            data = var.dp.get_monthinfo(year,month)
            self.data = var.dp.viewmonthinfo()
        except Exception as e:
            self.data = [{'text':'{},{}'.format(var.month,var.year)}]







