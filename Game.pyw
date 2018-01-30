from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image,ImageTk
import random,pickle,os,pygame,time,Pmw,shutil,threading

class GameMain():
	#Движок
	def __init__(self):
		self.n=0
		self.DelayCommand=1
		self.root = Tk()
		self.root.minsize(width=1280,height=720)
		self.root.maxsize(width=1280,height=720)
		self.root.title("Darkest Days")

		self.balPRuka = Pmw.Balloon(self.root,initwait=1,relmouse="both")
		self.balLRuka = Pmw.Balloon(self.root,initwait=1,relmouse="both")
		self.balRuki = Pmw.Balloon(self.root,initwait=1,relmouse="both")
		self.balGolova = Pmw.Balloon(self.root,initwait=1,relmouse="both")
		self.balTors = Pmw.Balloon(self.root,initwait=1,relmouse="both")
		self.balNogi = Pmw.Balloon(self.root,initwait=1,relmouse="both")

		self.balpruka="Пусто"
		self.ballruka="Пусто"
		self.balruki="Пусто"
		self.balgolova="Пусто"
		self.baltors="Пусто"
		self.balnogi="Пусто"

		self.GUI_im =ImageTk.PhotoImage(Image.open('Data\img\GUI\GUInew.png'))
		self.canv111 = Canvas(self.root, width=1282, height=722, highlightthickness=0)
		self.canv111.create_image(0,0,anchor=NW,image=self.GUI_im)
		self.canv111.place(x=-2,y=-2)

		self.m = Menu(self.root) #создается объект Меню на главном окне
		self.root.config(menu=self.m) #окно конфигурируется с указанием меню для него

		self.fm = Menu(self.m, tearoff=0) #создается пункт меню с размещением на основном меню (m)
		self.m.add_cascade(label="Меню",menu=self.fm) #пункту располагается на основном меню (m)
		self.fm.add_command(label="Новая игра",command=self.new_game)
		self.fm.add_command(label="Загрузить",command=self.load)
		self.fm.add_command(label="Выход",command=self.quitgame)

		self.hm = Menu(self.m, tearoff=0) #второй пункт меню
		self.m.add_cascade(label="Персонаж",menu=self.hm,state="disabled")
		self.hm.add_command(label="Инвентарь",command=self.inventar)
		self.hm.add_command(label="Развитие",command=self.prokachka)

		self.opm=Menu(self.m, tearoff=0)
		self.m.add_cascade(label="Настройки",menu=self.opm)
		self.opm.add_command(label="Музыка: Вкл",command=self.Music)
		self.opm.add_command(label="Звуки: Вкл",command=self.Sounds)

		self.om = Menu(self.m, tearoff=0)
		self.m.add_cascade(label="О программе",menu=self.om)
		self.om.add_command(label="Интерфейс",command=self.Interface)
		self.om.add_command(label="Список изменений",command=self.PathNote)
		self.om.add_command(label="Авторы",command=self.Autors)

		#Загрузка картинок
		self.HaracIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\Haract.png")) #Прокачка персонажа----Окно Характеристик
		self.PlusIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\Plus.png")) #Прокачка персонажа----Плюсик
		self.AbilityIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\ActivAbil.png")) #Прокачка персонажа----Активные способности
		self.AbilityPassIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\PassAbil.png")) #Прокачка персонажа----Пассивные способности
		self.battlegroundIMG=ImageTk.PhotoImage(Image.open("Data\img\Battle\BattleGround.png")) #Бой----Поле боя
		self.HeroIMG=ImageTk.PhotoImage(Image.open("Data\img\Battle\Hero.png")) #Бой----Иконка героя на ПБ
		self.EnemyiconIMG=ImageTk.PhotoImage(Image.open("Data\img\Battle\Hero.png")) #Бой----Иконка врага на ПБ
		self.YESIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\Yes.png")) #Прокачка персонажа----Пассивные умения
		self.NOIMG=ImageTk.PhotoImage(Image.open("Data\\img\\Prokachka\\No.png")) #Прокачка персонажа----Активные умения
		self.BGTEXT=ImageTk.PhotoImage(Image.open("Data\\img\\BackGroundText.jpg")) #Прокачка персонажа----Активные умения

		#Рамка для картинки
		self.ramk = Frame(self.root,bd=0,bg="Blue")
		self.ramk.place(x=0,y=19,width=1282,height=321)
		
		#Статус поле
		self.statust = Text(self.root,width=20,height=3,font="Gabriola", wrap=WORD)
		self.statust.place(x=1013,y=360,width=246,height=285)

		self.root.bind("<Motion>", self.getXY)
		self.statust.bind("<Enter>", lambda e: self.Buble("Enter"))
		self.statust.bind("<Leave>", lambda e: self.Buble("Destro"))
		self.statust.bind("<Motion>", lambda e: self.Buble("Inside"))

		#Поле с текстом
		self.tex = Text(self.root,width=20,height=3,font="Gabriola", wrap=WORD, spacing2=0)
		self.tex.place(x=19,y=360,width=477,height=285)

		#Поле действий
		self.CSSt = Text(self.root,width=20,height=3,font="Gabriola",wrap=WORD)
		self.CSSt.place(x=516,y=360,width=477,height=285)

		#Картинка действия
		self.ph_im =ImageTk.PhotoImage(Image.open('Data\img\MainMenu.png'))
		self.canv111 = Canvas(self.ramk,width=1282, height=321, highlightthickness=0)
		self.canv111.create_image(0,0,anchor=NW,image=self.ph_im)
		self.canv111.place(x=0,y=0)

		#Кнопка
		self.but = Button(self.root,text="Enter")
		self.but.place(x=921,y=659,width=73,height=27)
		self.but.bind("<Button-1>",lambda e: self.Game(None) if self.DelayCommand==1 else None)

		#Поле ввода
		self.ent = Entry(self.root,width=1)
		self.ent.place(x=19,y=659,width=881,height=27)
		self.ent.bind("<Return>",lambda e: self.Game(None) if self.DelayCommand==1 else None)

		#Кнопка инвентаря
		self.KnopkaInvent_im=ImageTk.PhotoImage(Image.open('Data\img\GUI\ButnInvent.png'))
		self.KnopkaInventCanv = Canvas(self.root, width=62, height=27, highlightthickness=0)
		self.KnopkaInventCanv.create_image(0,0,anchor=NW,image=self.KnopkaInvent_im)
		self.KnopkaInventCanv.place(x=1028,y=659)
		Pmw.Balloon(self.root,initwait=1,relmouse="both").bind(self.KnopkaInventCanv,"Инвентарь")
		self.KnopkaInventCanv.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,1))

		#Кнопка прокачки
		self.KnopkaProkach_im=ImageTk.PhotoImage(Image.open('Data\img\GUI\Butnprokach.png'))
		self.KnopkaProkachCanv = Canvas(self.root, width=62, height=27, highlightthickness=0)
		self.KnopkaProkachCanv.create_image(0,0,anchor=NW,image=self.KnopkaProkach_im)
		self.KnopkaProkachCanv.place(x=1105,y=659)
		Pmw.Balloon(self.root,initwait=1,relmouse="both").bind(self.KnopkaProkachCanv,"Развитие")
		self.KnopkaProkachCanv.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,2))

		#Музыка
		self.Musicplay=0
		pygame.mixer.pre_init(44100, -16, 2, 4096)
		pygame.init()
		pygame.display.init()

		self.playlist=["Data\\Music\\Music3.mp3","Data\\Music\\Music2.mp3","Data\\Music\\Music1.mp3"]

		pygame.mixer.music.load (self.playlist.pop())
		pygame.mixer.music.play()
		pygame.mixer.music.set_endevent(pygame.USEREVENT) 
		pygame.mixer.music.set_volume(0.1)

		threading.Thread(target = self.PlayList).start()

		#Клики
		self.sounds=1
		self.click = pygame.mixer.Sound('Data\\sounds\\click.wav')
		self.click.set_volume(0.2)

		self.root.iconbitmap('Data\\img\\GUI\\icon.ico')
		self.root.mainloop()

	def newprintCSSt(self, x): #Редактирование текста в окне выбора
		self.CSSt.config(state="normal")
		self.CSSt.delete(1.0,END)
		self.CSSt.insert(END,x)
		self.CSSt.config(state="disabled")

	def newprinttex(self, x): #Редактирование текста в окне информации
		self.tex.config(state="normal")
		self.tex.delete(1.0,END)
		self.tex.insert(END,x)
		if self.func=="Бой":
			self.tex.yview('end')
		self.tex.config(state="disabled")

	def newprintstat(self, x): #Редактирование статистики
		self.statust.config(state="normal")
		self.statust.delete(1.0,END)
		self.statust.insert(END,x)
		self.statust.config(state="disabled")	
	
	def otchistiti(self):
		try:
			self.Tors.destroy()
			self.Golova.destroy()
			self.Ruki.destroy()
			self.Pruka.destroy()
			self.Lruka.destroy()
			self.Nogi.destroy()
		except:
			None
		try:
			self.AbilityIMGCanv.destroy()
			self.HaracIMGCanv.destroy()
			self.PlusSTR.destroy()
			self.PlusAGL.destroy()
			self.PlusMND.destroy()
			self.PlusHLT.destroy()
			self.STRtextCanv.destroy()
			self.AGLtextCanv.destroy()
			self.MNDtextCanv.destroy()
			self.HLTtextCanv.destroy()
			self.PNTtextCanv.destroy()
			self.SPPtextCanv.destroy()
			self.SAPtextCanv.destroy()
		except:
			None
		try:
			self.EnemyImageCanv.destroy()			
			self.battlegroundIMGCanv.destroy()
			self.HeroIMGCanv.destroy()
			self.EnemyiconIMGCanv.destroy()
		except:
			None
	
	def PlayList(self): # ----------------------------------------------------------ПРОИГРЫВАТЕЛЬ
		while True:
			time.sleep(0.5)
			if self.Musicplay==1:
				for event in pygame.event.get():
					if event.type == pygame.USEREVENT:
						if len(self.playlist) > 0:
							pygame.mixer.music.load (self.playlist.pop())
							pygame.mixer.music.play()
						elif len(self.playlist) == 0:
							self.playlist=["Data\\Music\\Music3.mp3","Data\\Music\\Music2.mp3","Data\\Music\\Music1.mp3"]	
							pygame.mixer.music.load (self.playlist.pop())
							pygame.mixer.music.play()
			elif self.Musicplay==0:
				None
			if self.DelayCommand==1:
				None
			elif self.DelayCommand<1:
				self.DelayCommand+=1

	def load(self):
		if self.sounds==1:
			self.clicking()
		
		self.op = askopenfilename(filetypes=[('Файлы сохранения', '*.save')])
		self.fsave1=open(self.op,'rb')
		self.loadtype=pickle.load(self.fsave1); self.part=int(self.loadtype[0]); self.path=int(self.loadtype[1]); self.S=int(self.loadtype[2])
		self.M=int(self.loadtype[3]); self.A=int(self.loadtype[4]);self.H=int(self.loadtype[5]); self.P=int(self.loadtype[6]); self.SP=int(self.loadtype[7]); self.SAP=int(self.loadtype[8]); self.lvl=int(self.loadtype[9])
		self.exp=int(self.loadtype[10]); self.expup=int(self.loadtype[11]); self.Equipment=self.loadtype[12]; self.invent=self.loadtype[13]; self.inventID=self.loadtype[14]; self.classname=self.loadtype[15]
		self.meshok=self.loadtype[16]; self.meshokID=self.loadtype[17]; self.weapon=self.loadtype[18]; self.HP=self.loadtype[19]; self.MP=self.loadtype[20]; self.S0=self.loadtype[21]; self.SA0=self.loadtype[22]; self.SID=self.loadtype[23]
		self.SAID=self.loadtype[24]; self.AS=self.loadtype[25]; self.AM=self.loadtype[26]; self.AH=self.loadtype[27]; self.AA=self.loadtype[28]; self.name=self.loadtype[29]; self.atk=self.loadtype[30]; self.FireRes=self.loadtype[31]
		self.WaterRes=self.loadtype[32]; self.EarthRes=self.loadtype[33]; self.AirRes=self.loadtype[34];self.PhisRes=self.loadtype[35];self.BleedRes=self.loadtype[36];self.PoisRes=self.loadtype[37];self.locat1=self.loadtype[38]
		self.CurrentLocation=self.loadtype[39]; self.Hour=self.loadtype[40]; self.Minutes=self.loadtype[41];self.Days=self.loadtype[42];self.Months=self.loadtype[43];self.Years=self.loadtype[44];self.Weather=self.loadtype[45]
		self.Block=self.loadtype[46]; self.Dodge=self.loadtype[47]; self.locatCur=self.loadtype[48];self.locatDisc=self.loadtype[49];self.locatCSS=self.loadtype[50];self.FHP=self.loadtype[51];self.FMP=self.loadtype[52];self.locatImg=self.loadtype[53]
		self.Inventimg=self.loadtype[54]; self.balpruka=self.loadtype[55]; self.ballruka=self.loadtype[56];self.balruki=self.loadtype[57];self.balgolova=self.loadtype[58];self.baltors=self.loadtype[59];self.balnogi=self.loadtype[60]
		self.classimg=self.loadtype[61]; self.weaponw=self.loadtype[62]; self.id=self.loadtype[63];self.atkp=self.loadtype[64];self.MSTN=self.loadtype[65];self.LVLN=self.loadtype[66];self.MNMC=self.loadtype[67];self.MNMG=self.loadtype[68]
		self.TeloHP=self.loadtype[69]; self.ControllRes=self.loadtype[70]
		self.safy=1
		self.fsave1.close()
		self.func="Игра"
		self.textes="Игра была загружена\n\n"+self.locatDisc
		self.newprinttex(self.textes)
		self.newprintCSSt(self.locatCSS)
		self.images(self.locatImg)
		self.stats="Локация: "+ self.locatCur +"\nЗдоровье: " + str(self.HP) + "/" + str(self.FHP) + "\nРесурс: " + str(self.MP) +"/"+str(self.FMP)
		self.newprintstat(self.stats)
		self.init=0
		self.otchistiti()
		if self.part>0 and self.init==0:
			self.init=1
			self.m.entryconfig('Персонаж',state="normal")
			self.fm.delete(0,4)
			self.fm.add_command(label="Продолжить",command=self.prodoljit) #формируется список команд пункта меню
			self.fm.add_command(label="Новая игра",command=self.new_game)
			self.fm.add_command(label="Сохранить",command=self.save)
			self.fm.add_command(label="Загрузить",command=self.load)
			self.fm.add_command(label="Выход",command=self.quitgame)

		self.FS=self.S+self.AS[0]; self.FM=self.M+self.AM[0]; self.FA=self.A+self.AA[0]; self.FH=self.H+self.AH[0]; self.FHP=self.FH*5; self.FMP=self.FM*5
		if self.weapon=="power":
			self.uron=round((self.atk[0]+self.atkp)*(self.FS*0.08+self.FA*0.06+self.FM*0.04))
		elif self.weapon=="agility":
			self.uron=round((self.atk[0]+self.atkp)*(self.FA*0.08+self.FM*0.06+self.FS*0.04))
		elif self.weapon=="magic":
			self.uron=round((self.atk[0]+self.atkp)*(self.FM*0.08+self.FS*0.06+self.FA*0.04))	
			
		self.namesave=os.path.basename(self.op)
		self.nazvanW='Save/'+self.namesave[:-4]+'/WeaArmList.data'
		shutil.copy(self.nazvanW,r'Data/WeaArmListtime.data')
	
	def save(self):
		if self.sounds==1:
			self.clicking()
		if self.func=="Бой":
			self.newprinttex("Нельзя сохранятся во время боя")
		else:
			self.sa = asksaveasfilename(filetypes=[('Файлы сохранения', '*.save')],defaultextension=".save")
			self.fsave = open(self.sa,"wb")
			self.SaveType1=[self.part,self.path,self.S,self.M,self.A,self.H,self.P,self.SP,self.SAP,self.lvl,self.exp,self.expup,self.Equipment,self.invent,self.inventID,self.classname,self.meshok,self.meshokID,self.weapon,self.HP,self.MP,self.S0,self.SA0,self.SID,self.SAID,self.AS,self.AM,self.AH,self.AA,self.name,self.atk,self.FireRes,self.WaterRes,self.EarthRes,self.AirRes,self.PhisRes,self.BleedRes,self.PoisRes,self.locat1,self.CurrentLocation,self.Hour,self.Minutes,self.Days,self.Months,self.Years,self.Weather,self.Block,self.Dodge,self.locatCur,self.locatDisc,self.locatCSS,self.FHP,self.FMP,self.locatImg,self.Inventimg,self.balpruka,self.ballruka,self.balruki,self.balgolova,self.baltors,self.balnogi,self.classimg,self.weaponw,self.id,self.atkp,self.MSTN,self.LVLN,self.MNMC,self.MNMG,self.TeloHP,self.ControllRes]
			pickle.dump(self.SaveType1,self.fsave)
			self.fsave.close()
			self.namesave=os.path.basename(self.sa)
			self.nazvanW='Save/'+self.namesave[:-4]+'/WeaArmList.data'
			self.nazvanP="Save/"+self.namesave[:-4]
			try:
				os.mkdir(self.nazvanP)
			except:
				None
			shutil.copy(r'Data/WeaArmListtime.data', self.nazvanW)

	def quitgame(self):
		if self.sounds==1:
			self.clicking()
		if askyesno("Выход", "Вы уверены что хотите выйти?"):
			self.root.destroy()
	
	def drop(self, shmotki): #Выпадение предметов
		self.textes=""
		while shmotki>0:
			Itemname=0;ItemID=0;ItemType=0;ItemAtack=0;ItemAtackType=0;ItemNeedMast=0;ItemNeedLvl=0;Itemimg="Data\\img\\Inventar\\BulavaNB.png"
			ItemToss=0;ItemStun=0;ItemSile=0;Itemname5=0;ItemWpLs=0;ItemBlnd=0;ItemPhis=0;ItemFire=0;ItemWatr=0;ItemEart=0;ItemBled=0;ItemPois=0;ItemCtrl=0
			ItemBlck=0;ItemDodg=0;ItemPower=0;ItemMind=0;ItemAgility=0;ItemHealth=0;ItemMnMg=0;ItemMnMc=0;ItemWind=0
			
			ItemAtackPR=0
			ItemPhisPR=0;ItemFirePR=0;ItemWatrPR=0;ItemEartPR=0;ItemBledPR=0;ItemPoisPR=0;ItemCtrlPR=0
			ItemBlckPR=0;ItemDodgPR=0;ItemPowerPR=0;ItemMindPR=0;ItemAgilityPR=0;ItemHealthPR=0;ItemMnMgPR=0;ItemMnMcPR=0;ItemWindPR=0
			
			KolHar=0
			self.id+=1
			shmotki-=1
			procent=random.randint(0,100)
			tipecip=random.randint(1,4)
			WeaArmList=open('Data/WeaArmListtime.data','a+', encoding='utf8')
			if self.lvl<5: #Уровни
				ItemNeedLvl=random.randint(1,self.lvl)
			else:
				ItemNeedLvl=random.randint(self.lvl-3,self.lvl)
			mesto=random.choice(["тело","голова","ноги","руки","лрука"]) #Определяет букву в self.id
			typeB=random.choice(["лёгкий","средний","тяжёлый"]) #Определяет уровень тяжести
			typeL=random.choice(["баклер ","щит ","башенный щит "]) #Определяет уровень тяжести
			typeTM=random.choice(["доспех ","нагрудник ","мундир "]) #Название торса
			typeTW=random.choice(["кираса ","бригантина ","броня "]) #Название торса
			typeRA=random.choice(["рукавицы ","перчатки ","наручи "]) #Название рук
			typeSM=random.choice(["шлем ","шишак ","топфхелм "]) #Название шлема
			typeNA=random.choice(["сапоги ", "ботфорты ", "ботинки "]) #Название ботинки
			typeClass=random.choice(["вор","маг","воин"]) #Название типа основной характеристики
			if procent>98: #Мифические
				if tipecip==1:
					if random.randint(1,2)==1:
						name=random.choice(["Мифический ","Уничтоженный ","Последний ","Чёрный ","Бессмертный ","Древний ","Святой ","Величавый ","Проклятый "])
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
					else:
						name=random.choice(["Мифическая ","Уничтоженная ","Последняя ","Чёрная ","Бессмертная ","Древняя ","Святая ","Величавая ","Проклятая "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:		
					prilagM=random.choice(["Пепельный ","Пламенный ","Тёмный ","Мифический ","Священный ","Древний ","Проклятый "]) #Прилагательные начала
					prilagW=random.choice(["Пепельная ","Пламенная ","Тёмная ","Мифическая ","Священная ","Древняя ","Проклятая "]) #Прилагательные начала
					prilagA=random.choice(["Пепельные ","Пламенные ","Тёмные ","Мифические ","Священные ","Древние ","Проклятые "]) #Прилагательные начала
				KolHar=6
				ItemRANG=15
				ItemID="F"
				ItemNeedMast="2"
				if ItemNeedLvl<5:
					ItemNeedLvl+=7
			elif procent>92: #Легендарные
				if tipecip==1:
					if random.randint(1,2)==1:
						name=random.choice(["Легендарный ","Уничтоженный ","Последний ","Чёрный ","Бессмертный ","Древний ","Святой ","Величавый ","Проклятый "])
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
					else:
						name=random.choice(["Легендарная ","Уничтоженная ","Последняя ","Чёрная ","Бессмертная ","Древняя ","Святая ","Величавая ","Проклятая "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:
					prilagM=random.choice(["Пепельный ","Пламенный ","Тёмный ","Легендарный ","Священный ","Древний ","Проклятый "]) #Прилагательные начала
					prilagW=random.choice(["Пепельная ","Пламенная ","Тёмная ","Легендарная ","Священная ","Древняя ","Проклятая "]) #Прилагательные начала
					prilagA=random.choice(["Пепельные ","Пламенные ","Тёмные ","Легендарные ","Священные ","Древние ","Проклятые "]) #Прилагательные начала
				KolHar=5
				ItemRANG=12
				ItemID="L"
				ItemNeedMast="2"
				if ItemNeedLvl<5:
					ItemNeedLvl+=5
			elif procent>84: #Редкие
				if tipecip==1:
					if random.randint(1,2)==1:
						name=random.choice(["Редкий ","Отличный ","Метеоритный ","Особенный ","Драконий ","Смертоносный "])
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
					else:
						name=random.choice(["Редкая ","Отличная ","Метеоритная ","Особенная ","Драконяя ","Смертоносная "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:	
					prilagM=random.choice(["Редкий ","Особенный ","Странный ","Уникальный ","Великолепный "]) #Прилагательные начала
					prilagW=random.choice(["Редкая ","Особенная ","Странная ","Уникальная ","Великолепная "]) #Прилагательные начала
					prilagA=random.choice(["Редкие ","Особенные ","Странные ","Уникальные ","Великолепные "]) #Прилагательные начала
				KolHar=4
				ItemRANG=9
				ItemID="R"
				ItemNeedMast="1"
				if ItemNeedLvl<5:
					ItemNeedLvl+=3
			elif procent>70: #Магические
				if tipecip==1:
					if random.randint(1,2)==1:
						name=random.choice(["Закалённый ","Волшебный ","Магический ","Необычный ","Хороший ","Платиновый "])
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
					else:
						name=random.choice(["Закалённая ","Волшебная ","Магическая ","Необычная ","Хорошая ","Платиновая "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:	
					prilagM=random.choice(["Магический ","Волшебный ","Удивительный ","Необыкновенный "]) #Прилагательные начала
					prilagW=random.choice(["Магическая ","Волшебная ","Удивительная ","Необыкновенная "]) #Прилагательные начала
					prilagA=random.choice(["Магические ","Волшебные ","Удивительные ","Необыкновенные "]) #Прилагательные начала
				KolHar=3
				ItemRANG=6
				ItemID="M"
				ItemNeedMast="1"
			elif procent>40: #Нормальные
				if tipecip==1:
					if random.randint(0,1)==1:
						name=random.choice(["Обычный ","Железный ","Стальной ","Простой ","Наточенный ","Заострённый "])
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
					else:
						name=random.choice(["Обычная ","Железная ","Стальная ","Простая ","Наточенная ","Заострённая "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:		
					prilagM=random.choice(["Обычный ","Простой ","Качественый ","Железный ","Стальной "]) #Прилагательные начала
					prilagW=random.choice(["Обычная ","Простая ","Качественая ","Железная ","Стальная "]) #Прилагательные начала
					prilagA=random.choice(["Обычные ","Простые ","Качественые ","Железные ","Стальные "]) #Прилагательные начала
				KolHar=3
				ItemRANG=3
				ItemID="N"
				ItemNeedMast="0"
			else: #Плохо
				if tipecip==1:
					if random.randint(0,1)==1:
						type=random.choice(["одноручный меч","одноручный топор","скипетр","кинжал","двуручный меч","двуручный топор","боевой посох"])
						name=random.choice(["Деревянный ","Трестнутый ","Сломаный ","Ржавый ","Плохой ","Старый ","Тупой "])
					else:
						name=random.choice(["Деревянная ","Трестнутая ","Сломаная ","Ржавая ","Плохая ","Старая "])
						type=random.choice(["одноручная булава","катана","двуручная булава"])
				else:	
					prilagM=random.choice(["Плохой ","Некачественный ","Потрёпаный ","Изношеный ","Треснутый "]) #Прилагательные начала
					prilagW=random.choice(["Плохая ","Некачественная ","Потрёпаная ","Изношеная ","Треснутая "]) #Прилагательные начала
					prilagA=random.choice(["Плохие ","Некачественные ","Потрёпаные ","Изношеные ","Треснутые "]) #Прилагательные начала
				KolHar=3
				ItemRANG=1
				ItemID="B"
				ItemNeedMast="0"
			if tipecip==1:
				name+=type
				if ItemID=="F" or ItemID=="L":
					name+=random.choice([" забытого короля"," подземных глубин"," однорукого карлика"," повелителя мёртвых"," последнего героя"," лорда вайтрана"," из утерянного склепа"," далёких песков"," смертельных ветров"])
				Itemname=name
				ItemID+="WP"+str(self.id)
				if type=="одноручный меч":
					ItemType="Одноручный меч"
					ItemPower=round((random.randint(2,5)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Сила
					ItemHealth=round((random.randint(1,4)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Здоровье
					ItemAtack=round((random.randint(5,10)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Атака
					ItemAtackType="power"
					if random.randint(1,100)>50:
						if random.randint(1,100)>90:
							ItemMind=round((random.randint(0,2)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Разум
							ItemAgility=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Ловкость
						elif random.randint(1,100)>45:
							ItemMind=round((random.randint(0,2)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Разум
						else:
							ItemAgility=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Ловкость
				elif type=="одноручный топор":
					ItemType="Одноручный топор"
					ItemAtack=round((random.randint(6,11)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Атака
					ItemPower=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Сила
					ItemMind=0
					ItemAgility=round((random.randint(1,3)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Ловкость
					ItemHealth=round((random.randint(2,5)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Здоровье
					ItemAtackType="power"
				elif type=="скипетр":
					ItemType="Скипетр"
					ItemAtack=round((random.randint(7,12)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Атака
					ItemPower=0
					ItemMind=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Разум
					ItemAgility=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Ловкость
					ItemHealth=round((random.randint(1,3)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Здоровье
					ItemAtackType="magic"
				elif type=="кинжал":
					ItemType="Кинжал"
					ItemAtack=round((random.randint(10,15)+ItemRANG)*(0.5+ItemNeedLvl/10)) #Атака
					ItemPower=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=0
					ItemAgility=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="agility"
				elif type=="двуручный меч":
					ItemType="Двуручный меч"
					ItemAtack=round((random.randint(13,18)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(4,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=0
					ItemAgility=round((random.randint(0,5)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(2,7)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="power"
				elif type=="двуручный топор":
					ItemType="Двуручный топор"
					ItemAtack=round((random.randint(14,19)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(4,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=0
					ItemAgility=round((random.randint(0,5)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(2,7)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="power"
				elif type=="боевой посох":
					ItemType="Боевой посох"
					ItemAtack=round((random.randint(13,18)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=round((random.randint(3,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAgility=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="magic"
				elif type=="одноручная булава":
					ItemType="Одноручная булава"
					ItemAtack=round((random.randint(7,12)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(2,5)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=round((random.randint(0,2)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAgility=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(1,4)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="power"
				elif type=="двуручная булава":
					ItemType="Двуручная булава"
					ItemAtack=round((random.randint(13,18)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(4,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=0
					ItemAgility=round((random.randint(1,2)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(4,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="power"
				elif type=="катана":
					Itemimg="Data/img/Inventar/KatanaNB.png"
					ItemType="Катана"
					ItemAtack=round((random.randint(13,18)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemPower=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemMind=0
					ItemAgility=round((random.randint(4,9)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemHealth=round((random.randint(0,3)+ItemRANG)*(0.5+ItemNeedLvl/10))
					ItemAtackType="agility"
			else:
				if mesto=="тело": #Line 1 and Line 2
					if random.randint(1,2)==1:
						Itemname=prilagM+typeTM
					else:
						Itemname=prilagW+typeTW
					TypeMnog=1.5
				elif mesto=="голова":
					Itemname=prilagM+typeSM
					TypeMnog=1.2
				elif mesto=="ноги":
					Itemname=prilagA+typeNA
					TypeMnog=1
				elif mesto=="руки":
					Itemname=prilagA+typeRA
					TypeMnog=1
				elif mesto=="лрука":
					Itemname=prilagM+typeL
					TypeMnog=1
				if mesto=="тело" or mesto=="голова" or mesto=="ноги" or mesto=="руки": #Line 3
					if typeB=="лёгкий":
						ItemType="Лёгкая броня"
						TypeMnog+=0.8
					elif typeB=="средний":
						ItemType="Средняя броня"
						TypeMnog+=1
					elif typeB=="тяжёлый":
						ItemType="Тяжёлая броня"
						TypeMnog+=1.2
				elif mesto=="лрука": #Line 3
					if typeL=="баклер ":
						ItemType="Баклер"
						TypeMnog+=0.8
					elif typeL=="щит ":
						ItemType="Щит"
						TypeMnog+=1
					elif typeL=="башенный щит ":
						ItemType="Башенный щит"
						TypeMnog+=1.2
				if ItemID=="F" or ItemID=="L":
					Itemname+=random.choice(["забытых богов","дыхания смерти","архиепископа","тёмного рыцаря","похитителя жизни","брошеного героя"])
				ItemID+="A"
				if mesto=="тело": #Line 1 and Line 2
					ItemID+="T"+str(self.id)
				elif mesto=="голова":
					ItemID+="G"+str(self.id)
				elif mesto=="ноги":
					ItemID+="N"+str(self.id)
				elif mesto=="руки":
					ItemID+="R"+str(self.id)
				elif mesto=="лрука":
					ItemID+="L"+str(self.id)
				if self.lvl<5: #Line 25
					ItemNeedLvl=random.randint(1,self.lvl+3)
				else:
					ItemNeedLvl=random.randint(self.lvl-3,self.lvl+3)
				ItemPhis=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog)) #Физическая защита +
				ItemFire=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Огненная защита +
				ItemWatr=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Водяная защита +
				ItemEart=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Защита от земли +
				ItemWind=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Защита от воздуха +
				ItemBled=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Защита от кровотечения +
				ItemPois=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Защита от яда +
				ItemCtrl=round((random.randint(2,6)+ItemRANG)*(0.5+ItemNeedLvl/10*TypeMnog))  #Защита от страха +
				if mesto=="тело" or mesto=="голова" or mesto=="ноги" or mesto=="руки":
					if typeB=="лёгкий": 
						ItemBlck=0 
						ItemDodg=0
						ItemMnMg=round(random.randint(3,6)*ItemNeedLvl/10) #Множитель магии
						if ItemMnMg>6:
							ItemMnMg=6
						ItemMnMc=round(random.randint(-2,0)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc<-2:
							ItemMnMc=0
					elif typeB=="средний":
						ItemBlck=0
						ItemDodg=0  #Уворот
						ItemMnMg=0 #Множитель магии
						ItemMnMc=round(random.randint(16,19)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc>19:
							ItemMnMc=16
					elif typeB=="тяжёлый":
						ItemBlck=0  #Блок
						ItemDodg=0 
						ItemMnMg=round(random.randint(-13,-9)*ItemNeedLvl/10) #Множитель магии
						if ItemMnMg<-19:
							ItemMnMg=-9
						ItemMnMc=round(random.randint(24,27)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc>27:
							ItemMnMc=24
				elif mesto=="лрука":
					if typeL=="баклер ": 
						ItemBlck=0 
						ItemDodg=0
						ItemMnMg=round(random.randint(3,6)*ItemNeedLvl/10) #Множитель магии
						if ItemMnMg>6:
							ItemMnMg=6
						ItemMnMc=round(random.randint(-2,0)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc<-2:
							ItemMnMc=0
					elif typeL=="щит ":
						ItemBlck=0
						ItemDodg=0  #Уворот
						ItemMnMg=0 #Множитель магии
						ItemMnMc=round(random.randint(16,19)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc>19:
							ItemMnMc=16
					elif typeL=="башенный щит ":
						ItemBlck=0  #Блок
						ItemDodg=0 
						ItemMnMg=round(random.randint(-13,-9)*ItemNeedLvl/10) #Множитель магии
						if ItemMnMg<-19:
							ItemMnMg=-9
						ItemMnMc=round(random.randint(24,27)*ItemNeedLvl/10) #Множитель Манакосты
						if ItemMnMc>27:
							ItemMnMc=24
				ItemPower=round(random.randint(0,2)*ItemNeedLvl/10) #Сила
				ItemMind=round(random.randint(0,2)*ItemNeedLvl/10) #Разум
				ItemAgility=round(random.randint(0,2)*ItemNeedLvl/10) #Ловкость
				ItemHealth=round(random.randint(0,2)*ItemNeedLvl/10) #Здоровье
				if typeClass=="вор":
					ItemAgility+=round(random.randint(0,2)*ItemNeedLvl/10)
				elif typeClass=="маг":
					ItemMind+=round(random.randint(0,2)*ItemNeedLvl/10)
				elif typeClass=="воин":
					ItemPower+=round(random.randint(0,2)*ItemNeedLvl/10)
			"""Вывод характеристик"""
			self.meshok.append(Itemname)
			self.meshokID.append(ItemID)
			WeaArmList.write("ITID: " + ItemID + "\n")
			WeaArmList.write("NAME: " + Itemname + "\n")
			WeaArmList.write("IIMG: " + Itemimg + "\n")
			WeaArmList.write("ITTP: " + ItemType + "\n")
			WeaArmList.write("MSTN: " + str(ItemNeedMast) + "\n")
			WeaArmList.write("LVLN: " + str(ItemNeedLvl) + "\n")
			if tipecip==1:
				WeaArmList.write("ATTP: " + str(ItemAtackType) + "\n")
			if ItemPhis>0:
				WeaArmList.write("PHIS: " + str(ItemPhis) + "\n")
			if ItemAtack>0:
				WeaArmList.write("ATCK: " + str(ItemAtack) + "\n")
			haracteristiki=[2,3,4,5,6,7,8,15,16,17,18,19,20,21,22]
			while KolHar>0:
				napisano=0
				z=len(haracteristiki)-1
				if z==0:
					CSS=0
				else:
					CSS=random.randint(0,z)
				Haractr=haracteristiki.pop(CSS)
				if Haractr==2 and ItemFire>0 and ItemFirePR==0 and KolHar>0:
					napisano=1
					ItemFirePR=1
					WeaArmList.write("FIRE: " + str(ItemFire) + "\n")
				elif Haractr==3 and ItemWatr>0 and ItemWatrPR==0 and KolHar>0:
					napisano=1 
					ItemWatrPR=1
					WeaArmList.write("WATR: " + str(ItemWatr) + "\n")
				elif Haractr==4 and ItemEart>0 and ItemEartPR==0 and KolHar>0:
					napisano=1 
					ItemEartPR=1
					WeaArmList.write("EART: " + str(ItemEart) + "\n")
				elif Haractr==5 and ItemWind>0 and ItemWindPR==0 and KolHar>0:
					napisano=1 
					ItemWindPR=1
					WeaArmList.write("WIND: " + str(ItemWind) + "\n")
				elif Haractr==6 and ItemBled>0 and ItemBledPR==0 and KolHar>0:
					napisano=1 
					ItemBledPR=1
					WeaArmList.write("BLED: " + str(ItemBled) + "\n")
				elif Haractr==7 and ItemPois>0 and ItemPoisPR==0 and KolHar>0:
					napisano=1 
					ItemPoisPR=1
					WeaArmList.write("POIS: " + str(ItemPois) + "\n")
				elif Haractr==8 and ItemCtrl>0 and ItemCtrlPR==0 and KolHar>0:
					napisano=1 
					ItemCtrlPR=1
					WeaArmList.write("CTRL: " + str(ItemPois) + "\n")
				elif Haractr==15 and ItemBlck>0 and ItemBlckPR==0 and KolHar>0:
					napisano=1 
					ItemBlckPR=1
					WeaArmList.write("BLCK: " + str(ItemBlck) + "\n")
				elif Haractr==16 and ItemDodg>0 and ItemDodgPR==0 and KolHar>0:
					napisano=1 
					ItemDodgPR=1
					WeaArmList.write("DODG: " + str(ItemDodg) + "\n")
				elif Haractr==17 and ItemPower>0 and ItemPowerPR==0 and KolHar>0:
					napisano=1 
					ItemPowerPR=1
					WeaArmList.write("POWR: " + str(ItemPower) + "\n")
				elif Haractr==18 and ItemMind>0 and ItemMindPR==0 and KolHar>0:
					napisano=1 
					ItemMindPR=1
					WeaArmList.write("MIND: " + str(ItemMind) + "\n")
				elif Haractr==19 and ItemAgility>0 and ItemAgilityPR==0 and KolHar>0:
					napisano=1 
					ItemAgilityPR=1
					WeaArmList.write("AGIL: " + str(ItemAgility) + "\n")
				elif Haractr==20 and ItemHealth>0 and ItemHealthPR==0 and KolHar>0:
					napisano=1 
					ItemHealthPR=1
					WeaArmList.write("HELT: " + str(ItemHealth) + "\n")
				elif Haractr==21 and ItemMnMg>0 and ItemMnMgPR==0 and KolHar>0:
					napisano=1 
					ItemMnMgPR=1
					WeaArmList.write("MNMG: " + str(ItemMnMg) + "\n")
				elif Haractr==22 and ItemMnMc>0 and ItemMnMcPR==0 and KolHar>0:
					napisano=1 
					ItemMnMcPR=1
					WeaArmList.write("MNMC: " + str(ItemMnMc) + "\n")
				if napisano==1:
					KolHar-=1
				if len(haracteristiki)==0 or KolHar==0:
					break
			WeaArmList.write("STOP\n")
			if ItemID[:1]=="F":
				self.textes+="\nПОЗДРАВЛЯЮ ВЫ ПОЛУЧИЛИ САМЫЙ РЕДКИЙ ТИП СНАРЯЖЕНИЯ МИФИЧЕСКИЙ: "+Itemname
			elif ItemID[:1]=="L":
				self.textes +="\nПоздравляю вы получили легендарную вещь!: "+Itemname
			elif ItemID[:1]=="R":
				self.textes +="\nПоздравляю вы получили редкую вещь: "+Itemname
			elif ItemID[:1]=="M":
				self.textes +="\nВы получили магическую вещь: "+Itemname
			elif ItemID[:1]=="N" or ItemID[:1]=="B":
				self.textes +="\nВаша добыча: "+Itemname
			WeaArmList.close()
	
	def inventar(self):
		if self.sounds==1:
			self.clicking()
		try:
			if self.func=="Инвентарь":
				self.Tors.destroy()
				self.Golova.destroy()
				self.Ruki.destroy()
				self.Pruka.destroy()
				self.Lruka.destroy()
				self.Nogi.destroy()
		except:
			None
		if self.func=="Бой":
			self.newprinttex("Во время боя открывать инвентарь невозможно")
		else:
			self.Pruka = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.PrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[0]))
			self.Pruka.create_image(0,0,anchor=NW,image=self.PrukaimgOpened)
			self.Pruka.place(x=0,y=0)
			self.Lruka = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.LrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[1]))
			self.Lruka.create_image(0,0,anchor=NW,image=self.LrukaimgOpened)
			self.Lruka.place(x=152,y=0)
			self.Golova = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.GolovaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[2]))
			self.Golova.create_image(0,0,anchor=NW,image=self.GolovaimgOpened)
			self.Golova.place(x=304,y=0)
			self.Tors = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.TorsimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[3]))
			self.Tors.create_image(0,0,anchor=NW,image=self.TorsimgOpened)
			self.Tors.place(x=456,y=0)
			self.Ruki = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.RukiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[4]))
			self.Ruki.create_image(0,0,anchor=NW,image=self.RukiimgOpened)
			self.Ruki.place(x=608,y=0)		
			self.Nogi = Canvas(self.ramk, highlightbackground="LightGoldenrod4", highlightthickness=0, width=150, height=321)
			self.NogiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[5]))
			self.Nogi.create_image(0,0,anchor=NW,image=self.NogiimgOpened)
			self.Nogi.place(x=760,y=0)		
			self.Pruka.bind("<Button-3>", lambda e: self.Snyati(None,"Pruka"))
			self.Lruka.bind("<Button-3>",lambda e: self.Snyati(None,"Lruka"))
			self.Golova.bind("<Button-3>",lambda e: self.Snyati(None,"Golova"))
			self.Tors.bind("<Button-3>",lambda e: self.Snyati(None,"Tors"))
			self.Ruki.bind("<Button-3>",lambda e: self.Snyati(None,"Ruki"))
			self.Nogi.bind("<Button-3>",lambda e: self.Snyati(None,"Nogi"))
			self.balPRuka.bind(self.Pruka, self.balpruka)
			self.balLRuka.bind(self.Lruka, self.ballruka)
			self.balGolova.bind(self.Golova, self.balgolova)
			self.balTors.bind(self.Tors, self.baltors)
			self.balRuki.bind(self.Ruki, self.balruki)
			self.balNogi.bind(self.Nogi, self.balnogi)
			self.images(self.classimg)
			if len(self.meshokID)==0:
				self.textes="Экипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
				self.newprinttex(self.textes)
				self.newprintCSSt("Ваш мешок пуст\n0)Продолжить игру")
			else:
				self.uporyadochivanie()
				self.newprintCSSt(self.uporyd)
				self.textes="Экипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
				self.newprinttex(self.textes)
				self.cor=1
			self.func="Инвентарь"
			self.cor=1
			self.stats="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nТекущие значения:\nСила(Свои/предметы): " + str(self.FS) + " (" + str(self.S) + "/" + str(self.AS[0]) + ")\nЛовкость(Свои/предметы): " + str(self.FA) + " (" + str(self.A) + "/" + str(self.AA[0]) + ")\nМудрость(Свои/предметы): " + str(self.FM) + " (" + str(self.M) + "/" + str(self.AM[0]) + ")\nЗдоровье(Свои/предметы: )" + str(self.FH) + " (" + str(self.H) + "/" + str(self.AH[0]) + ")\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nСпособности: " + str(self.S0) + "\nАктивные способности: " + str(self.SA0) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nОчки здоровья: " + str(self.HP) + "/" + str(self.FHP) + "\nОчки ресурса: " + str(self.MP) + "/" + str(self.FMP) + "\nУрон: " + str(self.uron)
			self.stats+="\nОсновная характеристика оружия: "
			if self.weapon=="power":
				self.stats+="Сила"
			elif self.weapon=="agility":
				self.stats+="Ловкость"
			elif self.weapon=="magic":
				self.stats+="Разум"
			self.stats+= "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nБроня: " + str(self.PhisRes[0]) + "\nЗащита от огня: " + str(self.FireRes[0]) + "\nЗащита от воды: " + str(self.WaterRes[0]) + "\nЗащита от земли: " + str(self.EarthRes[0]) + "\nЗащита от воздуха: " + str(self.AirRes[0]) + "\nЗащита от кровотечения: " + str(self.BleedRes[0]) + "\nЗащита от яда: " + str(self.PoisRes[0]) + "\nЗащита от контроля: " + str(self.ControllRes[0]) + "\nБлок: " + str(self.Block[0]) + "\nУворот: " + str(self.Dodge[0])
			self.newprintstat(self.stats)
	
	def Snyati(self, event, x): # ------------------------------------------------РАЗДЕВАНИЕ НАЖАТИЕМ
		if self.sounds==1:
			self.clicking()
		if x=="Pruka":
			if self.inventID[0]=="000":
				None
			else:
				if self.inventID[0]==self.inventID[1]:
					MestoDlyaSneiya=1
					self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
					self.meshok.append(self.invent[MestoDlyaSneiya-1])
					self.balpruka="Пусто"
					self.ballruka="Пусто"
					self.balPRuka.bind(self.Pruka, self.balpruka)
					self.balLRuka.bind(self.Lruka, self.ballruka)
					self.invent[MestoDlyaSneiya]="Левая рука"
					self.invent[MestoDlyaSneiya-1]="Правая рука"
					self.Inventimg[0] = 'Data/img/Inventar/Pruka.png'
					self.Inventimg[1] = 'Data/img/Inventar/Lruka.png'
				else:
					MestoDlyaSneiya=1
					self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
					self.meshok.append(self.invent[MestoDlyaSneiya-1])
					self.Inventimg[0] = 'Data/img/Inventar/Pruka.png'
					self.balpruka="Пусто"
					self.balPRuka.bind(self.Pruka, self.balpruka)
					self.invent[MestoDlyaSneiya-1]="Правая рука"
		elif x=="Lruka":
			if self.inventID[1]=="000":
				None
			else:
				if self.inventID[0]==self.inventID[1]:
					MestoDlyaSneiya=1
					self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
					self.meshok.append(self.invent[MestoDlyaSneiya-1])
					self.Inventimg[0] = 'Data/img/Inventar/Pruka.png'
					self.Inventimg[1] = 'Data/img/Inventar/Lruka.png'
					self.balpruka="Пусто"
					self.ballruka="Пусто"
					self.balPRuka.bind(self.Pruka, self.balpruka)
					self.balLRuka.bind(self.Lruka, self.ballruka)
					self.invent[MestoDlyaSneiya]="Левая рука"
					self.invent[MestoDlyaSneiya-1]="Правая рука"
				else:
					MestoDlyaSneiya=2
					self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
					self.meshok.append(self.invent[MestoDlyaSneiya-1])
					self.Inventimg[1] = 'Data/img/Inventar/Lruka.png'
					self.ballruka="Пусто"
					self.balLRuka.bind(self.Lruka, self.ballruka)
					self.invent[MestoDlyaSneiya-1]="Левая рука"
		elif x=="Golova":
			if self.inventID[2]=="000":
				None
			else:
				MestoDlyaSneiya=3
				self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
				self.meshok.append(self.invent[MestoDlyaSneiya-1])
				self.balgolova="Пусто"
				self.balGolova.bind(self.Golova, self.balgolova)
				self.Inventimg[2] = 'Data/img/Inventar/Golova.png'
				self.invent[MestoDlyaSneiya-1]="Голова"
		elif x=="Tors":
			if self.inventID[3]=="000":
				None
			else:
				MestoDlyaSneiya=4
				self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
				self.meshok.append(self.invent[MestoDlyaSneiya-1])
				self.baltors="Пусто"
				self.balTors.bind(self.Tors, self.baltors)
				self.Inventimg[3] = 'Data/img/Inventar/Tors.png'
				self.invent[MestoDlyaSneiya-1]="Торс"
		elif x=="Ruki":
			if self.inventID[4]=="000":
				None
			else:
				MestoDlyaSneiya=5
				self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
				self.meshok.append(self.invent[MestoDlyaSneiya-1])
				self.balruki="Пусто"
				self.balRuki.bind(self.Ruki,self.balruki)
				self.Inventimg[4] ='Data/img/Inventar/Ruki.png'
				self.invent[MestoDlyaSneiya-1]="Руки"
		elif x=="Nogi":
			if self.inventID[5]=="000":
				None
			else:
				MestoDlyaSneiya=6
				self.meshokID.append(self.inventID[MestoDlyaSneiya-1])
				self.meshok.append(self.invent[MestoDlyaSneiya-1])
				self.balnogi="Пусто"
				self.balNogi.bind(self.Nogi,self.balnogi)
				self.Inventimg[5] = 'Data/img/Inventar/Nogi.png'
				self.invent[MestoDlyaSneiya-1]="Ноги"
		self.Pruka.delete()
		self.Lruka.delete()
		self.Golova.delete()
		self.Tors.delete()
		self.Ruki.delete()
		self.Nogi.delete()
		self.PrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[0]))
		self.Pruka.create_image(0,0,anchor=NW,image=self.PrukaimgOpened)
		self.LrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[1]))
		self.Lruka.create_image(0,0,anchor=NW,image=self.LrukaimgOpened)
		self.GolovaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[2]))
		self.Golova.create_image(0,0,anchor=NW,image=self.GolovaimgOpened)
		self.TorsimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[3]))
		self.Tors.create_image(0,0,anchor=NW,image=self.TorsimgOpened)
		self.RukiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[4]))
		self.Ruki.create_image(0,0,anchor=NW,image=self.RukiimgOpened)
		self.NogiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[5]))
		self.Nogi.create_image(0,0,anchor=NW,image=self.NogiimgOpened)
		self.inventID[MestoDlyaSneiya-1]="000"
		self.AS[MestoDlyaSneiya]=0;self.AA[MestoDlyaSneiya]=0;self.AM[MestoDlyaSneiya]=0;self.AH[MestoDlyaSneiya]=0
		self.Equipment[MestoDlyaSneiya-1]="Пусто"
		self.FireRes[MestoDlyaSneiya]=0;self.WaterRes[MestoDlyaSneiya]=0;self.EarthRes[MestoDlyaSneiya]=0;self.AirRes[MestoDlyaSneiya]=0;self.PhisRes[MestoDlyaSneiya]=0;self.BleedRes[MestoDlyaSneiya]=0;self.PoisRes[MestoDlyaSneiya]=0;
		self.ControllRes[MestoDlyaSneiya]=0;
		self.Dodge[MestoDlyaSneiya]=0;self.Block[MestoDlyaSneiya]=0;self.atk[MestoDlyaSneiya]=0;self.MSTN[MestoDlyaSneiya]=0;self.LVLN[MestoDlyaSneiya]=0;self.MNMC[MestoDlyaSneiya]=0;self.MNMG[MestoDlyaSneiya]=0
		self.uporyadochivanie()
		self.newprintCSSt(self.uporyd)
		self.textes="Экипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
		self.newprinttex(self.textes)
		self.AS[0]=self.AS[1]+self.AS[2]+self.AS[3]+self.AS[4]+self.AS[5]+self.AS[6]; self.AM[0]=self.AM[1]+self.AM[2]+self.AM[3]+self.AM[4]+self.AM[5]+self.AM[6]; self.AA[0]=self.AA[1]+self.AA[2]+self.AA[3]+self.AA[4]+self.AA[5]+self.AA[6]; self.AH[0]=self.AH[1]+self.AH[2]+self.AH[3]+self.AH[4]+self.AH[5]+self.AH[6]
		self.FireRes[0]=self.FireRes[1]+self.FireRes[2]+self.FireRes[3]+self.FireRes[4]+self.FireRes[5]+self.FireRes[6]; self.WaterRes[0]=self.WaterRes[1]+self.WaterRes[2]+self.WaterRes[3]+self.WaterRes[4]+self.WaterRes[5]+self.WaterRes[6]
		self.EarthRes[0]=self.EarthRes[1]+self.EarthRes[2]+self.EarthRes[3]+self.EarthRes[4]+self.EarthRes[5]+self.EarthRes[6]; self.AirRes[0]=self.AirRes[1]+self.AirRes[2]+self.AirRes[3]+self.AirRes[4]+self.AirRes[5]+self.AirRes[6]
		self.PhisRes[0]=self.PhisRes[1]+self.PhisRes[2]+self.PhisRes[3]+self.PhisRes[4]+self.PhisRes[5]+self.PhisRes[6]; self.BleedRes[0]=self.BleedRes[1]+self.BleedRes[2]+self.BleedRes[3]+self.BleedRes[4]+self.BleedRes[5]+self.BleedRes[6]
		self.PoisRes[0]=self.PoisRes[1]+self.PoisRes[2]+self.PoisRes[3]+self.PoisRes[4]+self.PoisRes[5]+self.PoisRes[6];
		self.Block[0]=self.Block[1]+self.Block[2]+self.Block[3]+self.Block[4]+self.Block[5]+self.Block[6];self.Dodge[0]=self.Dodge[1]+self.Dodge[2]+self.Dodge[3]+self.Dodge[4]+self.Dodge[5]+self.Dodge[6]
		self.FS=self.S+self.AS[0]; self.FM=self.M+self.AM[0]; self.FA=self.A+self.AA[0]; self.FH=self.H+self.AH[0]; self.FHP=self.FH*5; self.FMP=self.FM*5
		if self.FHP<self.HP:
			self.HP=self.FHP
		if self.FMP<self.MP:
			self.MP=self.FMP
		if self.weapon=="power":
			self.uron=round((self.atk[0]+self.atkp)*(self.FS*0.08+self.FA*0.06+self.FM*0.04))
		elif self.weapon=="agility":
			self.uron=round((self.atk[0]+self.atkp)*(self.FA*0.08+self.FM*0.06+self.FS*0.04))
		elif self.weapon=="magic":
			self.uron=round((self.atk[0]+self.atkp)*(self.FM*0.08+self.FS*0.06+self.FA*0.04))
		self.stats="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nТекущие значения:\nСила(Свои/предметы): " + str(self.FS) + " (" + str(self.S) + "/" + str(self.AS[0]) + ")\nЛовкость(Свои/предметы): " + str(self.FA) + " (" + str(self.A) + "/" + str(self.AA[0]) + ")\nМудрость(Свои/предметы): " + str(self.FM) + " (" + str(self.M) + "/" + str(self.AM[0]) + ")\nЗдоровье(Свои/предметы: )" + str(self.FH) + " (" + str(self.H) + "/" + str(self.AH[0]) + ")\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nСпособности: " + str(self.S0) + "\nАктивные способности: " + str(self.SA0) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nОчки здоровья: " + str(self.HP) + "/" + str(self.FHP) + "\nОчки ресурса: " + str(self.MP) + "/" + str(self.FMP) + "\nУрон: " + str(self.uron)
		self.stats+="\nОсновная характеристика оружия: "
		if self.weapon=="power":
			self.stats+="Сила"
		elif self.weapon=="agility":
			self.stats+="Ловкость"
		elif self.weapon=="magic":
			self.stats+="Разум"
		self.stats+= "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nБроня: " + str(self.PhisRes[0]) + "\nЗащита от огня: " + str(self.FireRes[0]) + "\nЗащита от воды: " + str(self.WaterRes[0]) + "\nЗащита от земли: " + str(self.EarthRes[0]) + "\nЗащита от воздуха: " + str(self.AirRes[0]) + "\nЗащита от кровотечения: " + str(self.BleedRes[0]) + "\nЗащита от яда: " + str(self.PoisRes[0]) + "\nЗащита от контроля: " + str(self.ControllRes[0]) + "\nБлок: " + str(self.Block[0]) + "\nУворот: " + str(self.Dodge[0])
		self.newprintstat(self.stats)	

	def uporyadochivanie(self):
		meshokP=[]
		meshokIDP=[]
		smotP=0
		meshokL=[]
		meshokIDL=[]
		smotL=0
		meshokG=[]
		meshokIDG=[]
		smotG=0
		meshokT=[]
		meshokIDT=[]
		smotT=0
		meshokR=[]
		meshokIDR=[]
		smotR=0
		meshokN=[]
		meshokIDN=[]
		smotN=0
		nomershmot=0
		kolpredinmesh=len(self.meshok)
		i=0
		while i!=kolpredinmesh:
			z=self.meshokID[i]
			if z[2:3]=="P":
				meshokP.append(self.meshok[i])
				meshokIDP.append(self.meshokID[i])
				smotP+=1
			if z[2:3]=="L":
				meshokL.append(self.meshok[i])
				meshokIDL.append(self.meshokID[i])
				smotL+=1
			if z[2:3]=="G":
				meshokG.append(self.meshok[i])
				meshokIDG.append(self.meshokID[i])
				smotG+=1
			if z[2:3]=="T":
				meshokT.append(self.meshok[i])
				meshokIDT.append(self.meshokID[i])
				smotT+=1
			if z[2:3]=="R":
				meshokR.append(self.meshok[i])
				meshokIDR.append(self.meshokID[i])
				smotR+=1
			if z[2:3]=="N":
				meshokN.append(self.meshok[i])
				meshokIDN.append(self.meshokID[i])
				smotN+=1
			i+=1
		self.meshok.clear()
		self.meshokID.clear()
		self.meshok.extend(meshokP)
		self.meshokID.extend(meshokIDP)
		self.meshok.extend(meshokL)
		self.meshokID.extend(meshokIDL)
		self.meshok.extend(meshokG)
		self.meshokID.extend(meshokIDG)
		self.meshok.extend(meshokT)
		self.meshokID.extend(meshokIDT)
		self.meshok.extend(meshokR)
		self.meshokID.extend(meshokIDR)
		self.meshok.extend(meshokN)
		self.meshokID.extend(meshokIDN)
		self.uporyd="0)Продолжить\nВыберите вещь"
		if smotP!=0:
			self.uporyd+="\n                 ОРУЖИЕ"
			while smotP!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotP-=1
		if smotL!=0:
			self.uporyd+="\n                  ЩИТЫ"
			while smotL!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotL-=1
		if smotG!=0:
			self.uporyd+="\n                  ШЛЕМА"
			while smotG!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotG-=1
		if smotT!=0:
			self.uporyd+="\n                  ТОРС"
			while smotT!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotT-=1
		if smotR!=0:
			self.uporyd+="\n                ПЕРЧАТКИ"
			while smotR!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotR-=1
		if smotN!=0:
			self.uporyd+="\n                 САПОГИ"
			while smotN!=0:
				stri="\n"+str(nomershmot+1)+")"
				self.uporyd+=stri + str(self.meshok[nomershmot])
				nomershmot+=1
				smotN-=1

	def prokachka(self):
		if self.sounds==1:
			self.clicking()
		try:
			self.Tors.destroy()
			self.Golova.destroy()
			self.Ruki.destroy()
			self.Pruka.destroy()
			self.Lruka.destroy()
			self.Nogi.destroy()
		except:
			None
		#Основа
		self.images(self.classimg)
		
		self.AbilityIMGCanv = Canvas(self.ramk,width=793, height=321, highlightthickness=0)
		self.AbilityIMGCanv.create_image(0,0,anchor=NW,image=self.AbilityIMG)
		self.AbilityIMGCanv.place(x=0,y=0)
		
		self.HaracIMGCanv = Canvas(self.ramk,width=122, height=321, highlightthickness=0)
		self.HaracIMGCanv.create_image(0,0,anchor=NW,image=self.HaracIMG)
		self.HaracIMGCanv.place(x=793,y=0)
		
		#Пассивки и персонаж
		
		self.PlusSTR = Canvas(self.ramk,width=17, height=17, highlightthickness=0)
		self.PlusSTR.create_image(0,0,anchor=NW,image=self.PlusIMG)
		self.PlusSTR.place(x=895,y=96)
		self.PlusSTR.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,3))
		
		self.PlusAGL = Canvas(self.ramk,width=17, height=17, highlightthickness=0)
		self.PlusAGL.create_image(0,0,anchor=NW,image=self.PlusIMG)
		self.PlusAGL.place(x=895,y=114)
		self.PlusAGL.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,4))
		
		self.PlusMND = Canvas(self.ramk,width=17, height=17, highlightthickness=0)
		self.PlusMND.create_image(0,0,anchor=NW,image=self.PlusIMG)
		self.PlusMND.place(x=895,y=132)
		self.PlusMND.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,5))
		
		self.PlusHLT = Canvas(self.ramk,width=17, height=17, highlightthickness=0)
		self.PlusHLT.create_image(0,0,anchor=NW,image=self.PlusIMG)
		self.PlusHLT.place(x=895,y=150)
		self.PlusHLT.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,6))
		
		self.ActivButCanv = Canvas(self.ramk,width=35, height=35, highlightthickness=0)
		self.ActivButCanv.place(x=836,y=203)
		self.ActivButCanv.create_image(0,0,anchor=NW,image=self.YESIMG)
		self.ActivButCanv.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,7))
		
		self.PassiveButCanv = Canvas(self.ramk,width=35, height=35, highlightthickness=0)
		self.PassiveButCanv.place(x=836,y=261)
		self.PassiveButCanv.create_image(0,0,anchor=NW,image=self.NOIMG)
		self.PassiveButCanv.bind("<Button-1>", lambda e: self.KnopkiFUNC(None,8))
		
		self.STRtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
		self.STRtextCanv.place(x=862,y=97)
		self.STRtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.S)
		
		self.AGLtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
		self.AGLtextCanv.place(x=862,y=115)
		self.AGLtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.A)
		
		self.MNDtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
		self.MNDtextCanv.place(x=862,y=133)
		self.MNDtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.M)
		
		self.HLTtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
		self.HLTtextCanv.place(x=862,y=151)
		self.HLTtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.H)
		
		self.PNTtextCanv = Canvas(self.ramk,width=49, height=15, highlightthickness=0)
		self.PNTtextCanv.place(x=862,y=60)
		self.PNTtextCanv.create_text(24,5,font=("Gabriola", 12),text=self.P)
		
		self.SAPtextCanv = Canvas(self.ramk,width=49, height=15, highlightthickness=0)
		self.SAPtextCanv.place(x=862,y=42)
		self.SAPtextCanv.create_text(24,5,font=("Gabriola", 12),text=self.SAP)
		
		self.SPPtextCanv = Canvas(self.ramk,width=49, height=15, highlightthickness=0)
		self.SPPtextCanv.place(x=862,y=24)
		self.SPPtextCanv.create_text(24,5,font=("Gabriola", 12),text=self.SP)
		
		self.KolSpellov=1
		while self.KolSpellov<38:
			try:
				self.SpellUp(None,self.KolSpellov,0)
				self.KolSpellov+=1
			except:
				break
		
		self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
		self.newprinttex(self.textes)
		self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
		self.func="Прокачка персонажа"
		self.cor=1
		self.stats="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nТекущие значения:\nСила(Свои/предметы): " + str(self.FS) + " (" + str(self.S) + "/" + str(self.AS[0]) + ")\nЛовкость(Свои/предметы): " + str(self.FA) + " (" + str(self.A) + "/" + str(self.AA[0]) + ")\nМудрость(Свои/предметы): " + str(self.FM) + " (" + str(self.M) + "/" + str(self.AM[0]) + ")\nЗдоровье(Свои/предметы: )" + str(self.FH) + " (" + str(self.H) + "/" + str(self.AH[0]) + ")\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nСпособности: " + str(self.S0) + "\nАктивные способности: " + str(self.SA0) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nОчки здоровья: " + str(self.HP) + "/" + str(self.FHP) + "\nОчки ресурса: " + str(self.MP) + "/" + str(self.FMP) + "\nУрон: " + str(self.uron) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nБроня: " + str(self.PhisRes[0]) + "\nЗащита от огня: " + str(self.FireRes[0]) + "\nЗащита от воды: " + str(self.WaterRes[0]) + "\nЗащита от земли: " + str(self.EarthRes[0]) + "\nЗащита от воздуха: " + str(self.AirRes[0]) + "\nЗащита от кровотечения: " + str(self.BleedRes[0]) + "\nЗащита от яда: " + str(self.PoisRes[0]) + "\nЗащита от контроля: " + str(self.ControllRes[0])
		self.newprintstat(self.stats)	

	def SpellUp(self, event,i,d): #---------------------------------------------Не готово
		global spell1,spell2,spell3
		if i==1:
			if d!=0:
				try:
					CanvSpell1.destroy()
				except:
					None
				SAID[0]+=1;SAP-=1
			if SAID[0]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[0]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell1=ImageTk.PhotoImage(spell)
			CanvSpell1=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell1.place(x=22,y=209)
			CanvSpell1.create_image(0,0,anchor=NW,image=spell1)
			CanvSpell1.create_text(10,10,font=("Gabriola", 10),text=SAID[0])
		elif i==2:
			if d!=0:
				try:
					CanvSpell2.destroy()
				except:
					None
				SAID[1]+=1;SAP-=1
			if SAID[1]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[1]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell2=ImageTk.PhotoImage(spell)
			CanvSpell2=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell2.place(x=c,y=v)
			CanvSpell2.create_image(0,0,anchor=NW,image=spell2)
			CanvSpell2.create_text(10,10,font=("Gabriola", 10),text=SAID[1])
		elif i==3:
			if d!=0:
				try:
					CanvSpell3.destroy()
				except:
					None
				SAID[2]+=1;SAP-=1
			if SAID[2]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[2]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell3=ImageTk.PhotoImage(spell)
			CanvSpell3=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell3.place(x=c,y=v)
			CanvSpell3.create_image(0,0,anchor=NW,image=spell3)
			CanvSpell3.create_text(10,10,font=("Gabriola", 10),text=SAID[2])
		elif i==4:
			if d!=0:
				try:
					CanvSpell4.destroy()
				except:
					None
				SAID[3]+=1;SAP-=1
			if SAID[3]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[3]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell4=ImageTk.PhotoImage(spell)
			CanvSpell4=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell4.place(x=c,y=v)
			CanvSpell4.create_image(0,0,anchor=NW,image=spell4)
			CanvSpell4.create_text(10,10,font=("Gabriola", 10),text=SAID[3])
		elif i==5:
			if d!=0:
				try:
					CanvSpell5.destroy()
				except:
					None
				SAID[4]+=1;SAP-=1
			if SAID[4]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[4]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell5=ImageTk.PhotoImage(spell)
			CanvSpell5=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell5.place(x=c,y=v)
			CanvSpell5.create_image(0,0,anchor=NW,image=spell5)
			CanvSpell5.create_text(10,10,font=("Gabriola", 10),text=SAID[4])
		elif i==6:
			if d!=0:
				try:
					CanvSpell6.destroy()
				except:
					None
				SAID[5]+=1;SAP-=1
			if SAID[5]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[5]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell6=ImageTk.PhotoImage(spell)
			CanvSpell6=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell6.place(x=c,y=v)
			CanvSpell6.create_image(0,0,anchor=NW,image=spell6)
			CanvSpell6.create_text(10,10,font=("Gabriola", 10),text=SAID[5])
		elif i==7:
			if d!=0:
				try:
					CanvSpell7.destroy()
				except:
					None
				SAID[6]+=1;SAP-=1
			if SAID[6]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[6]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell7=ImageTk.PhotoImage(spell)
			CanvSpell7=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell7.place(x=c,y=v)
			CanvSpell7.create_image(0,0,anchor=NW,image=spell7)
			CanvSpell7.create_text(10,10,font=("Gabriola", 10),text=SAID[6])
		elif i==8:
			if d!=0:
				try:
					CanvSpell8.destroy()
				except:
					None
				SAID[7]+=1;SAP-=1
			if SAID[7]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[7]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell8=ImageTk.PhotoImage(spell)
			CanvSpell8=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell8.place(x=c,y=v)
			CanvSpell8.create_image(0,0,anchor=NW,image=spell8)
			CanvSpell8.create_text(10,10,font=("Gabriola", 10),text=SAID[7])
		elif i==9:
			if d!=0:
				try:
					CanvSpell9.destroy()
				except:
					None
				SAID[8]+=1;SAP-=1
			if SAID[8]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[8]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell9=ImageTk.PhotoImage(spell)
			CanvSpell9=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell9.place(x=c,y=v)
			CanvSpell9.create_image(0,0,anchor=NW,image=spell9)
			CanvSpell9.create_text(10,10,font=("Gabriola", 10),text=SAID[8])
		elif i==10:
			if d!=0:
				try:
					CanvSpell10.destroy()
				except:
					None
				SAID[9]+=1;SAP-=1
			if SAID[9]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[9]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell10=ImageTk.PhotoImage(spell)
			CanvSpell10=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell10.place(x=c,y=v)
			CanvSpell10.create_image(0,0,anchor=NW,image=spell10)
			CanvSpell10.create_text(10,10,font=("Gabriola", 10),text=SAID[9])
		elif i==11:
			if d!=0:
				try:
					CanvSpell11.destroy()
				except:
					None
				SAID[10]+=1;SAP-=1
			if SAID[10]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[10]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell11=ImageTk.PhotoImage(spell)
			CanvSpell11=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell11.place(x=c,y=v)
			CanvSpell11.create_image(0,0,anchor=NW,image=spell11)
			CanvSpell11.create_text(10,10,font=("Gabriola", 10),text=SAID[10])
		elif i==12:
			if d!=0:
				try:
					CanvSpell12.destroy()
				except:
					None
				SAID[11]+=1;SAP-=1
			if SAID[11]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[11]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell12=ImageTk.PhotoImage(spell)
			CanvSpell12=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell12.place(x=c,y=v)
			CanvSpell12.create_image(0,0,anchor=NW,image=spell12)
			CanvSpell12.create_text(10,10,font=("Gabriola", 10),text=SAID[11])
		elif i==13:
			if d!=0:
				try:
					CanvSpell13.destroy()
				except:
					None
				SAID[12]+=1;SAP-=1
			if SAID[12]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[12]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell13=ImageTk.PhotoImage(spell)
			CanvSpell13=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell13.place(x=c,y=v)
			CanvSpell13.create_image(0,0,anchor=NW,image=spell13)
			CanvSpell13.create_text(10,10,font=("Gabriola", 10),text=SAID[12])
		elif i==14:
			if d!=0:
				try:
					CanvSpell14.destroy()
				except:
					None
				SAID[13]+=1;SAP-=1
			if SAID[13]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[13]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell14=ImageTk.PhotoImage(spell)
			CanvSpell14=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell14.place(x=c,y=v)
			CanvSpell14.create_image(0,0,anchor=NW,image=spell14)
			CanvSpell14.create_text(10,10,font=("Gabriola", 10),text=SAID[13])
		elif i==15:
			if d!=0:
				try:
					CanvSpell15.destroy()
				except:
					None
				SAID[14]+=1;SAP-=1
			if SAID[14]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[14]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell15=ImageTk.PhotoImage(spell)
			CanvSpell15=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell15.place(x=c,y=v)
			CanvSpell15.create_image(0,0,anchor=NW,image=spell15)
			CanvSpell15.create_text(10,10,font=("Gabriola", 10),text=SAID[14])
		elif i==16:
			if d!=0:
				try:
					CanvSpell16.destroy()
				except:
					None
				SAID[15]+=1;SAP-=1
			if SAID[15]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[15]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell16=ImageTk.PhotoImage(spell)
			CanvSpell16=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell16.place(x=c,y=v)
			CanvSpell16.create_image(0,0,anchor=NW,image=spell16)
			CanvSpell16.create_text(10,10,font=("Gabriola", 10),text=SAID[15])
		elif i==17:
			if d!=0:
				try:
					CanvSpell17.destroy()
				except:
					None
				SAID[16]+=1;SAP-=1
			if SAID[16]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[16]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell17=ImageTk.PhotoImage(spell)
			CanvSpell17=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell17.place(x=c,y=v)
			CanvSpell17.create_image(0,0,anchor=NW,image=spell17)
			CanvSpell17.create_text(10,10,font=("Gabriola", 10),text=SAID[16])
		elif i==18:
			if d!=0:
				try:
					CanvSpell18.destroy()
				except:
					None
				SAID[17]+=1;SAP-=1
			if SAID[17]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[17]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell18=ImageTk.PhotoImage(spell)
			CanvSpell18=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell18.place(x=c,y=v)
			CanvSpell18.create_image(0,0,anchor=NW,image=spell18)
			CanvSpell18.create_text(10,10,font=("Gabriola", 10),text=SAID[17])
		elif i==19:
			if d!=0:
				try:
					CanvSpell19.destroy()
				except:
					None
				SAID[18]+=1;SAP-=1
			if SAID[18]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[18]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell19=ImageTk.PhotoImage(spell)
			CanvSpell19=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell19.place(x=c,y=v)
			CanvSpell19.create_image(0,0,anchor=NW,image=spell19)
			CanvSpell19.create_text(10,10,font=("Gabriola", 10),text=SAID[18])
		elif i==20:
			if d!=0:
				try:
					CanvSpell20.destroy()
				except:
					None
				SAID[19]+=1;SAP-=1
			if SAID[19]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[19]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell20=ImageTk.PhotoImage(spell)
			CanvSpell20=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell20.place(x=c,y=v)
			CanvSpell20.create_image(0,0,anchor=NW,image=spell20)
			CanvSpell20.create_text(10,10,font=("Gabriola", 10),text=SAID[19])
		elif i==21:
			if d!=0:
				try:
					CanvSpell21.destroy()
				except:
					None
				SAID[20]+=1;SAP-=1
			if SAID[20]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[20]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell21=ImageTk.PhotoImage(spell)
			CanvSpell21=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell21.place(x=c,y=v)
			CanvSpell21.create_image(0,0,anchor=NW,image=spell21)
			CanvSpell21.create_text(10,10,font=("Gabriola", 10),text=SAID[20])
		elif i==22:
			if d!=0:
				try:
					CanvSpell22.destroy()
				except:
					None
				SAID[21]+=1;SAP-=1
			if SAID[21]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[21]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell22=ImageTk.PhotoImage(spell)
			CanvSpell22=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell22.place(x=c,y=v)
			CanvSpell22.create_image(0,0,anchor=NW,image=spell22)
			CanvSpell22.create_text(10,10,font=("Gabriola", 10),text=SAID[21])
		elif i==23:
			if d!=0:
				try:
					CanvSpell23.destroy()
				except:
					None
				SAID[22]+=1;SAP-=1
			if SAID[22]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[22]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell23=ImageTk.PhotoImage(spell)
			CanvSpell23=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell23.place(x=c,y=v)
			CanvSpell23.create_image(0,0,anchor=NW,image=spell23)
			CanvSpell23.create_text(10,10,font=("Gabriola", 10),text=SAID[22])
		elif i==24:
			if d!=0:
				try:
					CanvSpell24.destroy()
				except:
					None
				SAID[23]+=1;SAP-=1
			if SAID[23]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[23]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell24=ImageTk.PhotoImage(spell)
			CanvSpell24=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell24.place(x=c,y=v)
			CanvSpell24.create_image(0,0,anchor=NW,image=spell24)
			CanvSpell24.create_text(10,10,font=("Gabriola", 10),text=SAID[23])
		elif i==25:
			if d!=0:
				try:
					CanvSpell25.destroy()
				except:
					None
				SAID[24]+=1;SAP-=1
			if SAID[24]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[24]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell25=ImageTk.PhotoImage(spell)
			CanvSpell25=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell25.place(x=c,y=v)
			CanvSpell25.create_image(0,0,anchor=NW,image=spell25)
			CanvSpell25.create_text(10,10,font=("Gabriola", 10),text=SAID[24])
		elif i==26:
			if d!=0:
				try:
					CanvSpell26.destroy()
				except:
					None
				SAID[25]+=1;SAP-=1
			if SAID[25]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[25]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell26=ImageTk.PhotoImage(spell)
			CanvSpell26=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell26.place(x=c,y=v)
			CanvSpell26.create_image(0,0,anchor=NW,image=spell26)
			CanvSpell26.create_text(10,10,font=("Gabriola", 10),text=SAID[25])
		elif i==27:
			if d!=0:
				try:
					CanvSpell27.destroy()
				except:
					None
				SAID[26]+=1;SAP-=1
			if SAID[26]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[26]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell27=ImageTk.PhotoImage(spell)
			CanvSpell27=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell27.place(x=c,y=v)
			CanvSpell27.create_image(0,0,anchor=NW,image=spell27)
			CanvSpell27.create_text(10,10,font=("Gabriola", 10),text=SAID[26])
		elif i==28:
			if d!=0:
				try:
					CanvSpell28.destroy()
				except:
					None
				SAID[27]+=1;SAP-=1
			if SAID[27]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[27]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell28=ImageTk.PhotoImage(spell)
			CanvSpell28=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell28.place(x=c,y=v)
			CanvSpell28.create_image(0,0,anchor=NW,image=spell28)
			CanvSpell28.create_text(10,10,font=("Gabriola", 10),text=SAID[27])
		elif i==29:
			if d!=0:
				try:
					CanvSpell29.destroy()
				except:
					None
				SAID[28]+=1;SAP-=1
			if SAID[28]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[28]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell29=ImageTk.PhotoImage(spell)
			CanvSpell29=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell29.place(x=c,y=v)
			CanvSpell29.create_image(0,0,anchor=NW,image=spell29)
			CanvSpell29.create_text(10,10,font=("Gabriola", 10),text=SAID[28])
		elif i==30:
			if d!=0:
				try:
					CanvSpell30.destroy()
				except:
					None
				SAID[29]+=1;SAP-=1
			if SAID[29]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[29]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell30=ImageTk.PhotoImage(spell)
			CanvSpell30=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell30.place(x=c,y=v)
			CanvSpell30.create_image(0,0,anchor=NW,image=spell30)
			CanvSpell30.create_text(10,10,font=("Gabriola", 10),text=SAID[29])
		elif i==31:
			if d!=0:
				try:
					CanvSpell31.destroy()
				except:
					None
				SAID[30]+=1;SAP-=1
			if SAID[30]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[30]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell31=ImageTk.PhotoImage(spell)
			CanvSpell31=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell31.place(x=c,y=v)
			CanvSpell31.create_image(0,0,anchor=NW,image=spell31)
			CanvSpell31.create_text(10,10,font=("Gabriola", 10),text=SAID[30])
		elif i==32:
			if d!=0:
				try:
					CanvSpell32.destroy()
				except:
					None
				SAID[31]+=1;SAP-=1
			if SAID[31]>0:
				spell=Image.open("Data\img\Prokachka\spellvk.gif")
			elif SAID[31]==0:
				spell=Image.open("Data\img\Prokachka\spellne.gif")
			spell32=ImageTk.PhotoImage(spell)
			CanvSpell32=Canvas(ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=17, height=17)
			CanvSpell32.place(x=c,y=v)
			CanvSpell32.create_image(0,0,anchor=NW,image=spell32)
			CanvSpell32.create_text(10,10,font=("Gabriola", 10),text=SAID[31])
		
	def Music(self): # ----------------------------------------------------------ФЛАГ ПРОИГРЫВАТЕЛЯ
		if self.sounds==1:
			self.clicking()
		if self.Musicplay==1:
			self.Musicplay=0
			self.opm.entryconfig(0, label="Музыка: Выкл")
			pygame.mixer.music.stop()
		elif self.Musicplay==0:
			self.Musicplay=1
			self.opm.entryconfig(0, label="Музыка: Вкл")
	
	def Sounds(self):
		if self.sounds==0:
			self.clicking()
		if self.sounds==1:
			self.sounds=0
			self.opm.entryconfig(1, label="Звуки: Выкл")
		elif self.sounds==0:
			self.sounds=1
			self.opm.entryconfig(1, label="Звуки: Вкл")
		
	def Interface(self):
		if self.sounds==1:
			self.clicking()
		os.startfile('Data\img\interface.jpg')
	
	def PathNote(self):
		if self.sounds==1:
			self.clicking()
		print("toto")
	
	def Autors(self):
		if self.sounds==1:
			self.clicking()
		print("Ведущий разработчик, деректор, лидер, босс, уничтожитель чая: Гильфанов Анвар Ирекович\nСценарист, кодер, проработка локаций и игрового мира: Борис Вениаминович Щщец\nСекритариат, работа с документацией, графическая обработка: Стаховец Елена Евгеньевна")

	def getXY(self, event):
		self.getx=event.x_root
		self.gety=event.y_root

	def clicking(self):
		self.click.play()

	def images(self, x):
		self.ph_im =ImageTk.PhotoImage(Image.open(x))
		self.canv111.create_image(0,0,anchor=NW,image=self.ph_im)

	def prodoljit(self):
		if self.sounds==1:
			self.clicking()
		self.otchistiti()
		self.func="Игра"
		self.images(self.locatImg)
		self.newprinttex(self.locatDisc)
		self.newprintCSSt(self.locatCSS)
		if self.func=="Игра" and self.part>0:
			self.stats="Локация: "+ self.locatCur +"\nЗдоровье: " + str(self.HP) + "/" + str(self.FHP) + "\nРесурс: " + str(self.MP) +"/"+str(self.FMP)
			self.newprintstat(self.stats)
		elif self.func=="Бой" and self.part>0:
			self.stats="Герой: \nЗдоровье: " + str(HP) + "/" + str(self.FHP) + "\nРесурс: " + str(self.MP) +"/"+str(self.FMP) + "\n\nВраг: " + str(self.Ename)
			if self.SID[24]==0:
				self.stats+="\nЗдоровье: неизвестно\nРесурс: неизвестно"
			elif self.SID[24]==1:
				self.stats+="\nЗдоровье: " + str(self.EHP) + "/" + str(self.EFHP) + "\nРесурс: " + str(self.EMP) +"/"+str(self.EFMP) 
			self.newprintstat(self.stats)

	def KnopkiFUNC(self, event, x):
		if self.init==0:
			None
		else:
			if x==1:
				if self.func=="Бой":
					self.newprinttex("Нельзя использовать в бою")
				else:
					if self.func=="Инвентарь":
						self.otchistiti()
						self.prodoljit()
					else:
						self.otchistiti()
						self.inventar()
			elif x==2:
				if self.func=="Бой":
					self.newprinttex("Нельзя использовать в бою")
				else:
					if self.func=="Прокачка персонажа":
						self.otchistiti()
						self.prodoljit()
					else:
						self.otchistiti()
						self.prokachka()
			elif x==3 or x==4 or x==5 or x==6:
				if self.sounds==1:
					self.clicking()
				if self.P>0:
					self.P-=1
					self.PNTtextCanv.destroy()
					self.PNTtextCanv = Canvas(self.ramk,width=49, height=15, highlightthickness=0)
					self.PNTtextCanv.place(x=862,y=60)
					self.PNTtextCanv.create_text(24,5,font=("Gabriola", 12),text=self.P)
					if x==3:
						self.S+=1
						self.STRtextCanv.destroy()
						self.STRtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
						self.STRtextCanv.place(x=862,y=97)
						self.STRtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.S)
					elif x==4:
						A+=1
						self.AGLtextCanv.destroy()
						self.AGLtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
						self.AGLtextCanv.place(x=862,y=115)
						self.AGLtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.A)
					elif x==5:
						self.M+=1
						self.MNDtextCanv.destroy()
						self.MNDtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
						self.MNDtextCanv.place(x=862,y=133)
						self.MNDtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.M)
					elif x==6:
						self.H+=1
						self.HLTtextCanv.destroy()
						self.HLTtextCanv = Canvas(self.ramk,width=31, height=15, highlightthickness=0)
						self.HLTtextCanv.place(x=862,y=151)
						self.HLTtextCanv.create_text(15,5,font=("Gabriola", 12),text=self.H)
				else:
					self.newprinttex("У вас недостаточно очков персонажа")
			else:
				if self.sounds==1:
					self.clicking()
				if self.x==7:
					self.ActivButCanv.create_image(0,0,anchor=NW,image=self.YESIMG)
					self.PassiveButCanv.create_image(0,0,anchor=NW,image=self.NOIMG)
					self.AbilityIMGCanv.create_image(0,0,anchor=NW,image=self.AbilityIMG)
					
				elif x==8:
					self.ActivButCanv.create_image(0,0,anchor=NW,image=self.NOIMG)
					self.PassiveButCanv.create_image(0,0,anchor=NW,image=self.YESIMG)
					self.AbilityIMGCanv.create_image(0,0,anchor=NW,image=self.AbilityPassIMG)

	#Игра		
	def new_game(self): # Начальные параметры при старте новой игры
		if self.sounds==1:
			self.clicking()
		self.otchistiti()
		#Другие переменные
		self.path=0;self.locat1="неизвестную сторону";self.name="?";self.expup=500;self.exp=0;self.magicdmg=0;self.vozvrat=0;self.loading=0;self.part=0;self.CurrentLocation="Обломки храма";self.Hour=12;self.Minutes=00;self.Days=0;self.Months=0;self.Years=0
		self.Weather=["Погода","Ясно","Пасмурно","Дождь","Гроза","Туман","Жара","Снег","Град","Ветер"];self.theftguild=0;self.zlo=0
			#Сопротивления
		self.FireRes=[0,0,0,0,0,0,0];self.WaterRes=[0,0,0,0,0,0,0];self.EarthRes=[0,0,0,0,0,0,0];self.AirRes=[0,0,0,0,0,0,0];self.PhisRes=[0,0,0,0,0,0,0];self.BleedRes=[0,0,0,0,0,0,0];self.PoisRes=[0,0,0,0,0,0,0];self.Dodge=[0,0,0,0,0,0,0];self.Block=[0,0,0,0,0,0,0]
		self.ControllRes=[0,0,0,0,0,0,0];self.MSTN=[0,0,0,0,0,0,0];self.LVLN=[0,0,0,0,0,0,0]
			#Характеристики
		self.P=30;self.SP=3;self.SAP=1;self.S=0;self.M=0;self.A=0;self.H=0;self.E=0;self.lvl=1;self.exp=0;self.safy=1;self.atkp=5;self.classname="Уникальный";self.atk=[0,0,0,0,0,0,0]
		self.AS=[0,0,0,0,0,0,0];self.AA=[0,0,0,0,0,0,0];self.AH=[0,0,0,0,0,0,0];self.AM=[0,0,0,0,0,0,0];self.MNMC=[0,0,0,0,0,0,0];self.MNMG=[0,0,0,0,0,0,0]
		self.Inventimg=['Data/img/Inventar/Pruka.png','Data/img/Inventar/Lruka.png','Data/img/Inventar/Golova.png','Data/img/Inventar/Tors.png','Data/img/Inventar/Ruki.png','Data/img/Inventar/Nogi.png']
			#Способности пассивные
		self.S0=[];self.SID=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			#Способности активные
		self.SA0=[];self.SAID=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.HP=0
		self.MP=0
		
		#Экипировка персонажа
		self.Equipment=["Пусто","Пусто","Пусто","Пусто","Пусто","Пусто"]
		self.invent=["Правая рука","Левая рука","Голова","Торс","Руки","Ноги"]
		self.inventID=["000","000","000","000","000","000"]
		self.meshok=[]
		self.meshokID=[]
		self.weapon="Отсутствует"
		self.func="Игра"
		self.init=0
		self.m.entryconfig('Персонаж',state="disabled")
		self.fm.delete(0,4)
		self.fm.add_command(label="Новая игра",command=self.new_game)
		self.fm.add_command(label="Загрузить",command=self.load)
		self.fm.add_command(label="Выход",command=self.quitgame)
		
		self.newprinttex("Введите ваше имя")
		self.newprintCSSt(" ")
		self.newprintstat(" ")
		self.images('Data/img/Create.png')
		self.id=0
		self.f=open('Data/WeaArmListtime.data', 'w')
		self.f.close()
		self.RangeHero=1

	def Game(self, event): #Сама игра Дописаь что продолжить 1)Продолжить
		if self.sounds==1:
			self.clicking()
		if self.DelayCommand==0:
			None
		else: 
			self.DelayCommand=0
			self.CSS=self.ent.get()
			self.ent.delete(0,END)
			try:
				if self.FHP<self.HP:
					self.HP=self.FHP
				if self.FMP<self.MP:
					self.MP=self.FMP
			except:
				None
			if self.part>0 and self.init==0:
				self.init=1
				self.m.entryconfig('Персонаж',state="normal")
				self.fm.delete(0,2)
				self.fm.add_command(label="Продолжить",command=self.prodoljit) #формируется список команд пункта меню
				self.fm.add_command(label="Новая игра",command=self.new_game)
				self.fm.add_command(label="Сохранить",command=self.save)
				self.fm.add_command(label="Загрузить",command=self.load)
				self.fm.add_command(label="Выход",command=self.quitgame)
			self.FS=self.S+self.AS[0]; self.FM=self.M+self.AM[0]; self.FA=self.A+self.AA[0]; self.FH=self.H+self.AH[0]; self.FHP=self.FH*5; self.FMP=self.FM*5 ; self.TeloFHP=[self.FHP*0.5,self.FHP*0.7,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35]
			if self.CSS[:6]=="dropme": #читы
				print("Чит сработал")
				self.drop(int(self.CSS[6:]))
			elif self.CSS=="odminexp":
				print("Чит сработал")
				self.exp=self.expup
			if self.weapon=="power":
				self.uron=round((self.atk[0]+self.atkp)*(self.FS*0.08+self.FA*0.06+self.FM*0.04))
			elif self.weapon=="agility":
				self.uron=round((self.atk[0]+self.atkp)*(self.FA*0.08+self.FM*0.06+self.FS*0.04))
			elif self.weapon=="magic":
				self.uron=round((self.atk[0]+self.atkp)*(self.FM*0.08+self.FS*0.06+self.FA*0.04))
			if self.func=="Игра":
				if self.part==0:
					self.locatCur="Создание персонажа"
					if self.path==0:
						if self.CSS=="":
							self.newprinttex("Введите правильное имя") #Обозначается текст
						else:
							self.name=str(self.CSS)
							self.newprinttex("Выберите способ созданиия персонажа") #Обозначается текст
							self.newprintCSSt("1)Вручную\n2)Шаблон") #Обозначаются действия
							self.path=1 # Задаётся метка с действиями в данном случае self.path 1
					elif self.path==1: #Действия в локации
						if self.CSS=="1": #Если выберет 1
							self.func="Прокачка персонажа"
							self.cor=1
							self.classimg='Data\img\Create.png'
							self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP)
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру") 
						elif self.CSS=="2": #Если выберет 2
							self.newprinttex("Какой класс ты желаешь выбрать?")
							self.newprintCSSt("Сила: 01)Варвар, 02)Воин, 03)Паладин\nЛовкость: 11)Вор, 12)Убийца, 13)Самурай\nМудрость: \nМаги: 211)Маг огня, 212)Маг воды, 213)Маг земли, 214)Маг воздуха \n22)Монах, \nБоевые Маги: 231)Маг огня, 232)Маг воды, 233)Маг земли, 234)Маг воздуха")
							self.path=2
					elif self.path==2:
						if self.CSS=="01":
							self.images("Data/img/Classes/Barbarian.png")
							self.classimg="Data/img/Classes/Barbarian.png"
							self.classnamew="Варвар"
							self.Sw=15
							self.Aw=5
							self.Mw=3
							self.Hw=7
							self.Sp1=4
							self.Sp2=12
							self.Sp3=21
							self.Spas1="Двуручные топоры"
							self.Spas2="Средняя броня"
							self.Spas3="Критический удар"
							self.weaponw="power"
							self.textes="Варвары это северный народ. Их сила и выносливость порой заставляют трепетать. Правда непонятно трепет это от воодушивления или от страха."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nДвуручные топоры, Средняя броня, Критический удар"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="02":
							self.images("Data\img\Classes\Warior.png")
							self.classimg="Data\img\Classes\Warior.png"
							self.classnamew="Воин"
							self.Sw=11
							self.Aw=8
							self.Mw=4
							self.Hw=7
							self.Sp1=1
							self.Sp2=9
							self.Sp3=13
							self.Spas1="Одноручные мечи"
							self.Spas2="Тяжёлая броня"
							self.Spas3="Щиты"
							self.weaponw="power"
							self.textes="Воины это бравые солдаты наполняющие все окружающие нас земли. Много кого можно назвать войном однако истинные из них обладают невероятным умением управлятся с мечом и щитом."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nОдноручные мечи, Тяжёлая броня, Щиты"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="03":
							self.images("Data\img\Classes\Palad.png")
							self.classimg="Data\img\Classes\Palad.png"
							self.classnamew="Паладин"
							self.Sw=11
							self.Aw=4
							self.Mw=4
							self.Hw=11
							self.Sp1=1
							self.Sp2=3
							self.Sp3=10
							self.Spas1="Одноручные булавы"
							self.Spas2="Тяжёлая броня"
							self.Spas3="Башенные щиты"
							self.weaponw="power"
							self.textes="Паладины это воины защитники из крепости Хеймволл. Они их обучали сражению против магических существ поэтому на их крепкость духа и выдержку можно положиться."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nОдноручные булавы, Тяжёлая броня, Башенные щиты"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="11":
							self.classnamew="Вор"
							self.images("Data\img\Classes\Theft.png")
							self.classimg="Data\img\Classes\Theft.png"
							self.Sw=8
							self.Aw=11
							self.Mw=5
							self.Hw=6
							self.Sp1=20
							self.Sp2=22
							self.Sp3=28
							self.Spas1="Кинжалы"
							self.Spas2="Вскрытие замков"
							self.Spas3="Скрытность"
							self.weaponw="agility"
							self.textes="Воры это та прожилка общества которая способна проникнуть куда угадно и когда угодно, хотя и неплохо управляется с ножами."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nКинжалы, Вскрытие замков, Скрытность"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="12":
							self.images("Data\img\Classes\Killer.png")
							self.classimg="Data\img\Classes\Killer.png"
							self.classnamew="Убийца"
							self.Sw=9
							self.Aw=13
							self.Mw=3
							self.Hw=5
							self.Sp1=26
							self.Sp2=28
							self.Sp3=21
							self.Spas1="Критический удар"
							self.Spas2="Кинжалы"
							self.Spas3="Парирование"
							self.weaponw="agility"
							self.textes="Специально обученные подразделения Тёмной руки никогда не оставляют свою жертву в живых. Специализируются на тайных операциях."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nКинжалы, Парирование, Критический удар"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="13":
							self.images("Data\img\Classes\Samurai.png")
							self.classimg="Data\img\Classes\Samurai.png"
							self.classnamew="Самурай"
							self.Sw=7
							self.Aw=13
							self.Mw=5
							self.Hw=5
							self.Sp1=29
							self.Sp2=11
							self.Sp3=21
							self.Spas1="Катаны"
							self.Spas2="Критический удар"
							self.Spas3="Лёгкая броня"
							self.weaponw="agility"
							self.textes="Самураи это воины прешедшие с дальнего востока легенды которые ходят об их мастерстве владения катаной очень часто оправдывают себя в битве."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nКатаны, Критический удар, Лёгкая броня"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="211":
							self.images("Data\img\Classes\Mag.png")
							self.classimg="Data\img\Classes\Mag.png"
							self.classnamew="Маг огня"
							self.Sw=4
							self.Aw=4
							self.Mw=15
							self.Hw=7
							self.Sp1=7
							self.Sp2=14
							self.Sp3=19
							self.Spas1="Чтение свитков"
							self.Spas2="Скипетры"
							self.Spas3="Магия огня"
							self.weaponw="magic"
							self.textes="Маги это люди рождённые и открывшие в себе Дар. Это магическая энергия неизвестного происхождения но нашедшая достойное прменение в обществе. Маги годами обучаются в одной из четырёх школ: Игнитус, Аквасис, Террамус или Аэркус."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nЧтение свитков, Скипетры, Магия огня"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="212":
							self.images("Data\img\Classes\Mag.png")
							self.classimg="Data\img\Classes\Mag.png"
							self.classnamew="Маг воды"
							self.Sw=4
							self.Aw=4
							self.Mw=15
							self.Hw=7
							self.Sp1=7
							self.Sp2=17
							self.Sp3=19
							self.Spas1="Чтение свитков"
							self.Spas2="Скипетры"
							self.Spas3="Магия воды"
							self.weaponw="magic"
							self.textes="Маги это люди рождённые и открывшие в себе Дар. Это магическая энергия неизвестного происхождения но нашедшая достойное прменение в обществе. Маги годами обучаются в одной из четырёх школ: Игнитус, Аквасис, Террамус или Аэркус."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nЧтение свитков, Скипетры, Магия воды"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="213":
							self.images("Data\img\Classes\Mag.png")
							self.classimg="Data\img\Classes\Mag.png"
							self.classnamew="Маг земли"
							self.Sw=4
							self.Aw=4
							self.Mw=15
							self.Hw=7
							self.Sp1=7
							self.Sp2=15
							self.Sp3=19
							self.Spas1="Чтение свитков"
							self.Spas2="Скипетры"
							self.Spas3="Магия земли"
							self.weaponw="magic"
							self.textes="Маги это люди рождённые и открывшие в себе Дар. Это магическая энергия неизвестного происхождения но нашедшая достойное прменение в обществе. Маги годами обучаются в одной из четырёх школ: Игнитус, Аквасис, Террамус или Аэркус."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nЧтение свитков, Скипетры, Магия земли"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="214":
							self.images("Data\img\Classes\Mag.png")
							self.classimg="Data\img\Classes\Mag.png"
							self.classnamew="Маг воздуха"
							self.Sw=4
							self.Aw=4
							self.Mw=15
							self.Hw=7
							self.Sp1=7
							self.Sp2=16
							self.Sp3=19
							self.Spas1="Чтение свитков"
							self.Spas2="Скипетры"
							self.Spas3="Магия воздуха"
							self.weaponw="magic"
							self.textes="Маги это люди рождённые и открывшие в себе Дар. Это магическая энергия неизвестного происхождения но нашедшая достойное прменение в обществе. Маги годами обучаются в одной из четырёх школ: Игнитус, Аквасис, Террамус или Аэркус."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nЧтение свитков, Скипетры, Магия воздуха"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="22":
							self.images("Data\img\Classes\Monah.png")
							self.classimg="Data\img\Classes\Warmage.png"
							self.classnamew="Монах"
							self.Sw=5
							self.Aw=9
							self.Mw=10
							self.Hw=7
							self.Sp1=6
							self.Sp2=19
							self.Sp3=27
							self.Spas1="Боевые посохи"
							self.Spas2="Чтение свитков"
							self.Spas3="Дух"
							self.weaponw="magic"
							self.textes="Монахи после длительного обучения спускаются к нам с монастырей расположеных в местах где когда то давно обитали существа обладающие большой магической энергией. Монахи не обладают Даром они используют дух и мантры, а также боевые искуства для ведения боя."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nБоевые посохи, Чтение свитков, Дух"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="231":
							self.images("Data\img\Classes\Warmage.png")
							self.classimg="Data\img\Classes\Warmage.png"
							self.classnamew="Боевой маг огня"
							self.Sw=10
							self.Aw=4
							self.Mw=9
							self.Hw=7
							self.Sp1=1
							self.Sp2=12
							self.Sp3=14
							self.Spas1="Средняя броня"
							self.Spas2="Одноручные мечи"
							self.Spas3="Магия огня"
							self.weaponw="magic"
							self.textes="Боевые маги это особые подразделения которые являются обладателями Дара, но кроме чтения книг они были обучены превосходному владению мечом."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nСредняя броня, Одноручные мечи, Магия огня"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="232":
							self.images("Data\img\Classes\Warmage.png")
							self.classimg="Data\img\Classes\Warmage.png"
							self.classnamew="Боевой маг воды"
							self.Sw=10
							self.Aw=4
							self.Mw=9
							self.Hw=7
							self.Sp1=1
							self.Sp2=12
							self.Sp3=17
							self.Spas1="Средняя броня"
							self.Spas2="Одноручные мечи"
							self.Spas3="Магия воды"
							self.weaponw="magic"
							self.textes="Боевые маги это особые подразделения которые являются обладателями Дара, но кроме чтения книг они были обучены превосходному владению мечом."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nСредняя броня, Одноручные мечи, Магия воды"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="233":
							self.images("Data\img\Classes\Warmage.png")
							self.classimg="Data\img\Classes\Warmage.png"
							self.classnamew="Боевой маг земли"
							self.Sw=10
							self.Aw=4
							self.Mw=9
							self.Hw=7
							self.Sp1=1
							self.Sp2=12
							self.Sp3=15
							self.Spas1="Средняя броня"
							self.Spas2="Одноручные мечи"
							self.Spas3="Магия земли"
							self.weaponw="magic"
							self.textes="Боевые маги это особые подразделения которые являются обладателями Дара, но кроме чтения книг они были обучены превосходному владению мечом."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nСредняя броня, Одноручные мечи, Магия земли"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
						elif self.CSS=="234":
							self.images("Data\img\Classes\Warmage.png")
							self.classimg="Data\img\Classes\Warmage.png"
							self.classnamew="Боевой маг воздуха"
							self.Sw=10
							self.Aw=4
							self.Mw=9
							self.Hw=7
							self.Sp1=1
							self.Sp2=12
							self.Sp3=16
							self.Spas1="Средняя броня"
							self.Spas2="Одноручные мечи"
							self.Spas3="Магия воздуха"
							self.weaponw="magic"
							self.textes="Боевые маги это особые подразделения которые являются обладателями Дара, но кроме чтения книг они были обучены превосходному владению мечом."
							self.textes+="\nХарактеристики: \nСила:" + str(self.Sw) +"\nЛовкость: " + str(self.Aw) + "\nМудрость: " + str(self.Mw) + "\nВыносливость: " + str(self.Hw)
							self.textes+="\nПассивные способности:\nСредняя броня, Одноручные мечи, Магия воздуха"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаешь ли ты выбрать этот класс? \n1)Да\n2)Нет")
							self.path=3
					elif self.path==3:
						if self.CSS=="1":
							self.classname=self.classnamew
							self.S=self.Sw
							self.A=self.Aw
							self.M=self.Mw
							self.H=self.Hw
							self.P=0
							self.SP=0
							self.SID[self.Sp1]=1
							self.SID[self.Sp2]=1
							self.SID[self.Sp3]=1
							self.S0.append(self.Spas1)
							self.S0.append(self.Spas2)
							self.S0.append(self.Spas3)
							self.weapon=self.weaponw
							self.FHP = self.H * 5
							self.FMP = self.M * 5
							self.HP=self.FHP
							self.TeloFHP = [self.FHP*0.5,self.FHP*0.7,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35]
							self.TeloHP = self.TeloFHP
							self.MP=self.FMP
							self.path=2
							self.part=1
							self.locatCur="Обломки храма"
							self.locatImg='Data\img\Locations\Hram.png'
							self.newprinttex("Вы очнулись на обломках в неизвестном для вас месте, помимо этого вы абсолютно не знаете кто вы и как тут оказались")
							self.newprintCSSt("Продолжить")
							self.images(self.locatImg)
							self.safy=1
						elif self.CSS=="2":
							self.newprinttex("Выберите способ созданиия персонажа")
							self.newprintCSSt("1)Вручную\n2)Шаблон")
							self.part=0
							self.path=1
							self.images('Data\img\Create.png')
					elif self.path==4:
						self.FHP = self.H * 5
						self.TeloFHP = [self.FHP*0.5,self.FHP*0.7,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35,self.FHP*0.35]
						self.FMP = self.M * 5
						self.HP=self.FHP
						self.TeloHP = self.TeloFHP
						self.MP=self.FMP
						self.part=1
						self.path=2
						self.safy=1
						self.locatImg='Data\img\Locations\Hram.png'
						self.locatDisc="Вы очнулись на обломках в неизвестном для вас месте, помимо этого вы абсолютно не знаете кто вы и как тут оказались"
						self.locatCSS="Продолжить"
						self.locatCur="Обломки храма"
						self.newprinttex(self.locatDisc)
						self.newprintCSSt(self.locatCSS)
						self.images(self.locatImg)
				elif self.part==1:
					if self.path==0:
						self.newprinttex("Падая на холодную землю последней мыслю было как мало вы узнали и как много вы не узнаете")
						self.newprintCSSt("Нажмите Enter чтобы продолжить")
					if self.exp==self.expup or self.exp>self.expup:
						self.lvl+=1
						self.HP=self.FHP
						self.MP=self.FMP
						self.expup=self.lvl*400*1.5
						self.P+=5
						if self.lvl%3==0:
							self.SP+=1
							self.SAP+=1
						self.textes="Поздравляю ваш уровень повышен и теперь он составляет "+ str(self.lvl) +"!\n"
						self.textes+=self.locatDisc
						self.newprinttex(self.textes)
						self.newprintCSSt(self.locatCSS)
					elif random.randint(1,100)>20 and self.safy==0: #Изменил
						self.newprinttex("Вы попали в бой")
						self.newprintCSSt("Продолжить")
						self.func="Бой"
						self.cor=0
					elif self.path==2:
						self.locatImg='Data\img\Locations\Hram.png'
						self.locatCur="Обломки храма"
						self.locatDisc="Вы находитесь в храме"
						self.locatCSS="1)Отдохнуть\n2)Покинуть обломки"
						self.newprinttex(self.locatDisc)
						self.newprintCSSt(self.locatCSS)
						self.images(self.locatImg)
						self.path=3
						self.safy = 1
					elif self.path==3: #Обломки храма
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Hram.png'
							self.locatCur="Обломки храма"
							self.HP=self.FHP
							self.MP=self.FMP
							self.TeloHP=self.TeloFHP
							self.locatDisc="Вы отдохнули\nВы находитесь в храме"
							self.locatCSS="1)Отдохнуть\n2)Покинуть обломки"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.safy = 1
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\Les1.gif'
							self.locatCur="Дорога в храм"
							self.locatDisc="Вы находитесь на дороге неподалёку от обломков на тропе которая ведёт прямо в даль."
							self.locatCSS="1)Идти в храм\n2)Идти дальше"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=4
							self.safy = 0
					elif self.path==4: #Дорога в храм
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Hram.png'
							self.locatCur="Обломки храма"
							self.locatDisc="Вы находитесь в храме"
							self.locatCSS="1)Отдохнуть\n2)Покинуть обломки"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=3
							self.safy = 1
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\Razvilka.gif'
							self.locatCur="Развилка"
							self.locatDisc="Вы прошли дальше по тропе и обнаружили разветвление на два пути. Между ними стоит указатель: в одну сторону храм, во вторую деревня Зайра и третий путь табличка повреждена и неразборчива."
							self.locatCSS="1)Вернуться на дорогу в храм\n2)Идти в деревню\n3)Идти в " + locat1
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=5
							self.safy = 0
					elif self.path==5: #Развилка
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Les1.gif'
							self.locatCur="Дорога в храм"
							self.locatDisc="Вы находитесь на дороге неподалёку от обломков на тропе которая ведёт прямо в даль."
							self.locatCSS="1)Идти в храм\n2)Идти дальше"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=4
							self.safy = 0
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\CenterVilage.gif'
							self.locatCur="Деревня Зайра"
							self.locatDisc="Вы пришли в деревню. На улице пусто и нет ниодного человека в поле зрения."
							self.locatCSS="1)Вернуться назад\n2)Идти в центр города\n3)Зайти в дом"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=6
							self.safy = 0
						elif self.CSS=="3":
							self.locatImg='Data\img\Locations\les1.gif'
							self.textes="Дорога в " + self.locat1
							self.locatCur=self.textes
							self.locatDisc="Вы прошли несколько километров по дороге и с каждым вашим шагом кроны деревьев всё больше заслоняют небо"
							self.locatCSS="1)Вернуться на развилку\n2)Идти дальше"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=7
							self.safy = 0
					elif self.path==6: #Деревня 1
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Razvilka.gif'
							self.locatCur="Развилка"
							self.locatDisc="Вы прошли дальше по тропе и обнаружили разветвление на два пути. Между ними стоит указатель: в одну сторону храм, во вторую деревня Зайра и третий путь табличка повреждена и неразборчива."
							self.locatCSS="1)Вернуться на дорогу в храм\n2)Идти в деревню\n3)Идти в " + self.locat1
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=5
							self.safy = 0
					elif self.path==7: #Дорога в неизвестность
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Razvilka.gif'
							self.locatCur="Развилка"
							self.locatDisc="Вы прошли дальше по тропе и обнаружили разветвление на два пути. Между ними стоит указатель: в одну сторону храм, во вторую деревня Зайра и третий путь табличка повреждена и неразборчива."
							self.locatCSS="1)Вернуться на дорогу в храм\n2)Идти в деревню\n3)Идти в " + self.locat1
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=5
							self.safy = 0
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\les1.gif'
							self.localCur="Неизвестный тракт"
							self.locatDisc="Пройдя несколько ярдов по заброшенной и неизвестной дороге, вас начинает терзасть странное чувства, как будто вы здесь уже бывали..."
							self.locatCSS="1)Вернуться к развилке\n2)Идти дальше"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=8
							self.safy = 0
					elif self.path==8: #Старый тракт
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\Razvilka.gif'
							self.locatCur="Развилка"
							self.locatDisc="Вы прошли дальше по тропе и обнаружили разветвление на два пути. Между ними стоит указатель: в одну сторону храм, во вторую деревня Зайра и третий путь табличка повреждена и неразборчива."
							self.locatCSS="1)Вернуться на дорогу в храм\n2)Идти в деревню\n3)Идти в " + self.locat1
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=5
							self.safy = 0
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\les1.gif'
							self.locatCur="Старый тракт"
							self.locatDisc="Вы, кажется, впервые на этой дороге, но неожиданный образ небольшой деревни вдруг всплыл в вашей памяти. Вы почему-то были уверены, что , пройдя еще немного, окажетесь в соседней деревне"
							self.locatCSS="1)Вернуться к началу тракта\n2)Идти в деревню"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=9
							self.safy = 0
					elif self.path==9: #Деревня Старые Луки
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\les1.gif'
							localcur="Неизвестный тракт"
							self.locatDisc="Пройдя несколько ярдов по заброшенной и неизвестной дороге, вас начинает терзать странное чувство, как будто вы здесь уже бывали..."
							self.locatCSS="1)Вернуться к развилке\n2)Идти дальше"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=7
							self.safy = 0
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\CenterVilage.gif'
							self.locatCur="Старые Луки"
							self.locatDisc="Неизвестная деревня оказалась до боли знакомой, но могильная тишина пугала до дрожи в коленях. Пустые глазницы окон пронзительно смотрели на вас. Особенно удивляло полное отсутсвие людей, как будто они исчезли в один миг, не успев закончить текущих дел...Тут стоило осмотреться"
							self.locatCSS="1)Вернуться на тракт\n2)Зайти в ближайший дом\n3)Выйти на рыночную площадь"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=10
							self.safy=1
					elif self.path==10: #Старые Луки
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\les1.gif'
							self.locatCur="Старый тракт"
							self.locatDisc="Вы, кажется, впервые на этой дороге, но неожиданный образ небольшой деревни вдруг всплыл в вашей памяти. Вы почему-то были уверены, что , пройдя еще немного, окажетесь в соседней деревне"
							self.locatCSS="1)Вернуться к началу тракта\n2)Идти в деревню"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=9
							self.safy = 0
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\DomVnutri.gif'
							self.locatCur="Небольшой дом"
							self.locatDisc="Этот дом явно принадлежал богатому крестьянину или родственнику Кума, главы деревни. Все выглядело, как будто хозяева вышли мгновенье назад..."
							self.locatCSS="1)Отдохнуть\n2)Покинуть дом"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=11
							self.safy = 1
						elif self.CSS=="3":
							self.locatImg='Data\img\Locations\CenterVilage.gif'
							self.locatCur="Рыночная площадь"
							self.locatDisc="Выйдя на рыночную площадь, вы заметили кучу лавок, теснящихся рядом друг с другом: кузнеца, рыболова и прочих. Вроде, тут в каждый праздник Новоцвета бывал настоящих волшебник из Цитадели... Откуда я это знаю?"
							self.locatCSS="1)Покинуть площадь"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=12
							self.safy = 0
					elif self.path==11: #Дом	
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\DomVnutri.gif'
							self.locatCur="Небольшой дом"
							self.HP=self.FHP
							self.MP=self.FMP
							self.locatDisc="Вы отдохнули\nВы находитесь в деревенском доме"
							self.locatCSS="1)Отдохнуть\n2)Покинуть дом"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.safy=1
						elif self.CSS=="2":
							self.locatImg='Data\img\Locations\CenterVilage.gif'
							self.locatCur="Старые Луки"
							self.locatDisc="Неизвестная деревня оказалась до боли знакомой, но могильная тишина пугала до дрожи в коленях. Пустые глазницы окон пронзительно смотрели на вас. Особенно удивляло полное отсутсвие людей, как будто они исчезли в один миг, не успев закончить текущих дел...Тут стоило осмотреться"
							self.locatCSS="1)Вернуться на тракт\n2)Зайти в ближайший дом\n3)Выйти на рыночную площадь"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=10
							self.safy=0
					elif self.path==12: #Рыночная площадь
						if self.CSS=="1":
							self.locatImg='Data\img\Locations\CenterVilage.gif'
							self.locatCur="Старые Луки"
							self.locatDisc="Неизвестная деревня оказалась до боли знакомой, но могильная тишина пугала до дрожи в коленях. Пустые глазницы окон пронзительно смотрели на вас. Особенно удивляло полное отсутсвие людей, как будто они исчезли в один миг, не успев закончить текущих дел...Тут стоило осмотреться"
							self.locatCSS="1)Вернуться на тракт\n2)Зайти в ближайший дом\n3)Выйти на рыночную площадь"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.path=10
							self.safy=1
			elif self.func=="Инвентарь":
				self.balPRuka.bind(self.Pruka, self.balpruka)
				self.balLRuka.bind(self.Lruka, self.ballruka)
				self.balGolova.bind(self.Golova, self.balgolova)
				self.balTors.bind(self.Tors, self.baltors)
				self.balRuki.bind(self.Ruki, self.balruki)
				self.balNogi.bind(self.Nogi, self.balnogi)
				self.AS[0]=self.AS[1]+self.AS[2]+self.AS[3]+self.AS[4]+self.AS[5]+self.AS[6]; self.AM[0]=self.AM[1]+self.AM[2]+self.AM[3]+self.AM[4]+self.AM[5]+self.AM[6]; self.AA[0]=self.AA[1]+self.AA[2]+self.AA[3]+self.AA[4]+self.AA[5]+self.AA[6]; self.AH[0]=self.AH[1]+self.AH[2]+self.AH[3]+self.AH[4]+self.AH[5]+self.AH[6]
				self.FireRes[0]=self.FireRes[1]+self.FireRes[2]+self.FireRes[3]+self.FireRes[4]+self.FireRes[5]+self.FireRes[6]; self.WaterRes[0]=self.WaterRes[1]+self.WaterRes[2]+self.WaterRes[3]+self.WaterRes[4]+self.WaterRes[5]+self.WaterRes[6]
				self.EarthRes[0]=self.EarthRes[1]+self.EarthRes[2]+self.EarthRes[3]+self.EarthRes[4]+self.EarthRes[5]+self.EarthRes[6]; self.AirRes[0]=self.AirRes[1]+self.AirRes[2]+self.AirRes[3]+self.AirRes[4]+self.AirRes[5]+self.AirRes[6]
				self.PhisRes[0]=self.PhisRes[1]+self.PhisRes[2]+self.PhisRes[3]+self.PhisRes[4]+self.PhisRes[5]+self.PhisRes[6]; self.BleedRes[0]=self.BleedRes[1]+self.BleedRes[2]+self.BleedRes[3]+self.BleedRes[4]+self.BleedRes[5]+self.BleedRes[6]
				self.PoisRes[0]=self.PoisRes[1]+self.PoisRes[2]+self.PoisRes[3]+self.PoisRes[4]+self.PoisRes[5]+self.PoisRes[6]; 
				self.Block[0]=self.Block[1]+self.Block[2]+self.Block[3]+self.Block[4]+self.Block[5]+self.Block[6];self.Dodge[0]=self.Dodge[1]+self.Dodge[2]+self.Dodge[3]+self.Dodge[4]+self.Dodge[5]+self.Dodge[6]
				self.FS=self.S+self.AS[0]; self.FM=self.M+self.AM[0]; self.FA=self.A+self.AA[0]; self.FH=self.H+self.AH[0]; self.FHP=self.FH*5; self.FMP=self.FM*5
				if self.weapon=="power":
					self.uron=round((self.atk[0]+self.atkp)*(self.FS*0.08+self.FA*0.06+self.FM*0.04))
				elif self.weapon=="agility":
					self.uron=round((self.atk[0]+self.atkp)*(self.FA*0.08+self.FM*0.06+self.FS*0.04))
				elif self.weapon=="magic":
					self.uron=round((self.atk[0]+self.atkp)*(self.FM*0.08+self.FS*0.06+self.FA*0.04))
				if self.cor==1: #Выбор предмета чтобы надеть
					if self.CSS=="0":
						self.func="Игра"
						self.images(self.locatImg)
						self.newprinttex(self.locatDisc)
						self.newprintCSSt(self.locatCSS)
						self.Tors.destroy()
						self.Pruka.destroy()
						self.Lruka.destroy()
						self.Golova.destroy()
						self.Ruki.destroy()
						self.Nogi.destroy()
					elif self.CSS!="0":
						self.TempItemNAME=0;self.TempItemITTP=0;self.TempItemMSTN=0;self.TempItemLVLN=0;self.TempItemATTP=0;self.TempItemATCK=0;self.TempItemMNMC=0
						self.TempItemEART=0;self.TempItemWIND=0;self.TempItemBLED=0;self.TempItemPOIS=0;self.TempItemPHIS=0;self.TempItemFIRE=0;self.TempItemWATR=0
						self.TempItemBLCK=0;self.TempItemDODG=0;self.TempItemPOWR=0;self.TempItemMIND=0;self.TempItemAGIL=0;self.TempItemHELT=0;self.TempItemMNMG=0
						self.TempItemCTRL=0
						try:
							self.CSS2=self.CSS
							self.y=self.meshokID[int(self.CSS2)-1]
							self.WeaArmList=open('Data\\WeaArmListtime.data','r', encoding='utf8')
							self.WeanArmListVar=self.WeaArmList.readlines()
							self.OpedeleniePredmeta=0
							self.i=0
							if self.y[2:3]=="N":
								self.MestoPredmeta=6
							elif self.y[2:3]=="R":
								self.MestoPredmeta=5
							elif self.y[2:3]=="G":
								self.MestoPredmeta=3	
							elif self.y[2:3]=="T":
								self.MestoPredmeta=4
							elif self.y[2:3]=="P":
								self.MestoPredmeta=1	
							elif self.y[2:3]=="L":
								self.MestoPredmeta=2	
							while self.OpedeleniePredmeta!=1:
								self.strokalista=self.WeanArmListVar[self.i].strip()
								if self.y==self.strokalista[6:]:
									self.TempItemITID=self.strokalista[6:]
									while True:
										self.strokalista=self.WeanArmListVar[self.i].strip()
										if self.strokalista=="STOP":
											self.OpedeleniePredmeta=1
											break
										elif self.strokalista[:4]=="NAME":
											self.TempItemNAME=self.strokalista[6:]
										elif self.strokalista[:4]=="IIMG":
											self.TempItemIIMG=self.strokalista[6:]
										elif self.strokalista[:4]=="ITTP":
											self.TempItemITTP=self.strokalista[6:]
										elif self.strokalista[:4]=="MSTN":
											self.TempItemMSTN=int(self.strokalista[6:])
										elif self.strokalista[:4]=="LVLN":
											self.TempItemLVLN=int(self.strokalista[6:])
										elif self.strokalista[:4]=="ATTP":
											self.TempItemATTP=self.strokalista[6:]
										elif self.strokalista[:4]=="ATCK":
											self.TempItemATCK=int(self.strokalista[6:])
										elif self.strokalista[:4]=="PHIS":
											self.TempItemPHIS=int(self.strokalista[6:])
										elif self.strokalista[:4]=="FIRE":
											self.TempItemFIRE=int(self.strokalista[6:])
										elif self.strokalista[:4]=="WATR":
											self.TempItemWATR=int(self.strokalista[6:])
										elif self.strokalista[:4]=="EART":
											self.TempItemEART=int(self.strokalista[6:])
										elif self.strokalista[:4]=="WIND":
											self.TempItemWIND=int(self.strokalista[6:])
										elif self.strokalista[:4]=="BLED":
											self.TempItemBLED=int(self.strokalista[6:])
										elif self.strokalista[:4]=="POIS":
											self.TempItemPOIS=int(self.strokalista[6:])
										elif self.strokalista[:4]=="CTRL":
											self.TempItemCTRL=int(self.strokalista[6:])
										elif self.strokalista[:4]=="BLCK":
											self.TempItemBLCK=int(self.strokalista[6:])
										elif self.strokalista[:4]=="DODG":
											self.TempItemDODG=int(self.strokalista[6:])
										elif self.strokalista[:4]=="POWR":
											self.TempItemPOWR=int(self.strokalista[6:])
										elif self.strokalista[:4]=="MIND":
											self.TempItemMIND=int(self.strokalista[6:])
										elif self.strokalista[:4]=="AGIL":
											self.TempItemAGIL=int(self.strokalista[6:])
										elif self.strokalista[:4]=="HELT":
											self.TempItemHELT=int(self.strokalista[6:])
										elif self.strokalista[:4]=="MNMG":
											self.TempItemMNMG=int(self.strokalista[6:])
										elif self.strokalista[:4]=="MNMC":
											self.TempItemMNMC=int(self.strokalista[6:])
										self.i+=1
								self.i+=1
							self.WeaArmList.close()
							self.textes=str(self.TempItemNAME) + " | " + str(self.invent[self.MestoPredmeta-1]) + "\nТип предмета: " + str(self.TempItemITTP) + "|" + str(self.Equipment[self.MestoPredmeta-1]) + "\n"
							if self.TempItemMSTN!=0 or self.MSTN[self.MestoPredmeta]!=0:
								self.textes+="Нужный уровень мастерства: " + str(self.TempItemMSTN) + " | " + str(self.MSTN[self.MestoPredmeta]) + "\n"
							if self.TempItemLVLN!=0 or self.LVLN[self.MestoPredmeta]!=0:
								self.textes+="Нужный уровень: " + str(self.TempItemLVLN) + " | " + str(self.LVLN[self.MestoPredmeta]) + "\n"
							if self.TempItemATTP!=0:
								self.textes+="Основная характеристика: " + str(self.TempItemATTP) + " | " + str(self.weapon) + "\n"
							if self.TempItemATCK!=0 or self.atk[self.MestoPredmeta]!=0:
								self.textes+="Атака: " + str(self.TempItemATCK) + " | " + str(self.atk[self.MestoPredmeta]) + "\n"
							if self.TempItemPHIS!=0 or self.PhisRes[self.MestoPredmeta]!=0:
								self.textes+="Броня: " + str(self.TempItemPHIS) + " | " + str(self.PhisRes[self.MestoPredmeta]) + "\n"
							if self.TempItemDODG!=0 or self.Dodge[self.MestoPredmeta]!=0:
								self.textes+="Уворот: " + str(self.TempItemDODG) + " | " + str(self.Dodge[self.MestoPredmeta]) + "\n"
							if self.TempItemBLCK!=0 or self.Block[self.MestoPredmeta]!=0:
								self.textes+="Блок: " + str(self.TempItemBLCK) + " | " + str(self.Block[self.MestoPredmeta]) + "\n"
							if self.TempItemFIRE!=0 or self.FireRes[self.MestoPredmeta]!=0 or self.TempItemWATR!=0 or self.WaterRes[self.MestoPredmeta]!=0 or self.TempItemEART!=0 or self.EarthRes[self.MestoPredmeta]!=0 or self.TempItemWIND!=0 or self.AirRes[self.MestoPredmeta]!=0 or self.TempItemPOIS!=0 or self.PoisRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от нефизического урона:\n"
							if self.TempItemFIRE!=0 or self.FireRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от огня: " + str(self.TempItemFIRE) + " | " + str(self.FireRes[self.MestoPredmeta]) + "\n"
							if self.TempItemWATR!=0 or self.WaterRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от воды: " + str(self.TempItemWATR) + " | " + str(self.WaterRes[self.MestoPredmeta]) + "\n"
							if self.TempItemEART!=0 or self.EarthRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от земли: " + str(self.TempItemEART) + " | " + str(self.EarthRes[self.MestoPredmeta]) + "\n"
							if self.TempItemWIND!=0 or self.AirRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от воздуха: " + str(self.TempItemWIND) + " | " + str(self.AirRes[self.MestoPredmeta]) + "\n"
							if self.TempItemBLED!=0 or self.BleedRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от кровотечения: " + str(self.TempItemBLED) + " | " + str(self.BleedRes[self.MestoPredmeta]) + "\n"
							if self.TempItemPOIS!=0 or self.PoisRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от яда: " + str(self.TempItemPOIS) + " | " + str(self.PoisRes[self.MestoPredmeta]) + "\n"
							if self.TempItemCTRL!=0 or self.ControllRes[self.MestoPredmeta]!=0:
								self.textes+="Защита от контроля: " + str(self.TempItemCTRL) + " | " + str(self.ControllRes[self.MestoPredmeta]) + "\n"
							if self.TempItemPOWR!=0 or self.AS[self.MestoPredmeta]!=0 or self.TempItemMIND!=0 or self.AM[self.MestoPredmeta]!=0 or self.TempItemAGIL!=0 or self.AA[self.MestoPredmeta]!=0 or self.TempItemHELT!=0 or self.AH[self.MestoPredmeta]!=0:
								self.textes+="Основные характеристики: \n"
							if self.TempItemPOWR!=0 or self.AS[self.MestoPredmeta]!=0:
								self.textes+="Сила: " + str(self.TempItemPOWR) + " | " + str(self.AS[self.MestoPredmeta]) + "\n"
							if self.TempItemMIND!=0 or self.AM[self.MestoPredmeta]!=0:
								self.textes+="Разум: " + str(self.TempItemMIND) + " | " + str(self.AM[self.MestoPredmeta]) + "\n"
							if self.TempItemAGIL!=0 or self.AA[self.MestoPredmeta]!=0:
								self.textes+="Ловкость: " + str(self.TempItemAGIL) + " | " + str(self.AA[self.MestoPredmeta]) + "\n"
							if self.TempItemHELT!=0 or self.AH[self.MestoPredmeta]!=0:
								self.textes+="Выносливость: " + str(self.TempItemHELT) + " | " + str(self.AH[self.MestoPredmeta]) + "\n"
							if self.TempItemMNMG!=0 or self.MNMG[self.MestoPredmeta]!=0 or self.TempItemMNMC!=0 or self.MNMC[self.MestoPredmeta]!=0:
								self.textes+="Умения: "
							if self.TempItemMNMG!=0 or self.MNMG[self.MestoPredmeta]!=0:
								self.textes+="Увеличение урона умениями: " + str(self.TempItemMNMG) + " | " + str(self.MNMG[self.MestoPredmeta]) + "\n"
							if self.TempItemMNMC!=0 or self.MNMC[self.MestoPredmeta]!=0:
								self.textes+="Уменьшение затрат ресурса: " + str(self.TempItemMNMC) + " | " + str(self.MNMC[self.MestoPredmeta]) + "\n"
							self.newprinttex(self.textes)
							self.newprintCSSt("Желаете ли вы надеть этот предмет? \n1)Да\n2)Нет\n3)Выкинуть")
							self.cor=2
						except IndexError:
							self.textes="Введите правильный номер\nЭкипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
							self.newprinttex(self.textes)
				elif self.cor==2: #Поддтверждение надетия
					self.nope=0
					if self.CSS=="1":
						self.textes=""
						if self.TempItemITTP=="Одноручный меч" and self.TempItemMSTN>self.SID[1]:
							self.textes+="Вам нужен навык одноручные мечи уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Одноручный топор" and self.TempItemMSTN>self.SID[5]:
							self.textes+="Вам нужен навык одноручные топоры уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Одноручная булава" and self.TempItemMSTN>self.SID[3]:
							self.textes+="Вам нужен навык одноручные булавы уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Скипетр" and self.TempItemMSTN>self.SID[7]:
							self.textes+="Вам нужен навык скипетры уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Кинжал" and self.TempItemMSTN>self.SID[28]:
							self.textes+="Вам нужен навык кинжал уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Двуручный меч" and self.TempItemMSTN>self.SID[0]:
							self.textes+="Вам нужен навык двуручный меч уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Двуручный топор" and self.TempItemMSTN>self.SID[4]:
							self.textes+="Вам нужен навык двуручные топоры уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Двуручная булава" and self.TempItemMSTN>self.SID[2]:
							self.textes+="Вам нужен навык двуручные булавы уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Катана" and self.TempItemMSTN>self.SID[29]:
							self.textes+="Вам нужен навык катаны уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Боевой посох" and self.TempItemMSTN>self.SID[6]:
							self.textes+="Вам нужен навык боевые посохи уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Лёгкая броня" and self.TempItemMSTN>self.SID[11]:
							self.textes+="Вам нужен навык лёгкая броня уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Тяжёлая броня" and self.TempItemMSTN>self.SID[13]:
							self.textes+="Вам нужен навык тяжёлая броня уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Средняя броня" and self.TempItemMSTN>self.SID[12]:
							self.textes+="Вам нужен навык средняя броня уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Щит" and self.TempItemMSTN>self.SID[9]:
							self.textes+="Вам нужен навык щиты уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Башенный щит" and self.TempItemMSTN>self.SID[10]:
							self.textes+="Вам нужен навык щиты уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						elif self.TempItemITTP=="Баклер" and self.TempItemMSTN>self.SID[8]:
							self.textes+="Вам нужен навык щиты уровня: " + str(self.TempItemMSTN) + "\n"
							self.nope=1
						if self.TempItemLVLN>self.lvl:
							self.textes+="Вам нужен уровень: " + str(self.TempItemLVLN) + "\n"
							self.nope=1
						if self.nope==0:
							if self.inventID[self.MestoPredmeta-1]!="000":
								if self.MestoPredmeta==1 or self.MestoPredmeta==2 and self.inventID[self.MestoPredmeta-1]==self.inventID[self.MestoPredmeta]:
									self.meshokID.append(self.inventID[self.MestoPredmeta-1])
									self.meshok.append(self.invent[self.MestoPredmeta-1])
									self.inventID[self.MestoPredmeta]="000";self.inventID[self.MestoPredmeta-1]="000"
								else:
									self.meshokID.append(self.inventID[self.MestoPredmeta-1])
									self.meshok.append(self.invent[self.MestoPredmeta-1])
							if self.TempItemITTP=="Двуручный топор" or self.TempItemITTP=="Двуручная булава" or self.TempItemITTP=="Двуручный меч" or self.TempItemITTP=="Боевой посох" or self.TempItemITTP=="Катана":
								self.invent[self.MestoPredmeta-1]=self.TempItemNAME
								self.inventID[self.MestoPredmeta-1]=self.TempItemITID
								self.Equipment[self.MestoPredmeta-1]=self.TempItemITTP
								self.invent[self.MestoPredmeta]=self.TempItemNAME
								self.inventID[self.MestoPredmeta]=self.TempItemITID
								self.Equipment[self.MestoPredmeta]=self.TempItemITTP
							else:
								self.invent[self.MestoPredmeta-1]=self.TempItemNAME
								self.inventID[self.MestoPredmeta-1]=self.TempItemITID
								self.Equipment[self.MestoPredmeta-1]=self.TempItemITTP
							if self.TempItemATTP=="agility" or self.TempItemATTP=="power" or self.TempItemATTP=="mind":
								self.weapon=self.TempItemATTP
							self.MSTN[self.MestoPredmeta]=self.TempItemMSTN
							self.LVLN[self.MestoPredmeta]=self.TempItemLVLN
							self.atk[self.MestoPredmeta]=self.TempItemATCK
							self.PhisRes[self.MestoPredmeta]=self.TempItemPHIS
							self.Dodge[self.MestoPredmeta]=self.TempItemDODG
							self.Block[self.MestoPredmeta]=self.TempItemBLCK
							self.FireRes[self.MestoPredmeta]=self.TempItemFIRE
							self.WaterRes[self.MestoPredmeta]=self.TempItemWATR
							self.EarthRes[self.MestoPredmeta]=self.TempItemEART
							self.AirRes[self.MestoPredmeta]=self.TempItemWIND
							self.BleedRes[self.MestoPredmeta]=self.TempItemBLED
							self.PoisRes[self.MestoPredmeta]=self.TempItemPOIS
							self.ControllRes[self.MestoPredmeta]=self.TempItemCTRL
							self.AS[self.MestoPredmeta]=self.TempItemPOWR
							self.AM[self.MestoPredmeta]=self.TempItemMIND
							self.AA[self.MestoPredmeta]=self.TempItemAGIL
							self.AH[self.MestoPredmeta]=self.TempItemHELT
							self.MNMG[self.MestoPredmeta]=self.TempItemMNMG
							self.MNMC[self.MestoPredmeta]=self.TempItemMNMC
							self.TempBaloon=""
							if self.invent[self.MestoPredmeta-1]!=0:
								self.TempBaloon+=self.invent[self.MestoPredmeta-1]
							if self.Equipment[self.MestoPredmeta-1]!=0:
								self.TempBaloon+="\nТип: " + str(self.Equipment[self.MestoPredmeta-1])
							if self.MSTN[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nТреб.мастер: " + str(self.MSTN[self.MestoPredmeta])
							if self.LVLN[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nТреб.уровень: " + str(self.LVLN[self.MestoPredmeta])
							if self.TempItemATTP!=0:
								self.TempBaloon+="\nОсновная характеристика: " + str(self.weapon)
							if self.atk[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nАтака: " + str(self.atk[self.MestoPredmeta])
							if self.PhisRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nБроня: " + str(self.PhisRes[self.MestoPredmeta])
							if self.Dodge[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nУворот: " + str(self.Dodge[self.MestoPredmeta])
							if self.Block[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nБлок: " + str(self.Block[self.MestoPredmeta])
							if self.FireRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от огня: " + str(self.FireRes[self.MestoPredmeta])
							if self.WaterRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от воды: " + str(self.WaterRes[self.MestoPredmeta])
							if self.EarthRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от земли: " + str(self.EarthRes[self.MestoPredmeta])
							if self.AirRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от воздуха: " + str(self.AirRes[self.MestoPredmeta])
							if self.BleedRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от кровотечения: " + str(self.BleedRes[self.MestoPredmeta])
							if self.PoisRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от яда: " + str(self.PoisRes[self.MestoPredmeta])
							if self.ControllRes[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЗащита от контроля: " + str(self.ControllRes[self.MestoPredmeta])
							if self.AS[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nСила: " + str(self.AS[self.MestoPredmeta])
							if self.AM[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nРазум: " + str(self.AM[self.MestoPredmeta])
							if self.AA[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nЛовкость: " + str(self.AA[self.MestoPredmeta])
							if self.AH[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nВыносливость: " + str(self.AH[self.MestoPredmeta])
							if self.MNMG[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nУвеличение урона умениями: " + str(self.MNMG[self.MestoPredmeta])
							if self.MNMC[self.MestoPredmeta]!=0:
								self.TempBaloon+="\nУменьшение затрат ресурса: " + str(self.MNMC[self.MestoPredmeta])
							if self.y[2:3]=="N":
								self.balnogi=self.TempBaloon
							elif self.y[2:3]=="R":
								self.balruki=self.TempBaloon
							elif self.y[2:3]=="G":
								self.balgolova=self.TempBaloon
							elif self.y[2:3]=="T":
								self.baltors=self.TempBaloon
							elif self.y[2:3]=="P":
								if self.TempItemITTP=="Катана" or self.TempItemITTP=="Боевой посох" or self.TempItemITTP=="Двуручный меч" or self.TempItemITTP=="Двуручный топор" or self.TempItemITTP=="Двуручная булава":
									self.balpruka=self.TempBaloon
									self.ballruka=self.TempBaloon
								else:
									self.balpruka=self.TempBaloon
							elif self.y[2:3]=="L":
								self.ballruka=self.TempBaloon	
							self.balPRuka.bind(self.Pruka, self.balpruka)
							self.balLRuka.bind(self.Lruka, self.ballruka)
							self.balGolova.bind(self.Golova, self.balgolova)
							self.balRuki.bind(self.Ruki, self.balruki)
							self.balNogi.bind(self.Nogi, self.balnogi)
							self.balTors.bind(self.Tors, self.baltors)
							if self.MestoPredmeta==1:
								if self.TempItemITTP=="Катана" or self.TempItemITTP=="Боевой посох" or self.TempItemITTP=="Двуручный меч" or self.TempItemITTP=="Двуручный топор" or self.TempItemITTP=="Двуручная булава":
									self.Inventimg[0]=self.TempItemIIMG
									self.Pruka.delete()
									self.PrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[0]))
									self.Pruka.create_image(0,0,anchor=NW,image=self.PrukaimgOpened)
									self.Inventimg[1]=self.TempItemIIMG
									self.Lruka.delete()
									self.LrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[1]))
									self.Lruka.create_image(0,0,anchor=NW,image=self.LrukaimgOpened)
								else:
									self.Inventimg[0]=self.TempItemIIMG
									self.Pruka.delete()
									self.PrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[0]))
									self.Pruka.create_image(0,0,anchor=NW,image=self.PrukaimgOpened)
							elif self.MestoPredmeta==2:
								self.Lruka.delete()
								self.LrukaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[1]))
								self.Lruka.create_image(0,0,anchor=NW,image=self.LrukaimgOpened)
							elif self.MestoPredmeta==3:
								self.Golova.delete()
								self.GolovaimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[2]))
								self.Golova.create_image(0,0,anchor=NW,image=self.GolovaimgOpened)
							elif self.MestoPredmeta==4:
								self.Tors.delete()
								self.TorsimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[3]))
								self.Tors.create_image(0,0,anchor=NW,image=self.TorsimgOpened)
							elif self.MestoPredmeta==5:
								self.Ruki.delete()
								self.RukiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[4]))
								self.Ruki.create_image(0,0,anchor=NW,image=self.RukiimgOpened)
							elif self.MestoPredmeta==6:
								self.Nogi.delete()
								self.NogiimgOpened=ImageTk.PhotoImage(Image.open(self.Inventimg[5]))
								self.Nogi.create_image(0,0,anchor=NW,image=self.NogiimgOpened)
							self.meshokID.pop(int(self.CSS2)-1)
							self.meshok.pop(int(self.CSS2)-1)
					elif self.CSS=="3":
						print("Выбрасывает")
						self.meshokID.pop(int(self.CSS2)-1)
						self.meshok.pop(int(self.CSS2)-1)
					if (self.CSS=="2" or self.CSS=="1" or self.CSS=="3") and self.nope==0:
						self.uporyadochivanie()
						self.newprintCSSt(self.uporyd)
						self.textes="Экипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
						self.newprinttex(self.textes)
						self.cor=1
					elif (self.CSS=="2" or self.CSS=="1" or self.CSS=="3") and self.nope==1:
						self.uporyadochivanie()
						self.newprintCSSt(self.uporyd)
						self.textes+="Экипировка: \n" + str(self.invent) + "\nТип экипировки: \n" + str(self.Equipment)
						self.newprinttex(self.textes)
						self.cor=1
			elif self.func=="Бой":    
				if self.cor==0: #Подготовка боя
					self.images(self.classimg)
					self.vihod=1;self.proverka=0;self.ProverkaDodged=0;self.ProverkaSpell=0;
					#Враг
						#Состояние врага
					self.EFire=0;self.EBleed=0;self.EPois=0
						#Время негативных эффектов на враге
					self.EFireT=0;self.EBleedT=0;self.EPoisT=0
						#Урон от магии по умолчанию
					self.EFireDMG=0;self.EWaterDMG=0;self.EAirDMG=0;self.EEarthDMG=0;self.EPhisDMG=0;self.EPoisDMG=0;self.EDarkDMG=0;self.ETrueDMG=0
						#Способности врага
					self.Emag=0;self.EMP=0
					
					#Спеллы
					self.ESpellsType=[] #Тип урона
					self.ESpellsDMG=[] #Урон от спела
					self.ESpellsCost=[] #Затраты маны
					self.ESpellsTime=[] #Если 0 то урон наносится единожды
					self.ESpellsControll=[] #Если есть контроль
					self.ESpellsControllTime=[] #Время контроля
					self.ESpellsControllType=[] #Тип контроля Подброс,Стан,Ослепление,Страх,Привязка
					self.ESpellsBackPush=[] #Смещение от или к противнику
					self.ESpellsBackDist=[] #Дальность минус к противнику, плюс от противника
					
					#Персонаж
						#Состояние персонажа
					self.Fire=0;self.Bleed=0;self.Pois=0
						#Время негативных эффектов
					self.FireT=0;self.BleedT=0;self.PoisT=0
					self.x=random.randint(1,6)
					
					if self.x==1: #Волк
						self.Ename="Волк"
						self.EHP=10+round(10*(self.lvl/2));self.AV=3+round(5*(self.lvl/2));self.EFHP=self.EHP;self.EFMP=self.EMP #Здоровье и атака врага
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0 #Защита от Огня, Воды, Земли, Воздуха, Физикла, Кровотечения, Яда
						self.EnemyType="Животное" #Тип врага
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					elif self.x==2: #Медведь
						self.Ename="Медведь"
						self.EHP=15+round(15*(self.lvl/2));self.AV=3+round(5*(self.lvl/2));self.EFHP=self.EHP;self.EFMP=self.EMP
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0
						self.EnemyType="Животное"
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					elif self.x==3: #Кабан
						self.Ename="Кабан"
						self.EHP=15+round(12*(self.lvl/2));self.AV=5+round(6*(self.lvl/2));self.EFHP=self.EHP;self.EFMP=self.EMP
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0
						self.EnemyType="Животное"
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					elif self.x==4: #Змея
						self.Ename="Змея"
						self.EHP=10+round(10*(self.lvl/2));self.AV=3+round(5*(self.lvl/2));self.EFHP=self.EHP;self.EFMP=self.EMP
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0
						self.EnemyType="Животное"
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					elif self.x==5: #Орёл
						self.Ename="Орёл"
						self.EHP=10+round(10*(self.lvl/2));self.AV=6+round(6*(self.lvl/2));self.EFHP=self.EHP;self.EFMP=self.EMP
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0
						self.EnemyType="Животное"
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					elif self.x==6: #Слизень
						self.Ename="Слизень"
						self.EHP=10+round(10*(self.lvl/2));self.AV=3+round(5*(self.lvl/2));self.Emag=1;self.EMP=20;self.EFHP=self.EHP;self.EFMP=self.EMP
						self.ESpellsType.append("EPoisDMG") #Добавляет спелл в список
						self.ESpellsType.append("EPoisDMG") #Добавляет спелл в список
						self.ESpellsDMG.append(int(10)) #Добавляет урон от спела в список
						self.ESpellsDMG.append(int(6)) #Добавляет урон от спела в список
						self.ESpellsCost.append(int(25)) #Добавляет манакост спела в список
						self.ESpellsCost.append(int(7)) #Добавляет манакост спела в список
						self.EFireRes=0;self.EWaterRes=0;self.EEarthRes=0;self.EAirRes=0;self.EPhisRes=0;self.EBleedRes=0;self.EPoisRes=0
						self.EnemyType="Животное"
						self.expplus=100
						self.EIMG="Data\img\Battle\Enemy\Wolf.png"
					self.EKolHodov=0
					self.ESpeed=2
					self.RangeEnemy=1
					
					self.ETeloFHP=[self.EHP*0.5,self.EHP*0.7,self.EHP*0.35,self.EHP*0.35,self.EHP*0.35,self.EHP*0.35]
					self.ETeloHP=[self.EHP*0.5,self.EHP*0.7,self.EHP*0.35,self.EHP*0.35,self.EHP*0.35,self.EHP*0.35]
					
					self.EnemyImage=ImageTk.PhotoImage(Image.open(self.EIMG))
					self.EnemyImageCanv=Canvas(self.ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=399, height=321)
					self.EnemyImageCanv.place(x=0,y=0)
					self.EnemyImageCanv.create_image(0,0,anchor=NW,image=self.EnemyImage)
					
					self.battlegroundIMGCanv=Canvas(self.ramk,highlightthickness=0, width=562, height=321)
					self.battlegroundIMGCanv.place(x=360,y=0)
					self.battlegroundIMGCanv.create_image(0,0,anchor=NW,image=self.battlegroundIMG)

					self.xh=random.randint(7,9)
					self.yh=random.randint(7,9)
					self.HeroIMGCanv=Canvas(self.ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=27, height=27)
					self.HeroIMGCanv.place(x=501+28*self.xh,y=24+28*self.yh)
					self.HeroIMGCanv.create_image(0,0,anchor=NW,image=self.HeroIMG)
					
					self.xe=random.randint(0,2)
					self.ye=random.randint(0,2)
					self.EnemyiconIMGCanv=Canvas(self.ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=27, height=27)
					self.EnemyiconIMGCanv.place(x=501+28*self.xe,y=24+28*self.ye)
					self.EnemyiconIMGCanv.create_image(0,0,anchor=NW,image=self.EnemyiconIMG)

					self.i=random.randint(1,2)
					if self.i==2:
						self.textes="Вы попали в засаду\n"
						self.textes += "Ваш противник: " + self.Ename + "\n"
						self.newprintCSSt("Продолжить")
						self.cor=1
					else:
						self.textes="Ваш противник: " + self.Ename + "\n"
						self.newprintCSSt("Продолжить")
						self.cor=1
				
				elif self.cor==1: #Выбор действия
					if self.EHP == 0 or self.HP == 0 or self.EHP < 0 or self.HP < 0:
						if self.EHP == 0 or self.EHP < 0:
							self.otchistiti()
							self.textes="Вы победили\n"
							self.exp += self.expplus
							if random.randint(1, 100) > 0: #Изменил
								if random.randint(1, 100) > 90:
									self.x = 2
								else:
									self.x = 1
								self.drop(self.x)
							self.textes+="\nВы получили: " + str(self.expplus) + " опыта\n\n" + self.locatDisc
							self.otchistiti()
							self.newprinttex(self.textes)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
							self.func="Игра"
						elif self.HP == 0 or self.HP < 0:
							self.otchistiti()
							self.func="Игра"
							self.textes+="Вы проиграли\n"
							self.newprintCSSt("Загрузите или начните новую игру")
							self.path = 0
						self.safy=1
					else:
						if self.i%2==1:
							self.textes+="Ваш ход\n"
							#Проверка контроля
							self.newprintCSSt("1)Атаковать\n2)Передвежение\n0)Пропустить ход")
							self.cor=2
						else: #                                                      ----------------------------------------------ТУТ--------------------------------------------
							self.textes+="Ход врага\n"
							self.EffectiveAtack=1/3
							self.EffectiveSpell=1/3
							self.EffectiveHod=1/3
							if self.Emag!=1:
								self.EffectiveSpell*=0
							else:
								self.EffectiveSpell*=1
								self.EffectiveSpells=[]
								self.ESpellsType=["Fire","Water","Earth","Air","True","Dark"] #Тип урона
								self.ESpellsDMG=[self.EAbilityPower+random.randint(5,10)] #Урон от спела
								self.ESpellsDist=[random.randint(1,5)] #Растояние
								self.ESpellsCost=[random.randint(10,20)] #Затраты маны
								self.ESpellsEffects=["Смещение","Контроль","ПереодУрон"]
								
								self.ESpellsPushDist=[random.choice(-2,-1,1,2)]
								self.ESpellsTypeControlls=["Оглушение","Подброс","Ослепление","Страх","Привязка"]
								self.ESpellsPereodDMG=[self.EAbilityPower/5+random.randint(1,2)]
								
								self.NomerSpella=0
								while True:
									self.EffectiveSpell=1/3
									if (self.xh-self.xe<=self.ESpellsDist[self.NomerSpella] and self.yh-self.ye<=self.ESpellsDist[self.NomerSpella]) or (self.xe-self.xh<=self.ESpellsDist[self.NomerSpella] and self.ye-self.yh<=self.ESpellsDist[self.NomerSpella]) or self.EKolHodov!=0: #Проверка ренджа
										self.EffectiveSpell*=1.5
									else:
										self.EffectiveSpell*=0
										self.NomerSpella+=1
										self.EffectiveSpells.append[self.EffectiveSpell]
										continue
									if self.ESpellsCost[self.NomerSpella]>self.EMP: #Проверка маны
										self.EffectiveSpell*=0
										self.NomerSpella+=1
										self.EffectiveSpells.append[self.EffectiveSpell]
										continue
									else:
										self.EffectiveSpell/=self.ESpellsCost[self.NomerSpella]/10
									self.EffectiveSpell*=self.ESpellsDMG[self.NomerSpella]/10 #Эффективность урона
									self.NomerSpella+=1
									if self.NomerSpella==len(self.ESpellsDist):
										break
							if self.xh-self.xe>self.RangeEnemy or self.yh-self.ye>self.RangeEnemy or self.xe-self.xh>self.RangeEnemy or self.ye-self.yh>self.RangeEnemy or self.EKolHodov!=0:
								self.EffectiveAtack*=0
							if self.EKolHodov==0 and ((self.xh-self.xe==self.RangeEnemy and self.yh-self.ye==self.RangeEnemy) or (self.xh-self.xe==self.RangeEnemy and self.yh-self.ye==0) or (self.xh-self.xe==0 and self.yh-self.ye==self.RangeEnemy) or (self.xe-self.xh==self.RangeEnemy and self.ye-self.yh==self.RangeEnemy) or (self.xe-self.xh==0 and self.ye-self.yh==self.RangeEnemy) or (self.xe-self.xh==self.RangeEnemy and self.ye-self.yh==0)):
								self.EffectiveHod*=0
							self.IIReshenie=max([self.EffectiveAtack,self.EffectiveSpell,self.EffectiveHod])
							if self.IIReshenie==0:
								self.i+=1
								self.cor=1
								self.EKolHodov=0
							elif self.EffectiveAtack==self.IIReshenie:
								self.textes+="Враг наносит удар"
								self.EMestoUdara=random.randint(0,5)
								if self.EMestoUdara==0:
									self.TeloHP[0]-=self.AV
									self.textes+=" в голову\n"
								elif self.EMestoUdara==1:
									self.TeloHP[1]-=self.AV
									self.textes+=" в торс\n"
								elif self.EMestoUdara==2:
									self.TeloHP[2]-=self.AV
									self.textes+=" в правую руку\n"
								elif self.EMestoUdara==3:
									self.TeloHP[3]-=self.AV
									self.textes+=" в левую руку\n"
								elif self.EMestoUdara==4:
									self.TeloHP[4]-=self.AV
									self.textes+=" в правую ногу\n"
								elif self.EMestoUdara==5:
									self.TeloHP[5]-=self.AV
									self.textes+=" в левую ногу\n"
								self.HP-=self.AV
								self.i+=1
								self.cor=1
							elif self.EffectiveSpell==self.IIReshenie:
								print("Каст абилки")
								self.i+=1
								self.cor=1
							elif self.EffectiveHod==self.IIReshenie:
								self.textes+="Враг походил "
								if self.xe!=self.xh and self.xe<self.xh:
									self.xe+=1
									self.textes+="вправо\n"
								elif self.xe!=self.xh and self.xe>self.xh:
									self.xe-=1
									self.textes+="влево\n"
								elif self.ye!=self.yh and self.ye<self.yh:
									self.ye+=1
									self.textes+="вниз\n"
								elif self.ye!=self.yh and self.ye>self.yh:
									self.ye-=1
									self.textes+="вверх\n"
								self.EKolHodov+=1
								if self.EKolHodov==self.ESpeed:
									self.i+=1
									self.cor=1
									self.EKolHodov=0
								elif ((self.xh-self.xe==self.RangeEnemy and self.yh-self.ye==self.RangeEnemy) or (self.xh-self.xe==self.RangeEnemy and self.yh-self.ye==0) or (self.xh-self.xe==0 and self.yh-self.ye==self.RangeEnemy) or (self.xe-self.xh==self.RangeEnemy and self.ye-self.yh==self.RangeEnemy) or (self.xe-self.xh==0 and self.ye-self.yh==self.RangeEnemy) or (self.xe-self.xh==self.RangeEnemy and self.ye-self.yh==0)):
									self.i+=1
									self.cor=1
									self.EKolHodov=0
							print("Атака: ",self.EffectiveAtack,"Спелл: ",self.EffectiveSpell,"Ход: ",self.EffectiveHod,self.EKolHodov)
							self.newprintCSSt("Продолжить")
				elif self.cor==2: #Выбор действия
					if self.EHP==0 or self.EHP<0:
						print("You win")
					if self.CSS=="1":
						self.newprintCSSt("1)Удар\n2)Использовать умение\n0)Отмена")
						self.cor=3
					elif self.CSS=="2":
						self.newprintCSSt("1)Вверх\n2)Вниз\n3)Влево\n4)Вправо\n0)Отмена")
						self.cor=6
					elif self.CSS=="0":
						self.textes+="Вы пропустили ход\n"
						self.newprintCSSt("Продолжить")
						self.cor=1
						self.i+=1
				elif self.cor==3: #"Выбор атаки"
					if self.CSS=="1": #Удар рукой
						if self.xh-self.xe>self.RangeHero or self.yh-self.ye>self.RangeHero or self.xe-self.xh>self.RangeHero or self.ye-self.yh>self.RangeHero:
							self.textes+="Противник внедосягаемости\n"
							self.newprintCSSt("1)Атаковать\n2)Передвежение\n3)Пропустить ход")
							self.cor=2
						else:
							self.newprintCSSt("1)Голова\n2)Торс\n3)Правая рука\n4)Левая рука\n5)Правая нога\n6)Левая нога\n0)Назад")
							self.cor=4
					if self.CSS=="2": #Умение
						if len(self.SA0)==0:
							self.textes+="У вас нет активных умений\n"
							self.newprintCSSt("1)Атаковать\n2)Передвежение\n3)Пропустить ход")
							self.cor=2
						else:
							self.textes+="Выберите умение\n"
							self.UmeniyaTEX=""
							self.ivan=0
							while True:
								try:
									self.UmeniyaTEX += str(self.ivan+1) + ")" + self.SA0[self.ivan] + "\n"
									self.ivan+=1
								except:
									break
							self.UmeniyaTEX+="0)Назад"
							self.newprintCSSt(self.UmeniyaTEX)
							self.cor=5
				elif self.cor==4: #"Выбор места удара"
					if self.CSS=="1": #Удар в голову
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[0]-=self.dmg
						self.newprintCSSt("Продолжить")
					elif self.CSS=="2": #Удар в торс
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[1]-=self.dmg
						self.newprintCSSt("Продолжить")
					elif self.CSS=="3": #Удар в правую руку
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[2]-=self.dmg
						self.newprintCSSt("Продолжить")
					elif self.CSS=="4": #Удар в левую руку
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[3]-=self.dmg
						self.newprintCSSt("Продолжить")
					elif self.CSS=="5": #Удар в правую ногу
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[4]-=self.dmg
						self.newprintCSSt("Продолжить")
					elif self.CSS=="6": #Удар в левую ногу
						self.dmg=round(self.uron*(1-self.EPhisRes/(100+self.EPhisRes)))
						self.textes+="Удар прошёл благополучно\n"
						self.EHP-=self.dmg
						self.ETeloHP[5]-=self.dmg
						self.newprintCSSt("Продолжить")
					if self.CSS=="1" or self.CSS=="2" or self.CSS=="3" or self.CSS=="4" or self.CSS=="5" or self.CSS=="6":
						self.i+=1
						self.cor=1
					elif self.CSS=="0":
						self.cor=1
				elif self.cor==5: #"Выбор и активация умения"
					if self.CSS=="0":
						self.newprintCSSt("1)Атаковать\n2)Передвежение\n3)Пропустить ход")
						self.cor=2
					else:
						if int(self.CSS)>len(self.SA0):
							self.textes+="Введите правильное число"
						else:
							self.active(int(self.CSS))
				elif self.cor==6: #"1)Вверх\n2)Вниз\n3)Влево\n4)Вправо\n0)Отмена"
					if self.CSS=="1":
						if self.yh!=0:
							if self.ye==self.yh-1 and self.xe-self.xh==0:
								self.textes+="Вы не можете походить впереди враг\n"
								self.newprintCSSt("1)Атаковать\n2)Передвежение\n0)Пропустить ход")
								self.cor=2
							else:
								self.yh-=1
								self.i+=1
								self.cor=1
								self.textes+="Вы походили вверх\n"
								self.newprintCSSt("Продолжить")
						else:
							self.textes+="Вы уверены что хотите сбежать?\n"
							self.newprintCSSt("1)Да\n2)Нет")
							self.cor=7
					elif self.CSS=="2":
						if self.yh!=9:
							if self.ye==self.yh+1 and self.xe-self.xh==0:
								self.textes+="Вы не можете походить впереди враг\n"
								self.newprintCSSt("1)Атаковать\n2)Передвежение\n0)Пропустить ход")
								self.cor=2
							else:
								self.yh+=1
								self.i+=1
								self.cor=1
								self.textes+="Вы походили вниз\n"
								self.newprintCSSt("Продолжить")
						else:
							self.textes+="Вы уверены что хотите сбежать?\n"
							self.newprintCSSt("1)Да\n2)Нет")
							self.cor=7
					elif self.CSS=="3":
						if self.xh!=0:
							if self.xe==self.xh-1 and self.ye-self.yh==0:
								self.textes+="Вы не можете походить впереди враг\n"
								self.newprintCSSt("1)Атаковать\n2)Передвежение\n0)Пропустить ход")
								self.cor=2
							else:
								self.xh-=1
								self.i+=1
								self.cor=1
								self.textes+="Вы походили влево\n"
								self.newprintCSSt("Продолжить")
						else:
							self.textes+="Вы уверены что хотите сбежать?\n"
							self.newprintCSSt("1)Да\n2)Нет")
							self.cor=7
					elif self.CSS=="4":
						if self.xh!=9:
							if self.xe==self.xh+1 and self.ye-self.yh==0:
								self.textes+="Вы не можете походить впереди враг\n"
								self.newprintCSSt("1)Атаковать\n2)Передвежение\n0)Пропустить ход")
								self.cor=2
							else:
								self.xh+=1
								self.i+=1
								self.cor=1
								self.textes+="Вы походили вправо\n"
								self.newprintCSSt("Продолжить")
						else:
							self.textes+="Вы уверены что хотите сбежать?\n"
							self.newprintCSSt("1)Да\n2)Нет")
							self.cor=7
					elif self.CSS=="0":
						self.newprintCSSt("1)Атаковать\n2)Передвежение\n3)Пропустить ход")
						self.cor=2
				if self.func=="Бой":
					self.HeroIMGCanv.destroy()
					self.EnemyiconIMGCanv.destroy()
					
					self.HeroIMGCanv=Canvas(self.ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=27, height=27)
					self.HeroIMGCanv.place(x=501+28*self.xh,y=24+28*self.yh)
					self.HeroIMGCanv.create_image(0,0,anchor=NW,image=self.HeroIMG)
					
					self.EnemyiconIMGCanv=Canvas(self.ramk,highlightbackground="LightGoldenrod4",highlightthickness=0, width=27, height=27)
					self.EnemyiconIMGCanv.place(x=501+28*self.xe,y=24+28*self.ye)
					self.EnemyiconIMGCanv.create_image(0,0,anchor=NW,image=self.EnemyiconIMG)
					
					#Враг состояние
					if self.ETeloHP[0]>self.ETeloFHP[0]/100*75:
						self.ESTATUSHEADIMG="Data\img\Battle\HeadNormal.png"
					elif self.ETeloHP[0]>self.ETeloFHP[0]/100*30:
						self.ESTATUSHEADIMG="Data\img\Battle\HeadWound.png"
					elif self.ETeloHP[0]>0:
						self.ESTATUSHEADIMG="Data\img\Battle\HeadCritical.png"
					elif self.ETeloHP[0]<=0:
						self.ESTATUSHEADIMG="Data\img\Battle\HeadDestroyed.png"
						
					if self.ETeloHP[1]>self.ETeloFHP[1]/100*75:
						self.ESTATUSTORSIMG="Data\img\Battle\TorsNormal.png"
					elif self.ETeloHP[1]>self.ETeloFHP[1]/100*30:
						self.ESTATUSTORSIMG="Data\img\Battle\TorsWound.png"
					elif self.ETeloHP[1]>0:
						self.ESTATUSTORSIMG="Data\img\Battle\TorsCritical.png"
					elif self.ETeloHP[1]<=0:
						self.ESTATUSTORSIMG="Data\img\Battle\TorsDestroyed.png"
						
					if self.ETeloHP[2]>self.ETeloFHP[2]/100*75:
						self.ESTATUSRHANDIMG="Data\img\Battle\RightHandNormal.png"
					elif self.ETeloHP[2]>self.ETeloFHP[2]/100*30:
						self.ESTATUSRHANDIMG="Data\img\Battle\RightHandWound.png"
					elif self.ETeloHP[2]>0:
						self.ESTATUSRHANDIMG="Data\img\Battle\RightHandCritical.png"
					elif self.ETeloHP[2]<=0:
						self.ESTATUSRHANDIMG="Data\img\Battle\RightHandDestroyed.png"
						
					if self.ETeloHP[3]>self.ETeloFHP[3]/100*75:
						self.ESTATUSLHANDIMG="Data\img\Battle\LeftHandNormal.png"
					elif self.ETeloHP[3]>self.ETeloFHP[3]/100*30:
						self.ESTATUSLHANDIMG="Data\img\Battle\LeftHandWound.png"
					elif self.ETeloHP[3]>0:
						self.ESTATUSLHANDIMG="Data\img\Battle\LeftHandCritical.png"
					elif self.ETeloHP[3]<=0:
						self.ESTATUSLHANDIMG="Data\img\Battle\LeftHandDestroyed.png"
						
					if self.ETeloHP[4]>self.ETeloFHP[4]/100*75:
						self.ESTATUSRLEGIMG="Data\img\Battle\RightLegNormal.png"
					elif self.ETeloHP[4]>self.ETeloFHP[4]/100*30:
						self.ESTATUSRLEGIMG="Data\img\Battle\RightLegWound.png"
					elif self.ETeloHP[4]>0:
						self.ESTATUSRLEGIMG="Data\img\Battle\RightLegCritical.png"
					elif self.ETeloHP[4]<=0:
						self.ESTATUSRLEGIMG="Data\img\Battle\RightLegDestroyed.png"
					
					if self.ETeloHP[5]>self.ETeloFHP[5]/100*75:
						self.ESTATUSLLEGIMG="Data\img\Battle\LeftLegNormal.png"
					elif self.ETeloHP[5]>self.ETeloFHP[5]/100*30:
						self.ESTATUSLLEGIMG="Data\img\Battle\LeftLegWound.png"
					elif self.ETeloHP[5]>0:
						self.ESTATUSLLEGIMG="Data\img\Battle\LeftLegCritical.png"
					elif self.ETeloHP[5]<=0:
						self.ESTATUSLLEGIMG="Data\img\Battle\LeftLegDestroyed.png"
						
					self.EHeadIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSHEADIMG))
					self.battlegroundIMGCanv.create_image(54,105,anchor=NW,image=self.EHeadIMG)
					
					self.ETorsIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSTORSIMG))
					self.battlegroundIMGCanv.create_image(46,134,anchor=NW,image=self.ETorsIMG)
					
					self.ERHandIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSRHANDIMG))
					self.battlegroundIMGCanv.create_image(11,140,anchor=NW,image=self.ERHandIMG)
					
					self.ELHandIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSLHANDIMG))
					self.battlegroundIMGCanv.create_image(84,140,anchor=NW,image=self.ELHandIMG)
					
					self.ERLegIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSRLEGIMG))
					self.battlegroundIMGCanv.create_image(26,194,anchor=NW,image=self.ERLegIMG)
					
					self.ELLegIMG=ImageTk.PhotoImage(Image.open(self.ESTATUSLLEGIMG))
					self.battlegroundIMGCanv.create_image(67,194,anchor=NW,image=self.ELLegIMG)
					
					#Герой
					if self.TeloHP[0]>self.TeloFHP[0]/100*75:
						self.STATUSHEADIMG="Data\img\Battle\HeadNormal.png"
					elif self.TeloHP[0]>self.TeloFHP[0]/100*30:
						self.STATUSHEADIMG="Data\img\Battle\HeadWound.png"
					elif self.TeloHP[0]>0:
						self.STATUSHEADIMG="Data\img\Battle\HeadCritical.png"
					elif self.TeloHP[0]<=0:
						self.STATUSHEADIMG="Data\img\Battle\HeadDestroyed.png"
						
					if self.TeloHP[1]>self.TeloFHP[1]/100*75:
						self.STATUSTORSIMG="Data\img\Battle\TorsNormal.png"
					elif self.TeloHP[1]>self.TeloFHP[1]/100*30:
						self.STATUSTORSIMG="Data\img\Battle\TorsWound.png"
					elif self.TeloHP[1]>0:
						self.STATUSTORSIMG="Data\img\Battle\TorsCritical.png"
					elif self.TeloHP[1]<=0:
						self.STATUSTORSIMG="Data\img\Battle\TorsDestroyed.png"
						
					if self.TeloHP[2]>self.TeloFHP[2]/100*75:
						self.STATUSRHANDIMG="Data\img\Battle\RightHandNormal.png"
					elif self.TeloHP[2]>self.TeloFHP[2]/100*30:
						self.STATUSRHANDIMG="Data\img\Battle\RightHandWound.png"
					elif self.TeloHP[2]>0:
						self.STATUSRHANDIMG="Data\img\Battle\RightHandCritical.png"
					elif self.TeloHP[2]<=0:
						self.STATUSRHANDIMG="Data\img\Battle\RightHandDestroyed.png"
						
					if self.TeloHP[3]>self.TeloFHP[3]/100*75:
						self.STATUSLHANDIMG="Data\img\Battle\LeftHandNormal.png"
					elif self.TeloHP[3]>self.TeloFHP[3]/100*30:
						self.STATUSLHANDIMG="Data\img\Battle\LeftHandWound.png"
					elif self.TeloHP[3]>0:
						self.STATUSLHANDIMG="Data\img\Battle\LeftHandCritical.png"
					elif self.TeloHP[3]<=0:
						self.STATUSLHANDIMG="Data\img\Battle\LeftHandDestroyed.png"
						
					if self.TeloHP[4]>self.TeloFHP[4]/100*75:
						self.STATUSRLEGIMG="Data\img\Battle\RightLegNormal.png"
					elif self.TeloHP[4]>self.TeloFHP[4]/100*30:
						self.STATUSRLEGIMG="Data\img\Battle\RightLegWound.png"
					elif self.TeloHP[4]>0:
						self.STATUSRLEGIMG="Data\img\Battle\RightLegCritical.png"
					elif self.TeloHP[4]<=0:
						self.STATUSRLEGIMG="Data\img\Battle\RightLegDestroyed.png"
					
					if self.TeloHP[5]>self.TeloFHP[5]/100*75:
						self.STATUSLLEGIMG="Data\img\Battle\LeftLegNormal.png"
					elif self.TeloHP[5]>self.TeloFHP[5]/100*30:
						self.STATUSLLEGIMG="Data\img\Battle\LeftLegWound.png"
					elif self.TeloHP[5]>0:
						self.STATUSLLEGIMG="Data\img\Battle\LeftLegCritical.png"
					elif self.TeloHP[5]<=0:
						self.STATUSLLEGIMG="Data\img\Battle\LeftLegDestroyed.png"
						
					self.HeadIMG=ImageTk.PhotoImage(Image.open(self.STATUSHEADIMG))
					self.battlegroundIMGCanv.create_image(486,105,anchor=NW,image=self.HeadIMG)
					
					self.TorsIMG=ImageTk.PhotoImage(Image.open(self.STATUSTORSIMG))
					self.battlegroundIMGCanv.create_image(478,134,anchor=NW,image=self.TorsIMG)
					
					self.RHandIMG=ImageTk.PhotoImage(Image.open(self.STATUSRHANDIMG))
					self.battlegroundIMGCanv.create_image(445,140,anchor=NW,image=self.RHandIMG)
					
					self.LHandIMG=ImageTk.PhotoImage(Image.open(self.STATUSLHANDIMG))
					self.battlegroundIMGCanv.create_image(516,140,anchor=NW,image=self.LHandIMG)
					
					self.RLegIMG=ImageTk.PhotoImage(Image.open(self.STATUSRLEGIMG))
					self.battlegroundIMGCanv.create_image(458,194,anchor=NW,image=self.RLegIMG)
					
					self.LLegIMG=ImageTk.PhotoImage(Image.open(self.STATUSLLEGIMG))
					self.battlegroundIMGCanv.create_image(499,194,anchor=NW,image=self.LLegIMG)
					
					self.newprinttex(self.textes)
			elif self.func=="Прокачка персонажа":
				if self.cor==1: #Выбор что качать
					if self.CSS=="1":
						if self.part==0:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nВыносливость: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
						else:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nВыносливость: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n0)Назад")
							self.cor=2
					elif self.CSS=="2":
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки пассивных способностей: " + str(self.SP) + "\nСпособности: " + str(self.S0) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("0)Назад\nСпособности: \nЭкипировка:\n1)Двуручные мечи  2)Одноручные мечи\n3)Двуручные булавы  4)Одноручные булавы\n5)Двуручные топоры  6)Одноручные топоры\n7)Боевые посохи  8)Скипетры\n9)Баклеры       10)Щиты\n11)Башенные щиты  12)Лёгкая броня\n13)Средняя броня  14)Тяжёлая броня\nМагия:\n15)Магия огня  16)Магия земли\n17)Магия воздуха  18)Магия воды\n19)Магия тьмы\nВспомогательные:\n20)Чтение свитков  21)Скрытность\n22)Критический удар  23)Вскрытие замков\n24)Использование ловушек  25)Орлиное зрение\n26)Лечение  27)Парирование\n28)Дух  29)Кинжалы\n30)Катаны")
						self.cor=4
					elif self.CSS=="3":
						self.images('Data/img/Prokachka/ACTSpell.gif')
						SpellUp()
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки активных способностей: " + str(self.SAP) + "\nСпособности: " + str(self.SA0) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("0)Назад\nАктивные способности:   \nМагия огня 1)Шар стихии 2)Искра 3)Поток пламени 4)Дыхание дракона\nМагия воздуха 1)Шар стихии 5)Порез ветром 6)Сносящий поток 7)Смерч\nМагия земли 1)Шар стихии 8)Бросок камня 9)Столб земли 10)Землетрясение\nМагия воды 1)Шар стихии 11)Всплеск 12)Гейзер 13)Смертельный дождь\nМагия тьмы 1)Шар стихии 14)Сгуток тени 15)Похищение здоровья 16)Прикосновене смерти\nБаклеры 17)Тычёк щитом 18)Бросок щита\nЩиты 19)Удар щитом 20)Оглушение\nБашенные щиты 21)Таран 20)Оглушение\nМечи 22)Рассекающий порез 23)Разрубающий удар 24)Заряженный взмах\nТопоры 25)Рубитькромсать 26)Сильный удар 27)Удар с плеча\nБулавы 28)Удар с размаха 26)Сильный удар 29)Громовой удар\nКинжалы 22)Рассекающий порез 30)Проникающий удар 31)Перерезание глотки\nКатаны 32)Ослепляющий удар 33)Удар четырёх стихий 34)Тройной удар\nДух 35)Прикосновение духа 36)Разрез духа 37)Удар духа")
						self.cor=6
					elif self.CSS=="4" and self.part==0:
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаша текущая характеристика: "
						if self.weapon=="power":
							self.textes+="Сила"
						elif self.weapon=="agility":
							self.textes+="Ловкость"
						elif self.weapon=="magic":
							self.textes+="Мудрость"
						else:
							self.textes+="Отсутствует"
						self.newprintCSSt("1)Сила\n2)Ловкость\n3)Мудрость\n0)Назад")
						self.newprinttex(self.textes)
						self.cor=8
					elif self.CSS=="0":
						if (self.H==0 or self.P>0 or self.weapon=="Отсутствует") and self.part==0 and self.init==0:
							self.func="Прокачка персонажа"
							self.cor=1
							self.textes="Вы не можете начать игру с здоровьем равным нулю,непотраченными очками характеристик или с невыбранной основной характеристикой\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP)
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
						elif self.part==0 and self.init==0:
							self.func="Игра"
							self.FHP = self.H * 5
							self.FMP = self.M * 5
							self.HP=self.FHP
							self.MP=self.FMP
							self.part=1
							self.path=2
							self.safy=1
							self.locatImg='Data\img\Locations\Hram.png'
							self.locatDisc="Вы очнулись на обломках в неизвестном для вас месте, помимо этого вы абсолютно не знаете кто вы и как тут оказались"
							self.locatCSS="Продолжить"
							self.locatCur="Обломки храма"
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
							self.images(self.locatImg)
						else:
							self.func="Игра"
							self.images(self.locatImg)
							self.newprinttex(self.locatDisc)
							self.newprintCSSt(self.locatCSS)
				elif self.cor==2: #Выбор характеристики
					if self.CSS=="1":
						self.newprinttex("Введите количество очков которые вы хотите распределить на силу")
						self.CSS2="Сила"
						self.cor=3
					elif self.CSS=="2":
						self.newprinttex("Введите количество очков которые вы хотите распределить на ловкость")
						self.CSS2="Ловкость"
						self.cor=3
					elif self.CSS=="3":
						self.newprinttex("Введите количество очков которые вы хотите распределить на мудрость")
						self.CSS2="Мудрость"
						self.cor=3
					elif self.CSS=="4":
						self.newprinttex("Введите количество очков которые вы хотите распределить на выносливость")
						self.CSS2="Выносливость"
						self.cor=3
					elif self.CSS=="5" and self.part==0:
						self.newprinttex("Введите количество очков на которые вы хотите уменьшить силу")
						self.CSS2="Сила"
						self.cor=9
					elif self.CSS=="6" and self.part==0:
						self.newprinttex("Введите количество очков на которые вы хотите уменьшить ловкость")
						self.CSS2="Ловкость"
						self.cor=9
					elif self.CSS=="7" and self.part==0:
						self.newprinttex("Введите количество очков на которые вы хотите уменьшить мудрость")
						self.CSS2="Мудрость"
						self.cor=9
					elif self.CSS=="8" and self.part==0:
						self.newprinttex("Введите количество очков на которые вы хотите уменьшить выносливость")
						self.CSS2="Выносливость"
						self.cor=9
					elif self.CSS=="0" and self.part>0:
						self.cor=1
						self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
					elif self.CSS=="0" and self.part==0:
						self.cor=1
						self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
				elif self.cor==3: #Выбор количества характеристик
					if int(self.CSS)>self.P and self.init==0 and self.part==0:
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
						self.newprinttex(self.textes)
						self.newprintCSSt("У вас недостаточно очков характеристик\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
						self.cor=2
					elif int(self.CSS)>self.P:
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
						self.newprinttex(self.textes)
						self.newprintCSSt("У вас недостаточно очков характеристик\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n0)Назад")
						self.cor=2
					else:
						if self.CSS2=="Сила":
							self.S+=int(self.CSS)
						elif self.CSS2=="Ловкость":
							self.A+=int(self.CSS)
						elif self.CSS2=="Мудрость":
							self.M+=int(self.CSS)
						elif self.CSS2=="Выносливость":
							self.H+=int(self.CSS)
						self.P-=int(self.CSS)
					if self.init==0 and self.part==0:
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
						self.newprinttex(self.textes)
						self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
						self.cor=2
					else:
						self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
						self.newprinttex(self.textes)
						self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n0)Назад")
						self.cor=2
				elif self.cor==4: #Выбор способности
					if self.SP==0 and self.part>0:
						self.textes="Недостаточное количество очков!\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
						self.cor=1
					elif self.SP==0 and self.part==0:
						self.textes="Недостаточное количество очков!\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
						self.cor=1
					else:
						if self.CSS=="0" and self.part>0:
							self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
							self.cor=1
						elif self.CSS=="0" and self.part==0:
							self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
							self.cor=1
						elif self.CSS=="1":
							self.newprinttex("Навык двуручные мечи отвечает за возможность использования двуручных мечей и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="0"
							self.CSS3="Двуручные мечи"
							self.cor=5
						elif self.CSS=="2" or self.CSS=="Одноручные мечи":
							self.newprinttex("Навык одноручные мечи отвечает за возможность использования одноручных мечей и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="1"
							self.CSS3="Одноручные мечи"
							self.cor=5
						elif self.CSS=="3" or self.CSS=="Двуручные булавы":
							self.newprinttex("Навык двуручные булавы отвечает за возможность использования двуручных булав и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="2"
							self.CSS3="Двуручные булавы"
							self.cor=5
						elif self.CSS=="4" or self.CSS=="Одноручные булавы":
							self.newprinttex("Навык двуручные булавы отвечает за возможность использования двуручных булав и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="3"
							self.CSS3="Одноручные булавы"
							self.cor=5
						elif self.CSS=="5" or self.CSS=="Двуручные топоры":
							self.newprinttex("Навык двуручные топоры отвечает за возможность использования двуручных топоров и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="4"
							self.CSS3="Двуручные топоры"
							self.cor=5
						elif self.CSS=="6" or self.CSS=="Одноручные топоры":
							self.newprinttex("Навык одноручные топоры отвечает за возможность использования одноручных топоров и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="5"
							self.CSS3="Одноручные топоры"
							self.cor=5
						elif self.CSS=="7" or self.CSS=="Боевые посохи":
							self.newprinttex("Навык боевые посохи отвечает за возможность использования боевых посохов и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="6"
							self.CSS3="Боевые посохи"
							self.cor=5
						elif self.CSS=="8" or self.CSS=="Скипетры":
							self.newprinttex("Навык скипетры отвечает за возможность использования скипетров и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="7"
							self.CSS3="Скипетры"
							self.cor=5
						elif self.CSS=="9" or self.CSS=="Баклеры":
							self.newprinttex("Навык баклеры отвечает за возможность использования баклеров и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="8"
							self.CSS3="Баклеры"
							self.cor=5
						elif self.CSS=="10" or self.CSS=="Щиты":
							self.newprinttex("Навык щиты отвечает за возможность использования щитов и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="9"
							self.CSS3="Щиты"
							self.cor=5
						elif self.CSS=="11" or self.CSS=="Башенные щиты":
							self.newprinttex("Навык башенные щиты отвечает за возможность использования башенных щитов и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="10"
							self.CSS3="Башенные щиты"
							self.cor=5
						elif self.CSS=="12" or self.CSS=="Лёгкая броня":
							self.newprinttex("Навык лёгкая броня отвечает за возможность использования лёгкой брони и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="11"
							self.CSS3="Лёгкая броня"
							self.cor=5
						elif self.CSS=="13" or self.CSS=="Средняя броня":
							self.newprinttex("Навык средняя броня отвечает за возможность использования средней брони и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="12"
							self.CSS3="Средняя броня"
							self.cor=5
						elif self.CSS=="14" or self.CSS=="Тяжёлая броня":
							self.newprinttex("Навык тяжёлая броня отвечает за возможность использования тяжёлой брони и урон который они блокируют")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="13"
							self.CSS3="Тяжёлая броня"
							self.cor=5
						elif self.CSS=="15" or self.CSS=="Магия огня":
							self.newprinttex("Навык магия огня отвечает за возможность использования магии огня и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="14"
							self.CSS3="Магия огня"
							self.cor=5
						elif self.CSS=="16" or self.CSS=="Магия земли":
							self.newprinttex("Навык магия земли отвечает за возможность использования магии земли и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="15"
							self.CSS3="Магия земли"
							self.cor=5
						elif self.CSS=="17" or self.CSS=="Магия воздуха":
							self.newprinttex("Навык магия воздуха отвечает за возможность использования магии воздуха и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="16"
							self.CSS3="Магия воздуха"
							self.cor=5
						elif self.CSS=="18" or self.CSS=="Магия воды":
							self.newprinttex("Навык магия воды отвечает за возможность использования магии воды и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="17"
							self.CSS3="Магия воды"
							self.cor=5
						elif self.CSS=="19" or self.CSS=="Магия тьмы":
							self.newprinttex("Навык магия тьмы отвечает за возможность использования магии тьмы и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="18"
							self.CSS3="Магия тьмы"
							self.cor=5
						elif self.CSS=="20" or self.CSS=="Чтение свитков":
							self.newprinttex("Навык чтение свитков отвечает за возможность использования свитков")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="19"
							self.CSS3="Чтение свитков"
							self.cor=5
						elif self.CSS=="21" or self.CSS=="Скрытность":
							self.newprinttex("Навык скрытность отвечает за возможность использования скрытности и возможности избегать битвы")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="20"
							self.CSS3="Скрытность"
							self.cor=5
						elif self.CSS=="22" or self.CSS=="Критический удар":
							self.newprinttex("Навык критический удар отвечает за возможность выпадения критического удара во время атаки")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="21"
							self.CSS3="Критический удар"
							self.cor=5
						elif self.CSS=="23" or self.CSS=="Вскрытие замков":
							self.newprinttex("Навык вскрытие замков отвечает за возможность вскрытия дверей и сундуков без ключей")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="22"
							self.CSS3="Вскрытие замков"
							self.cor=5
						elif self.CSS=="24" or self.CSS=="Обращение с ловушками":
							self.newprinttex("Навык обращение с ловушками отвечает за возможность разминировать ловушки и устанавливать ловушки и мины")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="23"
							self.CSS3="Обращение с ловушками"
							self.cor=5
						elif self.CSS=="25" or self.CSS=="Орлиное зрение":
							self.newprinttex("Навык орлиное зрение отвечает за возможность нахождения скрытых контейнеров, проходов, а так же получение информации о противниках")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="24"
							self.CSS3="Орлиное зрение"
							self.cor=5
						elif self.CSS=="26" or self.CSS=="Лечение":
							self.newprinttex("Навык лечение отвечает за количество восстановленного здоровь путём зелий и аптечек")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="25"
							self.CSS3="Лечение"
							self.cor=5
						elif self.CSS=="27" or self.CSS=="Парирование":
							self.newprinttex("Навык парирование даёт шанс нанести противнику урон вместо блока")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="26"
							self.CSS3="Парирование"
							self.cor=5
						elif self.CSS=="28" or self.CSS=="Дух":
							self.newprinttex("Навык дух отвечает за возможность использования духа")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="27"
							self.CSS3="Дух"
							self.cor=5
						elif self.CSS=="29" or self.CSS=="Кинжалы":
							self.newprinttex("Навык кинжалы отвечает за возможность использования кинжалов и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="28"
							self.CSS3="Кинжалы"
							self.cor=5
						elif self.CSS=="30" or self.CSS=="Катаны":
							self.newprinttex("Навык катаны отвечает за возможность использования катан и урон от них")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="29"
							self.CSS3="Катаны"
							self.cor=5
				elif self.cor==5: #Подтверждение способности
					if self.SID[int(self.CSS2)]>2:
						self.textes="Уровень этой способности максимальный!\nИмя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки пассивных способностей: " + str(self.SP) + "\nСпособности: " + str(self.S0) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("0)Назад\nСпособности: \nЭкипировка:\n1)Двуручные мечи  2)Одноручные мечи\n3)Двуручные булавы  4)Одноручные булавы\n5)Двуручные топоры  6)Одноручные топоры\n7)Боевые посохи  8)Скипетры\n9)Баклеры       10)Щиты\n11)Башенные щиты  12)Лёгкая броня\n13)Средняя броня  14)Тяжёлая броня\nМагия:\n15)Магия огня  16)Магия земли\n17)Магия воздуха  18)Магия воды\n19)Магия тьмы\nВспомогательные:\n20)Чтение свитков  21)Скрытность\n22)Критический удар  23)Вскрытие замков\n24)Использование ловушек  25)Орлиное зрение\n26)Лечение  27)Парирование\n28)Дух  29)Кинжалы\n30)Катаны")
						self.cor=4
					else:
						if self.CSS=="1":
							self.SID[int(self.CSS2)]+=1
							self.SP-=1
							if self.SID[int(self.CSS2)]==1:
								self.S0.append(self.CSS3)
							elif self.SID[int(self.CSS2)]==2:
								self.S0.remove(self.CSS3)
								self.S0.append(self.CSS3 + " self.lvl 2")
							elif self.SID[int(self.CSS2)]==3:
								self.S0.remove(self.CSS3 + " self.lvl 2")
								self.S0.append(self.CSS3 + " self.lvl 3")
						if self.CSS=="2" or self.CSS=="1":
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки пассивных способностей: " + str(self.SP) + "\nСпособности: " + str(self.S0) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("0)Назад\nСпособности: \nЭкипировка:\n1)Двуручные мечи  2)Одноручные мечи\n3)Двуручные булавы  4)Одноручные булавы\n5)Двуручные топоры  6)Одноручные топоры\n7)Боевые посохи  8)Скипетры\n9)Баклеры       10)Щиты\n11)Башенные щиты  12)Лёгкая броня\n13)Средняя броня  14)Тяжёлая броня\nМагия:\n15)Магия огня  16)Магия земли\n17)Магия воздуха  18)Магия воды\n19)Магия тьмы\nВспомогательные:\n20)Чтение свитков  21)Скрытность\n22)Критический удар  23)Вскрытие замков\n24)Использование ловушек  25)Орлиное зрение\n26)Лечение  27)Парирование\n28)Дух  29)Кинжалы\n30)Катаны")
							self.cor=4
				elif self.cor==6: #Выбор активной способности
					if self.SAP==0 and self.part>0:
						self.textes="Недостаточное количество очков!\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
						self.cor=1
					elif self.SAP==0 and self.part==0:
						self.textes="Недостаточное количество очков!\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
						self.cor=1
					else:
						if self.CSS=="0" and self.part>0:
							self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n0)Продолжить")
							self.cor=1
						elif self.CSS=="0" and self.part==0:
							self.textes="Ваш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
							self.cor=1
						elif self.CSS=="1" or self.CSS=="Шар стихии": #Огонь, вода, воздух, земля Любая школа
							self.newprinttex("Стандартное заклинание которым овладевают все школы магии наносит урон взависимости от тех школ которыми владеет маг")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="0"
							self.CSS3="Шар стихии"
							self.cor=7
						elif self.CSS=="2" or self.CSS=="Искра": #Огонь, понижение брони Огонь 1
							self.newprinttex("Способность которой овладевают новички школы огня которая выпускает небольшой пучок огня который наносит противнику урон огнём")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="1"
							self.CSS3="Искра"
							self.cor=7
						elif self.CSS=="3" or self.CSS=="Поток пламени": #Огонь, поджог, понижение брони Огонь 2
							self.newprinttex("Поток пламени это способность которой обладают маги которые более углубились в изучении огненной магии. Это заклинание наносит огненный урон противнику и поджигает его")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="2"
							self.CSS3="Поток пламени"
							self.cor=7
						elif self.CSS=="4" or self.CSS=="Дыхание дракона": #Огонь, поджог, ужас, понижение брони Огонь 3
							self.newprinttex("Дыхание драконо это то заклинание постич которое желает каждый маг который посвятил свою жизнь огненной магии. Дыхание дракона наносит противнику большой урон от огня, поджигает, а так же имеет шанс повергнуть противника в ужас")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="3"
							self.CSS3="Дыхание дракона"
							self.cor=7
						elif self.CSS=="5" or self.CSS=="Порез ветром": #Воздух, кровотечение Воздух 1
							self.newprinttex("Порез ветром это начальное заклинание магов школы воздуха. Оно наносит урон от магии воздуха и вызывает кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="4"
							self.CSS3="Порез ветром"
							self.cor=7
						elif self.CSS=="6" or self.CSS=="Сносящий поток": #Воздух, обезоруживание Воздух 2
							self.newprinttex("Заклинание среднего уровня школы воздуха, наносит противнику урон от магии воздуха и с некоторым шансом может оглушить")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="5"
							self.CSS3="Сносящий поток"
							self.cor=7
						elif self.CSS=="7" or self.CSS=="Смерч": #Воздух, кровотечение, оглушение или обезоруживание Воздух 3
							self.newprinttex("Смерч это сильнейшее заклинание школы воздуха оно наносит большой урон от магии воздуха, вызывает кровотечение и имеет шанс оглушить врага")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="6"
							self.CSS3="Смерч"
							self.cor=7
						elif self.CSS=="8" or self.CSS=="Бросок камня": #Земля, оглушение Земля 1
							self.newprinttex("Бросок камня заклинание начального уровня наносящее урон от магии земли и с небольшим шансом оглушить")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="7"
							self.CSS3="Бросок камня"
							self.cor=7
						elif self.CSS=="9" or self.CSS=="Столб земли": #Земля, оглушение или обезоруживание земля 2
							self.newprinttex("Столб земли это заклинание наносящее урон от магии земли и с высоким шансом оглушить противника")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="8"
							self.CSS3="Столб земли"
							self.cor=7
						elif self.CSS=="10" or self.CSS=="Землетрясение": #Земля за ход, оглушение за ход или обезоруживание Земля 3
							self.newprinttex("Высшее заклинание школы земли наносящее противнику постепенный урон от магии земли каждый ход, помимо этого есть шанс оглушить противника во время действия")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="9"
							self.CSS3="Землетрясение"
							self.cor=7
						elif self.CSS=="11" or self.CSS=="Всплеск": #Вода, -поджог, ослепление Вода 1
							self.newprinttex("Всплеск это заклинание начального уровня наносящее урон от магии воды, если цель горит то она будет потушена")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="10"
							self.CSS3="Всплеск"
							self.cor=7
						elif self.CSS=="12" or self.CSS=="Гейзер": #Вода, подброс или обезоруживание Вода 2
							self.newprinttex("Гейзер это заклинание среднего уровня школы воды наносящее противнику урон от воды и с высоким шансом оглушить цель")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="11"
							self.CSS3="Гейзер"
							self.cor=7
						elif self.CSS=="13" or self.CSS=="Смертельный дождь": #Вода за ход, кровотечение, понижение брони Вода 3
							self.newprinttex("Смертельный дождь это высшее заклинание школы воды наносящее высокий урон противнику от воды в течении нескольких ходов и вызывающее кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="12"
							self.CSS3="Смертельный дождь"
							self.cor=7
						elif self.CSS=="14" or self.CSS=="Сгусток тени": #Тьма, ослепление Тьма 1
							self.newprinttex("Сгусток тени это заклинание начального уровня наносящее урон от тьмы противнику")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="13"
							self.CSS3="Сгусток тени"
							self.cor=7
						elif self.CSS=="15" or self.CSS=="Похищение здоровья": #Тьма, вампиризм Тьма 2
							self.newprinttex("Похищение здоровья заклинание наносящее противнику урон от тёмной магии и если цель является живой восстанавливает здоровье")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="14"
							self.CSS3="Похищение здоровья"
							self.cor=7
						elif self.CSS=="16" or self.CSS=="Прикосновение смерти": #Тьма, увеличение урона Тьма 3
							self.newprinttex("Прикосновение смерти высшее заклинание тёмной магии наносит высокий урон противнику от тёмной маии и если цель умерла урон от заклинания увеличивается (не действует на механойдов и нежить)")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="15"
							self.CSS3="Прикосновение смерти"
							self.cor=7
						elif self.CSS=="17" or self.CSS=="Тычёк щитом": #Физический, оглушить или молчание Баклеры 1
							self.newprinttex("Способность тычёк щитом наносит урон противнику и с малой вероятностью может оглушить")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="16"
							self.CSS3="Тычёк щитом"
							self.cor=7
						elif self.CSS=="18" or self.CSS=="Бросок щита": #Физический, обезоруживание Баклеры 2
							self.newprinttex("Бросок щита наносит противнику физический урон")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="17"
							self.CSS3="Бросок щита"
							self.cor=7
						elif self.CSS=="19" or self.CSS=="Удар щитом": #Физический, оглушить или молчание или обезоруживание Щиты 1
							self.newprinttex("Удар щитом наносит урон противнику с небольшой вероятностью оглушить")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="18"
							self.CSS3="Удар щитом"
							self.cor=7
						elif self.CSS=="20" or self.CSS=="Оглушение": #Физический, оглушить Башенные щиты 2 или Щиты 2
							self.newprinttex("Наносит противнику урон и с большой вероятностью может оглушить цель")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="19"
							self.CSS3="Оглушение"
							self.cor=7
						elif self.CSS=="21" or self.CSS=="Таран": #Физический, оглушить Башенные щиты 1
							self.newprinttex("Таран наносит удар на ходу по противнику оглушая его")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="20"
							self.CSS3="Таран"
							self.cor=7
						elif self.CSS=="22" or self.CSS=="Рассекающий порез": #Физический, кровотечение Кинжалы 1 или одноручные мечи 1 или двуручные мечи 1
							self.newprinttex("Наносит противнику удар который наносит физический урон, помимо этого у противника открывается кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="21"
							self.CSS3="Рассекающий порез"
							self.cor=7
						elif self.CSS=="23" or self.CSS=="Разрубающий удар": #Физический, кровотечение Одноручные мечи 2 или двуручные мечи 2
							self.newprinttex("Разрубающий удар наносит противнику высокий урон и открывает кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="22"
							self.CSS3="Разрубающий удар"
							self.cor=7
						elif self.CSS=="24" or self.CSS=="Заряженный взмах": #Физический, огонь, вода, воздух, земля Одноручные мечи 3 или двуручные мечи 3
							self.newprinttex("Наносит противнику физический урон, а так же урон от 4 стихий сверху")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="23"
							self.CSS3="Заряженный взмах"
							self.cor=7
						elif self.CSS=="25" or self.CSS=="Рубитькромсать": #Физический, кровотечение Одноручные топоры 1 или двуручные топоры 1
							self.newprinttex("Наносит противнику большой урон и есть возможноть кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="24"
							self.CSS3="Рубитькромсать"
							self.cor=7
						elif self.CSS=="26" or self.CSS=="Сильный удар": #Физический, оглушение  одноручные топоры 2 или двуручные топоры 2 или двуручные булавы 2 одноручные булавы 2
							self.newprinttex("Сильный удар наносит противнику урон и имеет шанс оглушать цель")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="25"
							self.CSS3="Сильный удар"
							self.cor=7
						elif self.CSS=="27" or self.CSS=="Удар с плеча": #Физический, сильное кровотечение одноручные топоры 3 или двуручные топоры 3
							self.newprinttex("Наносит противнику рубаящий удар и вызывает сильное кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="26"
							self.CSS3="Удар с плеча"
							self.cor=7
						elif self.CSS=="28" or self.CSS=="Удар с размаха": #Физический, оглушение одноручные или двуручные булавы
							self.newprinttex("Удар с размаха наносит противнику урон и с большой вероятностью оглушает цель")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="27"
							self.CSS3="Удар с размаха"
							self.cor=7
						elif self.CSS=="29" or self.CSS=="Громовой удар": #Физический, огонь, вода, воздух, земля, оглушение одноручные или двуручные булавы self.lvl 3
							self.newprinttex("Громовой удар наносит противнику физический урон, урон от стихий и с большой вероятностью оглушает цель")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="28"
							self.CSS3="Громовой удар"
							self.cor=7
						elif self.CSS=="30" or self.CSS=="Проникающий удар": #Физический урон игнорируя броню кинжалы self.lvl 2
							self.newprinttex("Проникающий удар наносит урон противнику игнорируя его броню")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="29"
							self.CSS3="Проникающий удар"
							self.cor=7
						elif self.CSS=="31" or self.CSS=="Перерезание глотки": #Физический урон игнорируя броню, кровотечение, молчание кинжалы self.lvl 3
							self.newprinttex("Перерезание глотки наносит физический урон цели игнорируя броню противника и наносит урон от кровотечения")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="30"
							self.CSS3="Перерезание глотки"
							self.cor=7
						elif self.CSS=="32" or self.CSS=="Ослепляющий удар": #Физический урон игнорируя броню, ослепление катаны 1
							self.newprinttex("Ослепляющий удар наносит противнику урон игнорируя броню противника и ослепляет врага")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="31"
							self.CSS3="Ослепляющий удар"
							self.cor=7
						elif self.CSS=="33" or self.CSS=="Удар четырёх стихий": #Физический, огонь, вода, воздух, земля катаны self.lvl 2
							self.newprinttex("Удар четырёх стихий наносит физический урон а так же урон от стихий")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="32"
							self.CSS3="Удар четырёх стихий"
							self.cor=7
						elif self.CSS=="34" or self.CSS=="Тройной удар": #Физический х3 катаны self.lvl 3
							self.newprinttex("Тройной удар наносит урон сразу в 3 точки противника")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="33"
							self.CSS3="Тройной удар"
							self.cor=7
						elif self.CSS=="35" or self.CSS=="Прикосновение духа": #Чистый урон дух 1
							self.newprinttex("Прикосновение духа наносит противнику чистый урон который не блокируется броней")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="34"
							self.CSS3="Прикосновение духа"
							self.cor=7
						elif self.CSS=="36" or self.CSS=="Разрез духа": #Чистый урон, кровотечение дух 2
							self.newprinttex("Разрез духа наносит чистый урон противнику и открывает кровотечение")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="35"
							self.CSS3="Разрез духа"
							self.cor=7
						elif self.CSS=="37" or self.CSS=="Удар духа": #Чистый урон, оглушение дух 3
							self.newprinttex("Наносит противнику чистый урон а так же имеет средний шанс оглушить")
							self.newprintCSSt("Желаете ли вы выбрать эту способность?\n1)Да\n2)Нет")
							self.CSS2="36"
							self.CSS3="Удар духа"
							self.cor=7
				elif self.cor==7: #Подтверждение активной способности
					if self.SAID[int(self.CSS2)]>2:
						self.textes="Уровень этой способности максимальный!\nИмя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки активных способностей: " + str(self.SAP) + "\nСпособности: " + str(self.SA0) + "\nВведите 0 для отмены"
						self.newprinttex(self.textes)
						self.newprintCSSt("0)Назад\nАктивные способности:   \nМагия огня 1)Шар стихии 2)Искра 3)Поток пламени 4)Дыхание дракона\nМагия воздуха 1)Шар стихии 5)Порез ветром 6)Сносящий поток 7)Смерч\nМагия земли 1)Шар стихии 8)Бросок камня 9)Столб земли 10)Землетрясение\nМагия воды 1)Шар стихии 11)Всплеск 12)Гейзер 13)Смертельный дождь\nМагия тьмы 1)Шар стихии 14)Сгуток тени 15)Похищение здоровья 16)Прикосновене смерти\nБаклеры 17)Тычёк щитом 18)Бросок щита\nЩиты 19)Удар щитом 20)Оглушение\nБашенные щиты 21)Таран 20)Оглушение\nМечи 22)Рассекающий порез 23)Разрубающий удар 24)Заряженный взмах\nТопоры 25)Рубитькромсать 26)Сильный удар 27)Удар с плеча\nБулавы 28)Удар с размаха 26)Сильный удар 29)Громовой удар\nКинжалы 22)Рассекающий порез 30)Проникающий удар 31)Перерезание глотки\nКатаны 32)Ослепляющий удар 33)Удар четырёх стихий 34)Тройной удар\nДух 35)Прикосновение духа 36)Разрез духа 37)Удар духа")
						self.cor=6
					else:
						if self.CSS=="1":
							self.SAID[int(self.CSS2)]+=1
							self.SAP-=1
							if self.SAID[int(self.CSS2)]==1:
								self.SA0.append(self.CSS3 + " self.lvl 1")
							else:
								self.SA0.remove(self.CSS3 + " self.lvl " + str(self.SAID[int(self.CSS2)]-1))
								self.SA0.append(self.CSS3 + " self.lvl " + str(self.SAID[int(self.CSS2)]))
						if self.CSS=="2" or self.CSS=="1":
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения:\nОчки активных способностей: " + str(self.SAP) + "\nСпособности: " + str(self.SA0) + "\nВведите 0 для отмены"
							self.newprinttex(self.textes)
							self.newprintCSSt("0)Назад\nАктивные способности:   \nМагия огня 1)Шар стихии 2)Искра 3)Поток пламени 4)Дыхание дракона\nМагия воздуха 1)Шар стихии 5)Порез ветром 6)Сносящий поток 7)Смерч\nМагия земли 1)Шар стихии 8)Бросок камня 9)Столб земли 10)Землетрясение\nМагия воды 1)Шар стихии 11)Всплеск 12)Гейзер 13)Смертельный дождь\nМагия тьмы 1)Шар стихии 14)Сгуток тени 15)Похищение здоровья 16)Прикосновене смерти\nБаклеры 17)Тычёк щитом 18)Бросок щита\nЩиты 19)Удар щитом 20)Оглушение\nБашенные щиты 21)Таран 20)Оглушение\nМечи 22)Рассекающий порез 23)Разрубающий удар 24)Заряженный взмах\nТопоры 25)Рубитькромсать 26)Сильный удар 27)Удар с плеча\nБулавы 28)Удар с размаха 26)Сильный удар 29)Громовой удар\nКинжалы 22)Рассекающий порез 30)Проникающий удар 31)Перерезание глотки\nКатаны 32)Ослепляющий удар 33)Удар четырёх стихий 34)Тройной удар\nДух 35)Прикосновение духа 36)Разрез духа 37)Удар духа")
							self.cor=6
				elif self.cor==8: #Основная характеристика
					if self.CSS=="1":
						self.weapon="power"
					elif self.CSS=="2":
						self.weapon="agility"
					elif self.CSS=="3":
						self.weapon="magic"
					self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаша текущая характеристика: "
					if self.weapon=="power":
						self.textes+="Сила"
					elif self.weapon=="agility":
						self.textes+="Ловкость"
					elif self.weapon=="magic":
						self.textes+="Мудрость"
					else:
						self.textes+="Отсутствует"
					self.newprintCSSt("1)Сила\n2)Ловкость\n3)Мудрость\n0)Назад")
					self.newprinttex(self.textes)
					if self.CSS=="0":
						self.func="Прокачка персонажа"
						self.cor=1
						self.textes="Вы не можете начать игру с здоровьем равным нулю или непотраченными очками характеристик\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\nКоличество очков характеристик: " + str(self.P) + "\nКоличество очков пассивных способностей: " + str(self.SP) + "\nКоличество очков активных способностей: " + str(self.SAP)
						self.newprinttex(self.textes)
						self.newprintCSSt("Что вы желаете распределить:\n1)Очки характеристик\n2)Очки пассивных способностей\n3)Очки активных способностей\n4)Выбрать основную характеристику\n0)Начать игру")
				elif self.cor==9: #Уменьшение очков
					if self.CSS2=="Сила":
						if int(self.CSS)>self.S:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("У вас недостаточно силы\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
						else:
							self.P+=int(self.CSS)
							self.S-=int(self.CSS)
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
					elif self.CSS2=="Мудрость":
						if int(self.CSS)>self.M:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("У вас недостаточно мудрости\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
						else:
							self.P+=int(self.CSS)
							self.M-=int(self.CSS)
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
					elif self.CSS2=="Ловкость":
						if int(self.CSS)>self.A:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("У вас недостаточно ловкости\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
						else:
							self.P+=int(self.CSS)
							self.A-=int(self.CSS)
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
					elif self.CSS2=="Выносливость":
						if int(self.CSS)>self.H:
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("У вас недостаточно выносливости\nКакую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
						else:
							self.P+=int(self.CSS)
							self.H-=int(self.CSS)
							self.textes="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nТекущие значения: " + "\nКоличество очков характеристик: " + str(self.P) + "\nСила: " + str(self.S) + "\nЛовкость: " + str(self.A) + "\nМудрость: " + str(self.M) + "\nЗдоровье: " + str(self.H)
							self.newprinttex(self.textes)
							self.newprintCSSt("Какую характеристику изменить?\n1)Повысить силу\n2)Повысить ловкость\n3)Повысить мудрость\n4)Повысить выносливость\n5)Понизить силу\n6)Понизить ловкость\n7)Понизить мудрость\n8)Понизить выносливость\n0)Назад")
							self.cor=2
			elif self.func=="Оплот надежды":
				if self.cor==0:
					self.newprinttex("После перемещения вы оказались в неизвестном вам ранее месте первое что вам бросилось в глаза это несколько живых людей на расстоянии несколько сотен метров, а за ними возвышалась крепость вглядевшись в которую вы дали ясно себе понять что этот город живой.")
					self.newprintCSSt("Продолжить...")
					self.cor=1
				elif self.cor==1:
					self.newprinttex("Вы находитесь возле портала ведущего к месту откуда вы пришли")
					self.newprintCSSt("1)Идти в крепость\n2)Войти в портал")
					self.cor=2
				elif self.cor==2:
					if self.CSS=="1" and zlo==0:
						self.newprinttex("Вы шли в сторону замка до тех пор пока не добрались до его врат. Врата были распахнуты.")
						self.newprintCSSt("1)Идти на центральную площадь\n2)Идти к порталу")
						self.cor=3
					elif self.CSS=="1" and zlo==1:
						self.newprinttex("Крепость в огне кококо")
						self.newprintCSSt("1)Умереть")
						self.cor=3
					elif self.CSS=="2":
						self.func="Игра"
						self.newprinttex(self.locatDisc)
						self.newprintCSSt(self.locatCSS)
				elif self.cor==3:
					if self.CSS=="1":
						self.newprinttex("Вы находитесь в центре крепости в которой цветёт жизнь и люди кругом ходят, суетятся у каждого свои мысли на голове и по выражению их лиц не скажешь что существуют такие места из которых вы пришли.")
						self.textes="1)В мерию\n2)В торговую лавку\n3)В кузню\n4)В трактир\n5)В книжную лавку\n6)К стенду с объявлениями"
						if theftguild==1:
							self.textes+="\n6)В гильдию воров"
						self.textes+="\n0)Вернуться к воротам"
						self.newprintCSSt("1)В мерию\n2)В торговую лавку\n3)В кузню\n4)В трактир\n5)В книжную лавку\n6)К стенду с объявлениями")
						self.cor=4
					elif self.CSS=="2":
						self.newprinttex("Вы находитесь возле портала ведущего к месту откуда вы пришли")
						self.newprintCSSt("1)Идти в крепость\n2)Войти в портал")
						self.cor=1		
			if self.func=="Игра" and self.part>0:
				self.stats="Локация: "+ self.locatCur +"\nЗдоровье: " + str(self.HP) + "/" + str(self.FHP) + "\nРесурс: " + str(self.MP) +"/"+str(self.FMP)
				self.newprintstat(self.stats)
			elif self.func=="Бой" and self.part>0 and self.cor>0:
				self.stats="Герой: \nЗдоровье: " + str(self.HP) + "/" + str(self.FHP) + "\nРесурс: " + str(self.MP) +"/"+str(self.FMP) + "\n\nВраг: " + str(self.Ename)
				if self.SID[24]==0:
					self.stats+="\nЗдоровье: неизвестно\nРесурс: неизвестно"
				elif self.SID[24]==1:
					self.stats+="\nЗдоровье: " + str(self.EHP) + "/" + str(self.EFHP) + "\nРесурс: " + str(self.EMP) +"/"+str(self.EFMP) 
				self.newprintstat(self.stats)
			elif (self.func=="Инвентарь" or self.func=="Прокачка персонажа") and self.part>0:
				self.AS[0]=self.AS[1]+self.AS[2]+self.AS[3]+self.AS[4]+self.AS[5]+self.AS[6]; self.AM[0]=self.AM[1]+self.AM[2]+self.AM[3]+self.AM[4]+self.AM[5]+self.AM[6]; self.AA[0]=self.AA[1]+self.AA[2]+self.AA[3]+self.AA[4]+self.AA[5]+self.AA[6]; self.AH[0]=self.AH[1]+self.AH[2]+self.AH[3]+self.AH[4]+self.AH[5]+self.AH[6]
				self.FireRes[0]=self.FireRes[1]+self.FireRes[2]+self.FireRes[3]+self.FireRes[4]+self.FireRes[5]+self.FireRes[6]; self.WaterRes[0]=self.WaterRes[1]+self.WaterRes[2]+self.WaterRes[3]+self.WaterRes[4]+self.WaterRes[5]+self.WaterRes[6]
				self.EarthRes[0]=self.EarthRes[1]+self.EarthRes[2]+self.EarthRes[3]+self.EarthRes[4]+self.EarthRes[5]+self.EarthRes[6]; self.AirRes[0]=self.AirRes[1]+self.AirRes[2]+self.AirRes[3]+self.AirRes[4]+self.AirRes[5]+self.AirRes[6]
				self.PhisRes[0]=self.PhisRes[1]+self.PhisRes[2]+self.PhisRes[3]+self.PhisRes[4]+self.PhisRes[5]+self.PhisRes[6]; self.BleedRes[0]=self.BleedRes[1]+self.BleedRes[2]+self.BleedRes[3]+self.BleedRes[4]+self.BleedRes[5]+self.BleedRes[6]
				self.PoisRes[0]=self.PoisRes[1]+self.PoisRes[2]+self.PoisRes[3]+self.PoisRes[4]+self.PoisRes[5]+self.PoisRes[6];
				self.Block[0]=self.Block[1]+self.Block[2]+self.Block[3]+self.Block[4]+self.Block[5]+self.Block[6];self.Dodge[0]=self.Dodge[1]+self.Dodge[2]+self.Dodge[3]+self.Dodge[4]+self.Dodge[5]+self.Dodge[6]
				self.FS=self.S+self.AS[0]; self.FM=self.M+self.AM[0]; self.FA=self.A+self.AA[0]; self.FH=self.H+self.AH[0]; self.FHP=self.FH*5; self.FMP=self.FM*5
				if self.weapon=="power":
					self.uron=round((self.atk[0]+self.atkp)*(self.FS*0.08+self.FA*0.06+self.FM*0.04))
				elif self.weapon=="agility":
					self.uron=round((self.atk[0]+self.atkp)*(self.FA*0.08+self.FM*0.06+self.FS*0.04))
				elif self.weapon=="magic":
					self.uron=round((self.atk[0]+self.atkp)*(self.FM*0.08+self.FS*0.06+self.FA*0.04))
				self.stats="Имя персонажа: " + self.name + "\nНазвание класса: " + self.classname + "\nВаш уровень: " + str(self.lvl) + "\nОпыт: " + str(self.exp) + "/" + str(self.expup) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nТекущие значения:\nСила(Свои/предметы): " + str(self.FS) + " (" + str(self.S) + "/" + str(self.AS[0]) + ")\nЛовкость(Свои/предметы): " + str(self.FA) + " (" + str(self.A) + "/" + str(self.AA[0]) + ")\nМудрость(Свои/предметы): " + str(self.FM) + " (" + str(self.M) + "/" + str(self.AM[0]) + ")\nЗдоровье(Свои/предметы: )" + str(self.FH) + " (" + str(self.H) + "/" + str(self.AH[0]) + ")\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nСпособности: " + str(self.S0) + "\nАктивные способности: " + str(self.SA0) + "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nОчки здоровья: " + str(self.HP) + "/" + str(self.FHP) + "\nОчки ресурса: " + str(self.MP) + "/" + str(self.FMP) + "\nУрон: " + str(self.uron)
				self.stats+="\nОсновная характеристика оружия: "
				if self.weapon=="power":
					self.stats+="Сила"
				elif self.weapon=="agility":
					self.stats+="Ловкость"
				elif self.weapon=="magic":
					self.stats+="Разум"
				self.stats+= "\n|~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\nБроня: " + str(self.PhisRes[0]) + "\nЗащита от огня: " + str(self.FireRes[0]) + "\nЗащита от воды: " + str(self.WaterRes[0]) + "\nЗащита от земли: " + str(self.EarthRes[0]) + "\nЗащита от воздуха: " + str(self.AirRes[0]) + "\nЗащита от кровотечения: " + str(self.BleedRes[0]) + "\nЗащита от яда: " + str(self.PoisRes[0]) + "\nЗащита от контроля: " + str(self.ControllRes[0]) + "\nБлок: " + str(self.Block[0]) + "\nУворот: " + str(self.Dodge[0])
				self.newprintstat(self.stats)
			print(self.func,self.path,self.part,"\n",self.inventID,"\n",self.id)

		
StartGame = GameMain()

try:
	os.remove("Data\\WeaArmListtime.data")
except:
	None

os._exit(0)
