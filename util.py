import re
import requests
from bs4 import BeautifulSoup

#Default reddit URLs look like this.
_reddit_url = re.compile(r'http(s)?://(www.)?reddit.com/r/learnprogramming')

def getURL(url):
	
	assert _reddit_url.match(url)
	headers = {'User-Agent': 'Tarunz Reddit Search bot version 1.0'}
	r = requests.get(url, headers = headers)
	if r.status_code != 200:
		raise Exception("Non-okay status code. {}".format(r.status_code))
	return r.text

def parseRedditPost(html):
	bs = BeautifulSoup(html)
	return bs.select('div.usertext-body')[1].text

