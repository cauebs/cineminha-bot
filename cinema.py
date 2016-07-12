from urllib.request import urlopen
from bs4 import BeautifulSoup
#from telegram import InlineQueryResultArticle, InputTextMessageContent

class Cineminha():

	def cinema(location, date_offset=0):
		url = 'http://google.com/movies?near='
		url += location + '&date=' + date_offset
		source = urlopen(url).read()
		soup = BeautifulSoup(source,'html.parser').find_all("div", class_="movie_results")[0]
		for div in soup.find_all('span')[0:-1]:
			if span.get('style')=="font-size:16px;" and span.strong is not None:
				strong = span.strong.get_text()

				nome = span.a.get_text()
				data = strong.split(' - ')[0]
				horario = strong.split(' - ')[1].replace(':','').strip()
				link = span.a.get('href')
				ing_soup = BeautifulSoup(urlopen(link).read(),'html.parser')
				ing_strong = ing_soup.find_all('strong')
				ingresso = ''
				for strong in ing_strong:
					if "Ingressos:" in strong.get_text():
						ingresso = strong.parent.get_text().replace('Ingressos:','').strip()
						if ingresso=='':
							i = 0
							for div in strong.parent.find_next_siblings():
								if div.get_text().strip()!='':
									ingresso += div.get_text().replace('\n','').replace('\t','').strip()+'\n'
								i = i+1
								if i>=5:
									break

				e = Evento(nome,datetime.strptime(data, '%d/%m/%Y'),horario,link,ingresso)
				self.lista.append(e)
