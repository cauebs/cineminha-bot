from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
#from telegram import InlineQueryResultArticle, InputTextMessageContent

def cineminha(near, date=0, time=0, sort=0, q='', hl='pt-br', info=False):
	url = "http://google.com/movies?near={}&date={}&time={}&sort={}&hl={}".format(quote(near), date, time, sort, hl)
	if q!='':
		url += '&q='+q
	soup = BeautifulSoup(urlopen(url).read(),'html.parser').find_all("div", class_="movie_results")[0]
	response = []
	c = 0
	for div in soup.children:
		if div["class"][0] == 'theater':
			response.append('')
			response[c] += '*- '+div.h2.get_text()+' -*\n\n'

			for movie in div.find_all("div", class_="movie"):
				response[c] += '*'+movie.a.get_text()+'*\n_'
				response[c] += movie.span.get_text()+'_\n'

				for time in movie.find_all("span", style='color:#666'):
					response[c] += time.get_text()+''
				for time in movie.find_all("span", style='color:'):
					response[c] += '*'+time.get_text()+'*'

				response[c] += '\n\n'
			c += 1

	return response
