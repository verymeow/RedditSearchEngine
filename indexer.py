from util import *
import argparse
import base64
import os
import json

#Indexer assumes that the entire collection fits in the memory.
class indexer(object):
	def __init__(self):
		self.inverted_index = dict()
		self.forward_index = dict() 
		self.url_to_id = dict()
		self.doc_count = 0

	#assuming add_doc() never called twice for a doc and all
	#have unique URL. Parsed text is list of words.
	def add_doc(self, url, parsed_text):
		self.doc_count += 1
		assert url not in self.url_to_id
		current_id = self.doc_count
		self.forward_index[current_id] = parsed_text
		for position, word in enumerate(parsed_text):
			if word not in self.inverted_index:
				self.inverted_index[word] = []
			self.inverted_index[word].append((position, current_id))

	def store_on_disk(self,index_dir):
		inverted_index_file_name = os.path.join(index_dir, "inverted_index")
		forward_index_file_name = os.path.join(index_dir, "forward_index")
		url_to_id_file_name = os.path.join(index_dir, "url_to_id")
		
		inverted_index_file = open(inverted_index_file_name, "w")
		forward_index_file = open(forward_index_file_name, "w")
		url_to_id_file = open(url_to_id_file_name, "w") 
		json.dump(self.inverted_index, inverted_index_file, indent=4)
		json.dump(self.forward_index, forward_index_file, indent=4)
		json.dump(self.url_to_id, url_to_id_file, indent=4)

def create_index_from_dir(stored_docs_dir, index_dir):
	idxr = indexer()
	for filename in os.listdir(stored_docs_dir):
		opened_file = open(os.path.join(stored_docs_dir, filename))
		parsed_doc = parseRedditPost(opened_file.read()).split(" ") 
		idxr.add_doc(base64.b16decode(filename), parsed_doc)
	idxr.store_on_disk(index_dir)

def main():
	parser = argparse.ArgumentParser(description='Indexes the learnprogramming subreddit.')
	parser.add_argument("--stored_docs_dir", dest = "stored_docs_dir")
	parser.add_argument("--index_dir", dest ="index_dir")
	args = parser.parse_args()
	create_index_from_dir(args.stored_docs_dir, args.index_dir)

if __name__ == "__main__": #checks if invocation from command line
	main()
