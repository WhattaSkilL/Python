import vk, time, random, sys, requests, json, fleep, os

token = ""

class VkBot:
	def __init__(self):
		global CSS
		session = vk.Session(access_token=token)
		self.api = vk.API(session)
		self.message = [0]
		self.api.messages.send(chat_id=101, message="Йо я онлайн!")
		CSS=0
		self.isGame=False
		self.isGameEnd=False
		self.playersList=[]
		self.t0 = time.time()
	
	def __exit__(self):
		self.api.messages.send(chat_id=101, message="Всем пока!")
	
	def CheckMessage(self, TimeWait):
		global CSS
		VremyaVipoln=time.time()-self.t0
		print("Время выполнения: ",VremyaVipoln)
		if (TimeWait>VremyaVipoln):
			time.sleep(TimeWait-VremyaVipoln)
			self.t0 = time.time()
			LastMesege = self.message[0]
			self.message =  self.api.messages.get(time_offset=TimeWait)
		else:
			self.t0 = time.time()
			LastMesege = self.message[0]
			self.message =  self.api.messages.get(time_offset=VremyaVipoln)
		print(self.message)
		if (len(self.message) > 1 and self.message[0] > LastMesege):
			for i in self.message[1:]:
				self.i=i
				self.TXTMes = self.i["body"].lower()
				print(f"CSS: {CSS}, Сообщение: {self.TXTMes}")
				SpisokSlov = self.TXTMes.split(' ')
				if (SpisokSlov[0].find("ваттабот") > -1 or SpisokSlov[0].find("whattabot") > -1 or SpisokSlov[0].find("ватт") > -1 or SpisokSlov[0].find("wht") > -1):
						for c in SpisokSlov[1:]:
							print(c)
							if CSS==0:
								if (c.find("привет")> -1 or c.find("йо")> -1):
									self.SendMessage(MessageForSend="И тебе привет")
									print(f"Ответил на !Привет: {i['uid']}")
									break
								elif (c.find("кто")> -1):
									randomPerson = random.choice(self.api.messages.getChatUsers(chat_id=101, fields="last"))
									self.SendMessage(MessageForSend=f"{random.choice(['Я думаю это ', 'Вероятно это ', 'Очевидно это '])}{randomPerson['first_name']} {randomPerson['last_name']}")
									print(f"Ответил на !Кто: {i['uid']}")
									break
								elif (c.find("когда")> -1):
									self.SendMessage(MessageForSend=f"{random.choice(['Скоро', 'Никогда', 'Завтра', 'Сегодня', 'На следующей неделе', 'Уже', 'Сань хуй соси'])}")
									print(f"Ответил на !Когда: {i['uid']}")
									break
								elif (c.find("инфа")> -1):
									self.SendMessage(MessageForSend=f"Около {random.randint(0, 100)}%")
									print(f"Ответил на !Инфа: {i['uid']}")
									break
								elif (c.find("где")> -1):
									self.SendMessage(MessageForSend=f"{random.choice(['На помойке', 'В жопе', 'Дома', 'На работе', 'В школке', 'В шараге', 'В общаге', 'На дне','В канаве'])}")
									print(f"Ответил на !Где: {i['uid']}")
									break
								elif (c.find("omae wa mou shienderu")> -1):
									self.SendMessage(MessageForSend="NANI?!")
									print(f"Ответил на !ОМАЕ ВА: {i['uid']}")
									break
								elif (c.find("хелп")> -1):
									self.SendMessage(MessageForSend="Меню: Главное меню\nЙо! Вот список того что я могу: \n1)Здороваться на команду: привет \n2)Спросить кто есть кто: кто [Кто] \n3)Могу ответить когда случится событие: когда \n3)Могу ответить какой процент командой: инфа \n 4)Могу указать место положения чего либо командой: где [Что \ Кто]\n5)Могу скинуть видео по запросу командой: youtube [Запрос] \n6)Могу найти картинку(Не работает) командой: картинка [название]")
									print(f"Ответил на !помощь: {i['uid']}")
									break
								elif (c.find("youtube")> -1):
									self.SendMessage(MessageForSend="Лови", File=self.VideoSearch(self.TXTMes[self.TXTMes.find("youtube"):]))
									print(f"Ответил на !Видео: {i['uid']}")
									break
								elif (c.find("картинка")> -1):
									self.SendMessage(MessageForSend="Лови", File=self.ImageSearch(self.TXTMes[self.TXTMes.find("картинка"):]))
									print(f"Ответил на !картинка: {i['uid']}")
									break
								elif (c.find("конкурсы")> -1):
									self.SendMessage(MessageForSend="Хотите конкурсы? Выбирайте:\n1)Угадай число\n2)Угадать картинку\n3)Виселица\n4)Города\n0)Назад")
									CSS=1
									print(f"Ответил на !Конкурсы: {i['uid']}")
									break
								else:
									self.SendMessage(MessageForSend='Я вас не понял если вы забыли список возможных команд наберите "Хелп"')
									print(f"Ответил на !Непоал: {i['uid']}")
									break
							elif CSS==1:
								if (c.find("1")> -1 or c.find("числ")> -1):
									self.SendMessage(MessageForSend=f'Суть игры заключается в следующем: вы должны угадать число которое я загадал. Человек который будет ближе всего к ответу победит. Для участия в игре напишите "Ватт я" после этого когда все игроки соберутся напишите "Ватт готовы" и после этого игра начнётся')
									self.playersList=[]
									CSS=2
									print(f"Ответил на !Выбор конкурса 1: {i['uid']}")
									break
								elif (c.find("2")> -1 or c.find("картинк")> -1):
									self.SendMessage(MessageForSend=f'Суть следующая я показываю картинку которая видоизмененна до неузнаваемости ваша же цель узнать что находится на картинке. Для участия в игре напишите "Ватт я" после этого когда все игроки соберутся напишите "Ватт готовы" и после этого игра начнётся')
									self.playersList=[]
									CSS=2
									print(f"Ответил на !Выбор конкурса 2: {i['uid']}")
									break
								elif (c.find("хелп")> -1):
									self.SendMessage(MessageForSend="Меню: Меню конкурсов\nЙо! Вот список текущих действий:\n1)Угадай число\n2)Угадать картинку\n3)Виселица\n4)Города\n0)Назад")
									print(f"Ответил на !помощь: {i['uid']}")
									break
								else:
									self.SendMessage(MessageForSend='Я вас не понял если вы забыли список возможных команд наберите "Хелп"')
									print(f"Ответил на !Непоал: {i['uid']}")
									break
							elif CSS==2:
								if (c.find("я")> -1):
									if self.playersList.count(i['uid'])==0:
										self.SendMessage(MessageForSend='Ты принят')
										self.playersList.append(i['uid'])
									else:
										self.SendMessage(MessageForSend='Ты уже в игре')
									print(f"Ответил на !Я: {i['uid']}")
									break
								elif (c.find("готов")> -1 and len(self.playersList)<1):
									self.SendMessage(MessageForSend='Игроков то нет пишите "Ватт я" чтобы принять участие')
									print(f"Ответил на !ГотовНо0: {i['uid']}")
									break
								elif (c.find("готов")> -1):
									PlayersName=""
									for Player in self.api.users.get(user_ids=self.playersList):
										PlayersName += f"\n{Player['first_name']} {Player['last_name']}"
									self.SendMessage(MessageForSend=f'Ну чтож приступим к игре :) называйте число в формате "Ватт [Число]"\n В игре учавствуют: {PlayersName}')
									CSS=3
									print(f"Ответил на !Готов: {i['uid']}")
									break
								elif (c.find("хелп")> -1):
									self.SendMessage(MessageForSend='Меню: Меню подтверждения\nЙо! Вот список текущих действий:\n1)Подтвердить участие командой "Я"\n2)Потвердить готовность командой "готовы"\n3)Вернуться в меню выбора игры командой "Назад"\n0)Выход в главное меню')
									print(f"Ответил на !Помощь: {i['uid']}")
									break
								elif (c.find("3")> -1 or c.find("назад")> -1):
									self.SendMessage(MessageForSend="Хотите конкурсы? Выбирайте:\n1)Угадай число\n2)Угадать картинку\n3)Виселица\n4)Города\n0)Назад")
									CSS=1
									print(f"Ответил на !Конкурсы: {i['uid']}")
									break
								elif (c.find("0")> -1 or c.find("меню")> -1):
									self.SendMessage(MessageForSend="Как хотите")
									CSS=0
									print(f"Ответил на !Меню: {i['uid']}")
									break
								else:
									self.SendMessage(MessageForSend='Я вас не понял если вы забыли список возможных команд наберите "Хелп"')
									print(f"Ответил на !Непоал: {i['uid']}")
									break
							elif CSS==3:
								if not self.i['uid'] in self.playersList:
									self.SendMessage(MessageForSend='Прошу прощения, но в данный момент идёт игра')
								else:
									self.SendMessage(MessageForSend='Типо игра')
								break
															
	def SendMessage(self, MessageForSend=None, Resend="On", File=None):
		if(Resend=="On"):
			self.api.messages.send(chat_id=101, message=MessageForSend, forward_messages=self.i["mid"], attachment=File)
		elif (Resend=="Off"):
			self.api.messages.send(chat_id=101, message=MessageForSend, attachment=File)
	
	def ImageSearch(self, ImageName):
		response = requests.get(f"https://yandex.ru/images/search?text={ImageName}")
		textResponse = response.text
		mesto = 0
		Ssilki = []
		while len(Ssilki) < 10:
			PoiskWatch = textResponse.find(',"img_href":"', mesto)
			mesto = textResponse.find('","', PoiskWatch)
			ssilka = textResponse[PoiskWatch + 13: mesto]
			Ssilki.append(ssilka)
		while True:
			randomEto = random.choice(Ssilki)
			print("ССылка: ", randomEto)
			p = requests.get(randomEto)
			with open("img.png", "wb") as file_handler:
				file_handler.write(p.content)
			with open("img.png", "rb") as file_handler:
				b = requests.post(self.api.photos.getMessagesUploadServer()['upload_url'], files={'photo': file_handler}).json()
			try:
				c = self.api.photos.saveMessagesPhoto(photo=b["photo"], server=b["server"], hash=b["hash"])
				break
			except:
				continue
		return f"{c[0]['id']}"
	
	def VideoSearch(self, VideoName):
		response = requests.get(f"https://www.youtube.com/results?search_query={VideoName}")
		textResponse = response.text
		mesto = 0
		Ssilki = []
		while len(Ssilki) < 8:
			PoiskWatch = textResponse.find("/watch?v=", mesto)
			mesto = textResponse.find('\"', PoiskWatch)
			ssilka = textResponse[PoiskWatch: mesto]
			print("Сcылка: ", ssilka)
			Ssilki.append(ssilka)
		randomEto = random.choice(Ssilki)
		Videos = self.api.video.save(name="Видос по запросу", is_private=1, link=f"https://www.youtube.com{randomEto}")
		requests.get(f'{Videos["upload_url"]}')
		return f"video{Videos['owner_id']}_{Videos['vid']}_{Videos['access_key']}"
		

vk = VkBot()

while True:
	try:
		vk.CheckMessage(3)
	except:
		print("Unexpected error:", sys.exc_info())
		with open("log.txt", "a") as file_handler:
			file_handler.write("Unexpected error:", sys.exc_info())
	
