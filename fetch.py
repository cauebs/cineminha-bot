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
					movie["info"] = m.span.get_text()
					movie["times"] = {"dub":[],"leg":[]}
					times = m.find_all("div", class_="times")[0]
					lang = ""
					if "Dublado" in movie["info"]:
						lang = "dub"
					if "Legendado" in movie["info"]:
						lang = "leg"

					if "Dublado" not in times.get_text() and "Legendado" not in times.get_text():
						lang = "dub"

					if lang != "":
						for time in times.find_all("span", style='color:#666'):
							movie["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times.find_all("span", style='color:'):
							movie["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')
					else:
						
						
						times1 = BeautifulSoup(str(times).split('<br>')[0],'html.parser')
						times2 = BeautifulSoup(str(times).split('<br>')[1],'html.parser')
						
						if "Legendado" in times1.get_text():
							lang = "leg"
						else: 
							lang = "dub"	
						for time in times1.find_all("span", style='color:#666'):
							movie["times"][lang].append(time.get_text().replace('\xa0','').strip())
						for time in times1.find_all("span", style='color:'):
							movie["times"][lang].append('*'+time.get_text().replace('\xa0','').strip()+'*')

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
				pass

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
		for theater in info:
			if theater["type"] == 'theater':
				t = '*'+theater["name"]+'*'
				if detail:
					t += '_'+theater["info"]+'_'

				for movie in theater["movies"]:
					t += '\n\n*'+movie["name"]+'*\n'
					t += '_'+movie["info"]+'_\n'
					if len(movie["times"]["dub"]) > 0:
						t += 'Dublado: '
						for time in movie["times"]["dub"]:
							t += time + '  '
					if len(movie["times"]["leg"]) > 0:
						t += 'Legendado: '
						for time in movie["times"]["leg"]:
							t += time + '  '
			response.append(t)

	return response
	