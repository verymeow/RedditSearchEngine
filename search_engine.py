import requests
from bs4 import BeautifulSoup
import time
import re
import os.path
import base64

class crawler(object):
	def __init__(self,   start_url, storage_dir):
		self.start_url = start_url
		self.storage_dir = storage_dir
	
	@staticmethod
	def _make_absolute_url(url):
		return 'http://reddit.com' + url

	def crawl(self):
		current_page_url = self.start_url
		while True:
			current_page = getURL(current_page_url)
			#print current_page_url
			soup = BeautifulSoup(current_page)
			all_links = soup.findAll('a' , attrs ={'class':'title'});
			post_links = [crawler._make_absolute_url(link['href']) for link in all_links]
			for post_link in post_links:
				html = getURL(post_link)
				stored_text_file_name = os.path.join(self.storage_dir, base64.b16encode(post_link))
				stored_text_file = open(stored_text_file_name, "w")
				stored_text_file.write(html.encode('utf8'))
				time.sleep(2)	
			next_page_url = soup.find('a', attrs = {'rel':'next'})['href']
			current_page_url = next_page_url
			time.sleep(2)


 
