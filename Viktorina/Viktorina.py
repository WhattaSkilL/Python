from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os, random

class Viktorina():
	def __init__(self): #Конструктор
		# Создание окна
		self.root = Tk()
		self.root.minsize(width=800,height=640)
		self.root.maxsize(width=800,height=640)
		self.root.title("Викторина!")
		#Загрузка изображения
		self.ph_im = PhotoImage(file='BG.gif')
		self.VsegoOtvecheno=0
		self.PravilnoOtvecheno=0
		self.SpisokVoprosov=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49]
		#Создание заднего фона
		self.MainramkCanv = Canvas(self.root,width=800, height=640, highlightthickness=0)
		self.MainramkCanv.place(x=0,y=0)
		self.MainramkCanv.create_image(0,0,anchor=NW,image=self.ph_im)
		#Создание текстового поля и кнопок
		self.Quest = Text(self.root, wrap=WORD)
		self.Quest.place(x=109,y=69,width=580,height=280)
		
		self.But1 = Button(self.root, text="Вариант 1", wraplength=100, anchor=W, justify=LEFT, padx=3)
		self.But1.place(x=171,y=368,width=180,height=42)
		self.But1.bind("<Button-1>", lambda e: self.Otvet(1))
		
		self.But2 = Button(self.root, text="Вариант 2", wraplength=100, anchor=W, justify=LEFT, padx=3)
		self.But2.place(x=447,y=368,width=180,height=42)
		self.But2.bind("<Button-1>", lambda e: self.Otvet(2))
		
		self.But3 = Button(self.root, text="Вариант 3", wraplength=100, anchor=W, justify=LEFT, padx=3)
		self.But3.place(x=171,y=441,width=180,height=42)
		self.But3.bind("<Button-1>", lambda e: self.Otvet(3))
		
		self.But4 = Button(self.root, text="Вариант 4", wraplength=100, anchor=W, justify=LEFT, padx=3)
		self.But4.place(x=447,y=441,width=180,height=42)
		self.But4.bind("<Button-1>", lambda e: self.Otvet(4))
		
		self.KolOtvetovCanv= Canvas(self.root,width=180, height=42, highlightthickness=0)
		self.KolOtvetovCanv.place(x=309,y=528)
		self.textforOtveti=str(self.PravilnoOtvecheno) + " \ " + str(self.VsegoOtvecheno)
		self.KolOtvetovCanv.create_text(90,22,anchor=CENTER,font=("Gabriola",20),text=self.textforOtveti)
		#Чтение файла с вопросами
		self.ListQuest=open('Questions.txt','r', encoding='utf8')
		self.StrokaListQuest=self.ListQuest.readlines()
	
	def QuestMake(self): #Создаватель вопросов и разместитель их по полям
		self.DlinaSpiska=len(self.SpisokVoprosov)-1
		self.Vopros=self.SpisokVoprosov.pop(random.randint(0,self.DlinaSpiska))
		print(self.Vopros)
		self.strokalista=self.StrokaListQuest[self.Vopros*5].strip()
		self.TempQuest=self.strokalista[6:]
		self.NRList=[]
		self.RightAnswer="None"
		i=0
		while True:
			print("тута")
			i+=1
			self.strokalista=self.StrokaListQuest[self.Vopros*5+i].strip()
			if self.strokalista[:4]=="QEST":
				print("тута2")
				break
			if self.strokalista[:4]=="NRGT":
				print("тута3")
				self.NRList.append(self.strokalista[6:])
			if self.strokalista[:4]=="RGHT":
				self.RightAnswer=self.strokalista[6:]
		self.Quest.config(state="normal")
		self.Quest.delete(1.0,END)
		self.Quest.insert(END,self.TempQuest)
		self.Quest.config(state="disabled")
		self.NRList.append(self.RightAnswer)
		self.dlinaotvetov=len(self.NRList)-1
		self.Zapolnenie=self.NRList.pop(random.randint(0,self.dlinaotvetov))
		if self.Zapolnenie==self.RightAnswer:
			self.PravilniyOtvet=1
		self.But1.config(text=self.Zapolnenie)
		self.Zapolnenie=self.NRList.pop(random.randint(0,self.dlinaotvetov-1))
		if self.Zapolnenie==self.RightAnswer:
			self.PravilniyOtvet=2
		self.But2.config(text=self.Zapolnenie)
		self.Zapolnenie=self.NRList.pop(random.randint(0,self.dlinaotvetov-2))
		if self.Zapolnenie==self.RightAnswer:
			self.PravilniyOtvet=3
		self.But3.config(text=self.Zapolnenie)
		self.Zapolnenie=self.NRList.pop(0)
		if self.Zapolnenie==self.RightAnswer:
			self.PravilniyOtvet=4
		self.But4.config(text=self.Zapolnenie)
		
	def Otvet(self, x): #Проверка нажатой кнопки и сверение с ответом
		if x==self.PravilniyOtvet:
			print(self.SpisokVoprosov)
			print("Ура вы ответили верно")
			if self.VsegoOtvecheno < 10: #Ограничение по количеству вопросов
				try:
					self.QuestMake()
				except:
					None
				self.KolOtvetovCanv.delete('all')
				self.VsegoOtvecheno+=1
				self.PravilnoOtvecheno+=1
				self.textforOtveti=str(self.PravilnoOtvecheno) + " \ " + str(self.VsegoOtvecheno)
				self.KolOtvetovCanv.create_text(90,22,anchor=CENTER,font=("Gabriola",20),text=self.textforOtveti)
				if self.VsegoOtvecheno == 10: #Ограничение по количеству вопросов
					Result="Вопросы закончились! Ваш результат:" + self.textforOtveti
					messagebox.showinfo("Викторина!", Result)
			else:
				None
		else:
			print(self.SpisokVoprosov)
			print("Увы вы ошиблись")
			if self.VsegoOtvecheno < 10: #Ограничение по количеству вопросов
				try:
					self.QuestMake()
				except:
					None
				self.KolOtvetovCanv.delete('all')
				self.VsegoOtvecheno+=1
				self.textforOtveti=str(self.PravilnoOtvecheno) + " \ " + str(self.VsegoOtvecheno)
				self.KolOtvetovCanv.create_text(90,22,anchor=CENTER,font=("Gabriola",20),text=self.textforOtveti)
				if self.VsegoOtvecheno == 10: #Ограничение по количеству вопросов
					Result="Вопросы закончились! Ваш результат:" + self.textforOtveti
					messagebox.showinfo("Викторина!", Result)
			else:
				None
			
vk = Viktorina()
vk.QuestMake()