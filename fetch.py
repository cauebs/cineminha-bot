from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from telegram import Emoji, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

def serialize(near, date=0, time=0, sort=0, q='', hl='pt-br'):

	url = "http://google.com/movies?near={}&date={}&time={}&sort={}&hl={}".format(quote(near), date, time, sort, hl)
	if q!='':
		url += '&q='+quote(q)

	soup = BeautifulSoup(urlopen(url).read(),'html.parser')
	body = soup.find_all("div", class_="movie_results")
	response = []

	days = []
	div = soup.find_all("div", class_="section")[1]
	for i in div.children:
		days.append(i.get_text().replace('›','').strip())	
	response.append(days)

	if len(body) > 0:	
		for div in body[0].children:

			if div["class"][0] == 'theater':
				theater = {}
				theater["type"] = "theater"
				theater["name"] = div.h2.get_text()
				theater["info"] = div.find_all("div", class_="info")[0].get_text()
				theater["movies"] = []

				for m in div.find_all("div", class_="movie"):
					movie = {}
					movie["name"] = m.a.get_text()
					if movie["name"] == '':
						continue
					movie["info"] = m.span.get_text()
					movie["times"] = {"dub":[],"leg":[]}
					times = m.find_all("div", class_="times")[0]
					lang = ""
					if "Dublado" in movie["info"]:
						lang = "dub"
					if "Legendado" in movie["info"]:
						lang = "leg"

					if lang == '' and "Dublado" not in times.get_text() and "Legendado" not in times.get_text():
						lang = "dub"

					if lang != "":
						for time in times.find_all("span", style='color:#666'):
							movie["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times.find_all("span", style='color:'):
							movie["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')
					else:		
						timesplit = str(times).split('<br>')
						times1 = BeautifulSoup(timesplit[0],'html.parser')
						if "Legendado" in times1.get_text():
							lang = "leg"
						else: 
							lang = "dub"	
						for time in times1.find_all("span", style='color:#666'):
							movie["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times1.find_all("span", style='color:'):
							movie["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')

						if len(timesplit) > 1:
							times2 = BeautifulSoup(timesplit[1],'html.parser')
							if "Legendado" in times2.get_text():
								lang = "leg"
							else: 
								lang = "dub"
							for time in times2.find_all("span", style='color:#666'):
								movie["times"][lang].append(time.get_text().replace('\xa0','').strip())
							for time in times2.find_all("span", style='color:'):
								movie["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')

					theater["movies"].append(movie)

				response.append(theater)

			if div["class"][0] == 'movie':
				movie = {}
				movie["type"] = "movie"
				movie["name"] = div.h2.get_text()
				movie["info"] = div.find_all("div", class_="info")[0].get_text().split('Diretor')[0]
				movie["theaters"] = []

				for t in div.find_all("div", class_="theater"):
					theater = {}
					theater["name"] = t.a.get_text()
					theater["times"] = {"dub":[],"leg":[]}
					times = t.find_all("div", class_="times")[0]
					lang = ""
					if "Dublado" in movie["info"]:
						lang = "dub"
					if "Legendado" in movie["info"]:
						lang = "leg"

					if lang == '' and "Dublado" not in times.get_text() and "Legendado" not in times.get_text():
						lang = "dub"

					if lang != "":
						for time in times.find_all("span", style='color:#666'):
							theater["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times.find_all("span", style='color:'):
							theater["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')
					else:
						timesplit = str(times).split('<br>')
						times1 = BeautifulSoup(timesplit[0],'html.parser')
						if "Legendado" in times1.get_text():
							lang = "leg"
						else: 
							lang = "dub"	
						for time in times1.find_all("span", style='color:#666'):
							theater["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times1.find_all("span", style='color:'):
							theater["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')

						if len(timesplit) > 1:
							times2 = BeautifulSoup(timesplit[1],'html.parser')
							if "Legendado" in times2.get_text():
								lang = "leg"
							else: 
								lang = "dub"
							for time in times2.find_all("span", style='color:#666'):
								theater["times"][lang].append(time.get_text().replace('\xa0','').strip())
							for time in times2.find_all("span", style='color:'):
								theater["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')

					movie["theaters"].append(theater)

				response.append(movie)

	return response

def cineminha(info):
	response = []

	if len(info)==0:
		text = '*Não foi encontrado nenhum resultado.*\nTente outra coisa ou atualize sua localização'
		response.append(text)

	else:
		for i in info:
			if i["type"] == 'theater' and len(i["movies"]) > 0:
				t = Emoji.MOVIE_CAMERA+' *'+i["name"]+'*\n'
				for movie in i["movies"]:
					t += '\n• '+movie["name"]+' '
					desc = movie["info"].split('-')
					#if detail and len(desc)>1:
					#	t += '\n'+desc[0].strip()+' - '+desc[1].strip()
					#else:
					t += '('+desc[0].strip()+')'
					t += '\n'
					if len(movie["times"]["dub"]) > 0:
						t += 'Dublado: '
						for time in movie["times"]["dub"]:
							t += time + '  '
						t += '\n'
					if len(movie["times"]["leg"]) > 0:
						t += 'Legendado: '
						for time in movie["times"]["leg"]:
							t += time + '  '
						t += '\n'
				response.append(t)

			if i["type"] == 'movie':
				m = Emoji.CLAPPER_BOARD+' *'+i["name"]+'*\n'
				m += i["info"]+'\n'
				for theater in i["theaters"]:
					m += '\n• '+theater["name"]+'\n'
					if len(theater["times"]["dub"]) > 0:
						m += 'Dublado: '
						for time in theater["times"]["dub"]:
							m += time + '  '
						m += '\n'
					if len(theater["times"]["leg"]) > 0:
						m += 'Legendado: '
						for time in theater["times"]["leg"]:
							m += time + '  '
						m += '\n'
				response.append(m)
	return response


def inline(loc, query):
	results = []
	info = serialize(loc, q=query, sort=1)[1:]
	if len(info)==0:
		title = 'Não foi encontrado nenhum resultado'
		desc = 'Tente outra coisa ou atualize sua localização'
		msg = InputTextMessageContent('*'+title+'*\n'+desc,parse_mode="Markdown")
		results.append(InlineQueryResultArticle(0,title,msg,description=desc))
	else:
		for i in info:
			title = i["name"]
			desc = i["info"]
			msgtext = cineminha([i])[0]
			message = InputTextMessageContent(msgtext, parse_mode="Markdown")
			results.append(InlineQueryResultArticle(str(len(results)), title, message, description=desc))
	return results

a = serialize('Palhoça')
print(a[0])