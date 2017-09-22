import requests
from bs4 import BeautifulSoup
import time
import re
import os.path
import base64
import argparse
from util import *
import logging


class crawler(object):
	def __init__(self,   start_url, storage_dir):
		self.start_url = start_url
		self.storage_dir = storage_dir
	
	@staticmethod
	def _make_absolute_url(url):
		return 'http://reddit.com' + url

	def crawl(self):
		current_page_url = self.start_url
		ok_url_count = 0
		error_url_count = 0
		while True:
				#conued okay urls for checking	
				ok_url_count += 1
				current_page = getURL(current_page_url)
				#print current_page_url
				soup = BeautifulSoup(current_page)
				all_links = soup.findAll('a' , attrs ={'class':'title'});
				post_links = [crawler._make_absolute_url(link['href']) for link in all_links]
				try:
					for post_link in post_links:
						ok_url_count +=1
						html = getURL(post_link)
						stored_text_file_name = os.path.join(self.storage_dir, base64.b16encode(post_link))
						stored_text_file = open(stored_text_file_name, "w")
						stored_text_file.write(html.encode('utf8'))
						stored_text_file.close()
						time.sleep(2)	
				except Exception as e:
					error_url_count += 1
					logging.error(u"Error while crawling{}".format(current_page_url))
					logging.exception(e)
				next_page_url = soup.find('a', attrs = {'rel':'next'})['href']
				current_page_url = next_page_url
				time.sleep(2)
			

def main():
	parser = argparse.ArgumentParser(description='Crawl Reddit.')
	parser.add_argument("--start_url", dest = "start_url")
	parser.add_argument("--storage_dir", dest ="storage_dir")
	args = parser.parse_args()	
	cr = crawler(args.start_url, args.storage_dir)
	cr.crawl()

if __name__ == "__main__": #checks if invocation from command line
	main()
