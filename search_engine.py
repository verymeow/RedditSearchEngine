import requests
from bs4 import BeautifulSoup

def get_URL(url):
	r = requests.get(url)
	if r.status_code != 200:
		raise Exception("Non-okay status code. {}".format(r.status_code))
	return r.text

def textParse(html):
	bs = BeautifulSoup(html)
	return bs.select('div.usertext-body')[1].text
	
