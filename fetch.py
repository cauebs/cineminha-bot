import requests
from requests.utils import quote
from bs4 import BeautifulSoup
from telegram import Emoji, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import os, textos

lang = os.environ.get('lang')

def serialize(near, date=0, time=0, sort=0, q='', id=''):

	url = "http://google.com/movies?near={}&date={}&time={}&hl={}".format(quote(near), date, time, lang)

	if id!='':
		url += "&"+id
	elif q!='':
		url += '&q='+quote(q)
	else:
		url += "&sort=" + str(sort)

	soup = BeautifulSoup(requests.get(url).text,'html.parser')
	body = soup.find_all("div", class_="movie_results")
	response = []

	days = []
	div = soup.find_all("div", class_="section")[1]
	for i in div.children:
		days.append(i.get_text().replace('›','').strip())	
	response.append(days)

	if len(body) > 0:	
		for div in body[0].children:
			parent = {}
			parent["type"] = div["class"][0]
			parent["name"] = div.h2.get_text()
			parent["id"] = div.a['href'].split('&')[-1]
			if parent["type"] == "movie":
				infos = div.find_all("div", class_="info")
				if infos[0]["class"] == ["info"]:
					parent["info"] = infos[0].get_text().split('Dire')[0]
				else:
					parent["info"] = infos[1].get_text().split('Dire')[0]
			else:
				parent["info"] = div.find_all("div", class_="info")[0].get_text()
			parent["children"] = []

			if parent["type"] == "movie":
				child_type = "theater"
			elif parent["type"] == "theater":
				child_type = "movie"

			for c in div.find_all("div", class_=child_type):
				child = {}
				child["name"] = c.a.get_text()
				child["type"] = child_type
				if child["name"] == '':
					continue
				try:
					if child_type == "movie":
						child["info"] = c.span.get_text("#", strip=True).split("#")[0]
						if child["info"][-1]=='-':
							child["info"] = child["info"][0:-1]
					else:
						child["info"] = c.find_all("div", class_="address")[0].get_text()
				except:
					child["info"] = ""
				child["times"] = {"none":[],"dub":[],"sub":[]}

				times = c.find_all("div", class_="times")[0]
				timesplit = str(times).split('<br>')

				times1 = BeautifulSoup(timesplit[0],'html.parser')
				if textos.lang[lang][1] in times1.get_text():
					opt = "sub"
				elif textos.lang[lang][0] in times1.get_text():
					opt = "dub"
				else:
					opt = 'none'
				for time in times1.find_all("span", style='color:#666'):
					child["times"][opt].append(time.get_text().replace('\xa0','').strip())
				for time in times1.find_all("span", style='color:'):
					child["times"][opt].append('*'+time.get_text().replace('\xa0','').strip()+'*')

				if len(timesplit) > 1:
					times2 = BeautifulSoup(timesplit[1],'html.parser')
					if textos.lang[lang][1] in times2.get_text():
						opt = "sub"
					elif textos.lang[lang][0] in times2.get_text():
						opt = "dub"
					else:
						opt = 'none'
					for time in times2.find_all("span", style='color:#666'):
						child["times"][opt].append(time.get_text().replace('\xa0','').strip())
					for time in times2.find_all("span", style='color:'):
						child["times"][opt].append('*'+time.get_text().replace('\xa0','').strip()+'*')
				parent["children"].append(child)
			response.append(parent)
	return response


def cineminha(info):
	response = []

	if len(info)==0:
		response.append(textos.no_results[lang])

	else:
		for i in info:
			if len(i["children"]) > 0:
				if i["type"] == 'theater':
					txt = Emoji.MOVIE_CAMERA
				elif i["type"] == 'movie':
					txt = Emoji.CLAPPER_BOARD
				txt += ' *'+i["name"]+'*'
				txt += '\n' + i["info"]

				for child in i["children"]:
					txt += '\n\n• '+child["name"]
					if child["type"] == "movie":
						txt += '\n'+child["info"]
					if len(child["times"]["none"]) > 0:
						txt += '\n'
						for time in child["times"]["none"]:
							txt += time + '  '
					if len(child["times"]["dub"]) > 0:
						txt += '\n'+textos.lang[lang][0]+':'
						for time in child["times"]["dub"]:
							txt += time + '  '
					if len(child["times"]["sub"]) > 0:
						txt += '\n'+textos.lang[lang][1]+':'
						for time in child["times"]["sub"]:
							txt += time + '  '
				response.append(txt)
	return response


def inline(loc, query, lang):
	results = []
	info = serialize(loc, q=query, sort=1)[1:]
	if len(info)==0:
		title = 
textos.no_results[lang].split('\n')[0].replace('*','')
		desc = textos.no_results[lang].split('\n')[1]
		msg = 
InputTextMessageContent(textos.no_results[lang],parse_mode="Markdown")
		results.append(InlineQueryResultArticle(0,title,msg,description=desc))
	else:
		for i in info:
			title = i["name"]
			desc = i["info"]
			msgtext = cineminha([i])[0]
			message = InputTextMessageContent(msgtext, parse_mode="Markdown")
			results.append(InlineQueryResultArticle(str(len(results)), title, message, description=desc))
	return results
