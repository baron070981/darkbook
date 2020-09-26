import os


class UserConfig:
    '''
    
    создание, удаление, изменение пароля
    сравнение паролей
    
    '''
    
    def __init__(self):
        self.__secretfile   = 'user_config.txt'
        self.__PASSWORD     = ''
        self.__FILENOTEMPTY = False
        self.__EXISTSFILE   = False
        
        self.__get_password()
    
    
    def __get_password(self):
        files = os.listdir('.')
        if self.__secretfile not in files:
            with open(self.__secretfile, 'w') as f:
                pass
            self.__EXISTSFILE = True
        with open(self.__secretfile, 'r') as f:
            password = f.read().strip()
        if len(password) > 0:
            self.__PASSWORD = password
            self.__FILENOTEMPTY = True
    
    
    
    
    
    
    @property
    def printcls(self):
        password = 'Empty password string.'
        if len(self.__PASSWORD) > 0:
            password = self.__PASSWORD
        
        print('Password:', password)
    
    
    
    

if __name__ == '__main__':
    user = UserConfig()
    user.printcls
    
    
    
    
    
    
    
    
    
    
    
