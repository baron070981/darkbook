


'''    Файл создания, изминения, удаления и проверки пароля   '''

from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.lang import Builder

import os
import sqlite3

import variables as var



class PasswordCls:
    def __init__(self):
        self.__DBname = 'secret.db'
        self.__TABLE = 'secret'
        self.__PASSWORD = 'password'
        self.__ID = 'id'
        self.__CONN = None
        self.__CURSOR = None
        self.__PASSWORD = None
        self.UPDATEPSSW = False
    
    
    def dbase(self):
        self.__CONN = sqlite3.connect(self.__DBname)
        self.__CURSOR = self.__CONN.cursor()
        self.__CURSOR.execute("""CREATE TABLE IF NOT EXISTS secret
                                 (id INTEGER PRYMARY KEY,
                                  password text)
                              """)
        tmp = self.__CURSOR.execute("SELECT password FROM secret").fetchone()
        if tmp == None:
            return
        self.__PASSWORD = tmp[0]
    
    
    def set_password(self,password):
        if self.__PASSWORD == None or len(self.__PASSWORD) == 0:
            print('Set password')
            #self.dbase()
            self.__CURSOR.execute("INSERT INTO secret(password) VALUES (?)",(password,))
        tmp = self.__CURSOR.execute("SELECT password FROM secret").fetchone()
        self.__PASSWORD = tmp[0]
        self.__CONN.commit()
    
    
    def get_password(self):
        tmp = self.__CURSOR.execute("SELECT password FROM secret").fetchone()
        self.__PASSWORD = tmp[0]
    
    
    def del_password(self,password):
        self.__CURSOR.execute("INSERT INTO secret(password) VALUES (?)",(password,))
        tmp = self.__CURSOR.execute("SELECT password FROM secret").fetchone()
        self.__PASSWORD = tmp[0]
        self.__CONN.commit()
    
    
    def updatepassword(self, password):
        self.__CURSOR.execute("UPDATE secret SET password=(?)",(password,))
        self.__CONN.commit()
        self.get_password()
    
    
    def check_password(self, password):
        if self.__PASSWORD == password:
            return True
        return False
    
    
    @property
    def ispassw(self):
        if self.__PASSWORD == None or len(self.__PASSWORD.strip()) == 0:
            return False
        return True
    
    
    def close(self):
        if self.__CONN:
            self.__CONN.close()
    
    @property
    def passw(self):
        print(self.__PASSWORD)





class LoginScreen(Screen):
    Builder.load_file('loginscreen.kv')
    welcome = StringProperty('Welcome string')
    errorstring = StringProperty('..........')
    inputpassword = ObjectProperty(None)
    var.dbpassw = PasswordCls()
    
    def on_enter(self):
        var.dbpassw.dbase()
        if not var.dbpassw.ispassw or var.dbpassw.UPDATEPSSW:
            self.welcome = 'придумайте пароль'
            return
        self.welcome = 'введите пароль'
    
    
    def on_leave(self):
        self.errorstring = ''
        #var.dbpassw.close()
    
    
    def check_password(self):
        password = self.inputpassword.text
        if len(password.strip()) == 0:
            self.errorstring = 'пароль не должен быть пустым'
            return
        if not var.dbpassw.UPDATEPSSW:
            if not var.dbpassw.ispassw:
                var.dbpassw.set_password(password)
                MDApp.get_running_app().root.current = 'generaldata'
                self.errorstring = '..........'
                return
            if not var.dbpassw.check_password(password):
                self.errorstring = 'не верный пароль'
                return
        else:
            var.dbpassw.updatepassword(password)
            MDApp.get_running_app().root.current = 'generaldata'
            self.errorstring = '..........'
            var.dbpassw.UPDATEPSSW = False
            return
        MDApp.get_running_app().root.current = 'generaldata'
        self.errorstring = '..........'



class TestLogin(MDApp):
    def __init__(self):
        super(TestLogin,self).__init__()
    
    def build(self):
        Builder.load_file('loginscreen.kv')
        return LoginScreen()

    def on_stop(self):
        print('On stop')
        var.dbpassw.close()









if __name__ == '__main__':
    
    TestLogin().run()
    
    
    
    
    
   # var.dbpassw.close()






