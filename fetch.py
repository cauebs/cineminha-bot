from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
#from telegram import InlineQueryResultArticle, InputTextMessageContent

def serialize(url):
	soup = BeautifulSoup(urlopen(url).read(),'html.parser').find_all("div", class_="movie_results")
	response = []

	if len(soup) > 0:	
		for div in soup[0].children:

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


def cineminha(near, date=0, time=0, sort=0, q='', hl='pt-br', detail=False):

	url = "http://google.com/movies?near={}&date={}&time={}&sort={}&hl={}".format(quote(near), date, time, sort, hl)
	if q!='':
		url += '&q='+q

	info = serialize(url)

	response = []

	if len(info)==0:
		text = '*Não foi encontrado nenhum resultado.*\nTente alterar a sua localização'
		response.append(text)
	else:
		for i in info:
			if i["type"] == 'theater' and len(i["movies"]) > 0:
				t = '*'+i["name"]+'*\n'
				for movie in i["movies"]:
					t += '\n*'+movie["name"]+'* '
					desc = movie["info"].split('-')
					if detail and len(desc)>1:
						t += '\n'+desc[0].strip()+' - '+desc[1].strip()
					else:
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
				t = '*'+i["name"]+'*\n'
				t += i["info"]+'\n'
				for theater in i["theaters"]:
					t += '\n'+theater["name"]+'\n'
					if len(theater["times"]["dub"]) > 0:
						t += 'Dublado: '
						for time in theater["times"]["dub"]:
							t += time + '  '
						t += '\n'
					if len(theater["times"]["leg"]) > 0:
						t += 'Legendado: '
						for time in theater["times"]["leg"]:
							t += time + '  '
						t += '\n'
				response.append(t)

	return response

print(cineminha('Palhoça', detail=True))