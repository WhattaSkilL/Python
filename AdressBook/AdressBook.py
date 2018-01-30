from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle, os

class AdresBook():

	def __init__(self):
		#Создание окна
		self.root = Tk()
		self.root.minsize(width=800,height=640)
		self.root.maxsize(width=800,height=640)
		self.root.title("Адресная книга")
		#Загрузка изображения
		self.ph_im = PhotoImage(file='Create.gif')
		self.MainIMG = PhotoImage(file='Main.gif')
		#Рамка главного окна
		self.Mainramk = Frame(self.root, bd=0)
		self.Mainramk.place(x=0,y=0,width=800,height=640)
		self.MainramkCanv = Canvas(self.Mainramk,width=800, height=640, highlightthickness=0)
		self.MainramkCanv.place(x=0,y=0)
		self.MainramkCanv.create_image(0,0,anchor=NW,image=self.MainIMG)
		#Создание списков
		self.familiyaL=[];self.nameL=[];self.otchestvoL=[];self.nomerL=[];self.emailL=[];self.infoL=[]
		self.fsave1=open("AdressBook.txt",'rb')
		self.loadtype=pickle.load(self.fsave1)
		self.familiyaL=self.loadtype[0]; self.nameL=self.loadtype[1]; self.otchestvoL=self.loadtype[2];	self.nomerL=self.loadtype[3]; self.emailL=self.loadtype[4];	self.infoL=self.loadtype[5];
		self.fsave1.close()
		#Создание листбокса
		self.listbox = Listbox(self.Mainramk)
		self.listbox.place(x=24,y=163,width=352,height=394)
		self.listbox.bind('<<ListboxSelect>>', lambda e: self.otobrajenie(None))
		# заполнение листбокса
		self.obnovlenie(1)
		# создание кнопок и полей
		self.entPhoneMain = Entry(self.Mainramk, width=1)
		self.entPhoneMain.place(x=419,y=163, width=163,height=34)
		
		self.entEmailMain = Entry(self.Mainramk, width=1)
		self.entEmailMain.place(x=613,y=163, width=163,height=34)
		
		self.entSearch = Entry(self.Mainramk, width=1)
		self.entSearch.place(x=613,y=26, width=163,height=34)
		self.entSearch.bind("<Return>", lambda e: self.SearchFunc(None))
		
		self.entKontachMain = Text(self.Mainramk,width=20,height=3,font="Gabriola", wrap=WORD, spacing2=0)
		self.entKontachMain.place(x=419,y=271,width=357,height=345)
		
		self.bDobaviti = Button(self.Mainramk, text="Добавить контакт")
		self.bDobaviti.place(x=213,y=582,width=163,height=34)
		self.bDobaviti.bind("<Button-1>", lambda e: self.Dobavlenie())
		
		self.bDobaviti = Button(self.Mainramk, text="Сохранить")
		self.bDobaviti.place(x=213,y=26,width=163,height=34)
		self.bDobaviti.bind("<Button-1>", lambda e: self.Sohranenie())
		
		self.bUdaliti = Button(self.Mainramk, text="Удалить контакт")
		self.bUdaliti.place(x=24,y=582,width=163,height=34)
		self.bUdaliti.bind("<Button-1>", lambda e: self.Udalenie(None))
		
		self.bSbros = Button(self.Mainramk, text="Сброс")
		self.bSbros.place(x=213,y=109,width=78,height=34)
		self.bSbros.bind("<Button-1>", lambda e: self.obnovlenie(1))
		
		self.variableUPR = StringVar(self.Mainramk)
		self.variableUPR.set("А-Я")
		self.OptionButUPR = OptionMenu(self.Mainramk,  self.variableUPR, "А-Я", "Я-А", command=self.Sortirovka)
		self.OptionButUPR.place(x=295,y=109,width=81,height=34)
		
		self.variable = StringVar(self.Mainramk)
		self.variable.set("ФИО")
		self.OptionBut = OptionMenu(self.Mainramk,  self.variable, "ФИО", "Тел.", "Емейл")
		self.OptionBut.place(x=504,y=26,width=78,height=34)
		
	def Sortirovka(self,event): #Функция упорядочивания
		OptionsetUPR=self.variableUPR.get()
		if OptionsetUPR=="А-Я":
			self.nameL.sort(key=self.familiyaL.sort());self.otchestvoL.sort(key=self.familiyaL.sort());self.nomerL.sort(key=self.familiyaL.sort());self.emailL.sort(key=self.familiyaL.sort());self.infoL.sort(key=self.familiyaL.sort());self.familiyaL.sort()
			self.obnovlenie(1)
		elif OptionsetUPR=="Я-А":
			self.nameL.sort(key=self.familiyaL.sort(),reverse=True);self.otchestvoL.sort(key=self.familiyaL.sort(),reverse=True);self.nomerL.sort(key=self.familiyaL.sort(),reverse=True);self.emailL.sort(key=self.familiyaL.sort(),reverse=True);self.infoL.sort(key=self.familiyaL.sort(),reverse=True);self.familiyaL.sort(reverse=True)
			self.obnovlenie(1)
	
	def SearchFunc(self, event): #Функция поиска
		WordForSearch=self.entSearch.get()
		Optionset=self.variable.get()
		if Optionset=="ФИО":
			SearcedAll=[]
			TablOfSearchedFamil=[]
			TablOfSearchedImya=[]
			TablOfSearchedOtch=[]
			if self.familiyaL.count(WordForSearch)==0 and self.nameL.count(WordForSearch)==0 and self.otchestvoL.count(WordForSearch)==0:
				messagebox.showinfo("Поиск", "Ничего не найдено")
			else:
				if self.familiyaL.count(WordForSearch)>0:
					i=-1
					while True:
						try:
							i=self.familiyaL.index(WordForSearch, i+1)
							TablOfSearchedFamil.append(i)
						except:
							break
				if self.nameL.count(WordForSearch)>0:
					i=-1
					while True:
						try:
							i=self.nameL.index(WordForSearch, i+1)
							TablOfSearchedImya.append(i)
						except:
							break
				if self.otchestvoL.count(WordForSearch)>0:
					i=-1
					while True:
						try:
							i=self.otchestvoL.index(WordForSearch, i+1)
							TablOfSearchedOtch.append(i)
						except:
							break
				SearcedAll.extend(TablOfSearchedFamil)
				SearcedAll.extend(TablOfSearchedImya)
				SearcedAll.extend(TablOfSearchedOtch)
				self.new_SearcedAll=list(set(SearcedAll))
				self.obnovlenie(2)
		elif Optionset=="Тел.":
			if self.nomerL.count(WordForSearch)==0:
				messagebox.showinfo("Поиск", "Ничего не найдено")
			else:
				self.new_SearcedAll=[]
				TablOfSearchednomer=[]
				i=-1
				while True:
					try:
						i=self.nomerL.index(WordForSearch, i+1)
						TablOfSearchednomer.append(i)
					except:
						break
				self.new_SearcedAll.extend(TablOfSearchednomer)
				self.obnovlenie(2)
		elif Optionset=="Емейл":
			if self.emailL.count(WordForSearch)==0:
				messagebox.showinfo("Поиск", "Ничего не найдено")
			else:
				self.new_SearcedAll=[]
				TablOfSearchedemail=[]
				i=-1
				while True:
					try:
						i=self.emailL.index(WordForSearch, i+1)
						TablOfSearchedemail.append(i)
					except:
						break
				self.new_SearcedAll.extend(TablOfSearchedemail)
				self.obnovlenie(2)
		
	def otobrajenie(self, event): #Функция заполнения дополнительных полей
		ImyaVibranogo = self.listbox.get(self.listbox.curselection())
		i=0
		while True:
			if ImyaVibranogo == self.familiyaL[i] + " " + self.nameL[i] + " " + self.otchestvoL[i]:
				break
			else:
				i+=1
		print("Выбран: " + str(i))
		self.entPhoneMain.delete(0,END)
		self.entPhoneMain.insert(END,self.nomerL[i])
		self.entEmailMain.delete(0,END)
		self.entEmailMain.insert(END,self.emailL[i])
		self.entKontachMain.delete(1.0,END)
		self.entKontachMain.insert(END,self.infoL[i])
		print(self.familiyaL, self.nameL, self.otchestvoL,self.nomerL, self.emailL,self.infoL)
				
	def obnovlenie(self,x): #Заполнение листбокса
		if x==1:
			self.listbox.delete(0,END)
			i=0
			KolKont=len(self.familiyaL)
			while i != KolKont:
				k = (self.familiyaL[i] + " " + self.nameL[i] + " " + self.otchestvoL[i])
				self.listbox.insert(END, k)
				i+=1
		elif x==2:
			self.listbox.delete(0,END)
			d=0
			KolKont=len(self.new_SearcedAll)
			while d!=KolKont:
				i=self.new_SearcedAll[d]
				k = (self.familiyaL[i] + " " + self.nameL[i] + " " + self.otchestvoL[i])
				self.listbox.insert(END, k)
				d+=1
			messagebox.showinfo("Поиск", "Найдено: " + str(KolKont))
			
	def Dobavlenie(self): #Переход в режим добавления человека
		#Рамка
		self.ramk = Frame(self.root, bd=0)
		self.ramk.place(x=0,y=0,width=800,height=640)
		#Фон
		
		self.canv111 = Canvas(self.ramk,width=800, height=640, highlightthickness=0)
		self.canv111.place(x=0,y=0)
		self.canv111.create_image(0,0,anchor=NW,image=self.ph_im)
		#Поля ввода
		self.entFam = Entry(self.ramk, width=1)
		self.entFam.place(x=212,y=264, width=163,height=34)
		
		self.entName = Entry(self.ramk, width=1)
		self.entName.place(x=212,y=211, width=163,height=34)
		
		self.entOtch = Entry(self.ramk, width=1)
		self.entOtch.place(x=212,y=316, width=163,height=34)
		
		self.entEmail = Entry(self.ramk, width=1)
		self.entEmail.place(x=613,y=211, width=163,height=34)
		
		self.entPhone = Entry(self.ramk, width=1)
		self.entPhone.place(x=613,y=264, width=163,height=34)
		
		self.entKontach = Entry(self.ramk, width=1)
		self.entKontach.place(x=613,y=316, width=163,height=34)
		
		#Кнопки
		self.SozdatiBut = Button(self.ramk,text="Добавить контакт")
		self.SozdatiBut.place(x=412,y=394,width=163,height=34)
		self.SozdatiBut.bind("<Button-1>", lambda e: self.DobavitiKont())
		
		self.OtmenaBut = Button(self.ramk,text="Вернуться назад")
		self.OtmenaBut.place(x=225,y=394,width=163,height=34)
		self.OtmenaBut.bind("<Button-1>", lambda e: self.ramk.destroy())
		
	def Udalenie(self, event): #Удаление активного человека из списка
		ImyaUdaleniya = self.listbox.get(ACTIVE)
		i=0
		while True:
			if ImyaUdaleniya == self.familiyaL[i] + " " + self.nameL[i] + " " + self.otchestvoL[i]:
				break
			else:
				i+=1
		self.familiyaL.pop(i);self.nameL.pop(i);self.otchestvoL.pop(i);self.nomerL.pop(i);self.emailL.pop(i);self.infoL.pop(i)
		self.entPhoneMain.delete(0,END)
		self.entEmailMain.delete(0,END)
		self.entKontachMain.delete(1.0,END)
		self.obnovlenie(1)
		print("Контакт удалён")
	
	def DobavitiKont(self): #Непосредственно добавляет в список
		Familiya=self.entFam.get();	Name=self.entName.get();	Otchestvo=self.entOtch.get(); Email=self.entEmail.get(); Telefon=self.entPhone.get(); OKontakt=self.entKontach.get()
		if len(Familiya)==0:
			Familiya="Пусто"
		if len(Name)==0:
			Name="Пусто"
		if len(Otchestvo)==0:
			Otchestvo="Пусто"
		if len(Email)==0:
			Email="Пусто"
		if len(Telefon)==0:
			Telefon="Пусто"
		if len(OKontakt)==0:
			OKontakt="Пусто"
		self.familiyaL.append(Familiya);self.nameL.append(Name);self.otchestvoL.append(Otchestvo);self.nomerL.append(Telefon);self.emailL.append(Email);self.infoL.append(OKontakt)
		self.obnovlenie(1)
		self.ramk.destroy()
		print("Контакт добавлен")
	
	def Sohranenie(self): #Сохранение
		self.fsave = open("AdressBook.txt","wb")
		self.SaveType1=[self.familiyaL,self.nameL,self.otchestvoL,self.nomerL,self.emailL,self.infoL]
		pickle.dump(self.SaveType1,self.fsave)
		self.fsave.close()
		print("Список сохранён")
		
AB = AdresBook()
