import json
import ftplib
import threading
from os.path import basename

class LocalToServ():
    
    def __init__(self):
        #self.ftp = ftplib.FTP('host', 'username', 'password')
        #self.ftp.login()
        with open("Config.json", "r") as self.conf_op:
            self.OpenedAndRead = self.conf_op.read()
        self.parsed_string = json.loads(self.OpenedAndRead)
        print(self.parsed_string["FileNames"])
        print(self.parsed_string["PathsOnServer"])
    
    def send(self):
        self.i=0
        while self.i < len(self.parsed_string["FileNames"]):
            print(basename(self.parsed_string["FileNames"][self.i]["FileName"]))
            try:
                my_thread = threading.Thread(target=self.upload(self.parsed_string["FileNames"][self.i]["FileName"], self.parsed_string["PathsOnServer"][self.i]["Path"]), name=self.i)
                my_thread.start()
            except:
                print("Ошибка: отсутствуют пути для отправления")
            self.i+=1
        #self.end()
            
    def upload(self, filename, path):
        print(f"{basename(filename)} отправлен в {path}")
        #try:
            #with open(filename , 'rb') as obj:
                #ftp.storbinary('STOR ' + path + "\\" + basename(filename), obj)
        #except:
            #print("Ошибка: Невозможно отправить файл. Проверьте правильность указанного имени и директории")
    
    def end(self):
        self.ftp.quit()
    
p = LocalToServ()

p.send()

