from urllib.request import urlopen
from bs4 import BeautifulSoup
#from telegram import InlineQueryResultArticle, InputTextMessageContent

def cineminha(near, date=0, time=0, sort=0, q='', hl='pt-br', info=False):
	url = "http://google.com/movies?near={}&date={}&time={}&sort={}&hl={}".format(near, date, time, sort, hl)
	if q!='':
		url += '&q='+q
	soup = BeautifulSoup(urlopen(url).read(),'html.parser').find_all("div", class_="movie_results")[0]
	response = ''

	for div in soup.children:
		if div["class"][0] == 'theater':
			response += '*- '+div.h2.get_text()+' -*\n\n'

			for movie in div.find_all("div", class_="movie"):
				response += '*'+movie.a.get_text()+'*\n_'
				response += movie.span.get_text()+'_\n'

				for time in movie.find_all("span", style='color:#666'):
					response += time.get_text()+''
				for time in movie.find_all("span", style='color:'):
					response += '*'+time.get_text()+'*'

				response += '\n\n'
			response += '\n'

	return response

print(cineminha('Rua Indiana, 86'))