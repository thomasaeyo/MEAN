from alchemyapi import AlchemyAPI
import csv
import pickle
from pymongo import MongoClient

alchemyapi = AlchemyAPI()

def parse_csv():
	people_list = [] # first_name, last_name, crunchbase_url, img_url, facebook_url, twitter_url, linkedin_url
	with open('data/cb_custom_export/people.csv') as f:
		reader = csv.reader(f)
		for line in reader:
			person = {}
			person['first_name'] = line[2]
			person['last_name'] = line[4]
			person['crunchbase_url'] = line[6]
			person['img_url'] = line[7]
			person['facebook_url'] = line[8]
			person['twitter_url'] = line[9]
			person['linkedin_url'] = line[10]
			people_list.append(person)
	pickle.dump(people_list, open('data/people_list_dump.txt','wb'))

def create_db_input():
	db_input_list = []
	people_list = pickle.load(open('data/people_list_dump.txt','rb'))[1:]

	N = 100
	people_list = people_list[:N]
	try:
		for idx,person in enumerate(people_list):
			db_input = {}
			db_input['first_name'] = person['first_name']
			db_input['last_name'] = person['last_name']
			db_input['img_url'] = person['img_url']
			db_input['facebook_url'] = person['facebook_url']
			db_input['twitter_url'] = person['twitter_url']
			db_input['linkedin_url'] = person['linkedin_url']
			alchemy_keywords = alchemyapi.keywords('url',person['crunchbase_url'])['keywords']
			db_input['keywords'] = {keyword['text'].lower():keyword['relevance'] for keyword in alchemy_keywords}
			db_input_list.append(db_input)
			print idx
	except Exception,e:
		print repr(e)
		pass
	pickle.dump(db_input_list, open('data/100_ppl_dump.txt','wb'))

def preprocess():
	db_input_list = pickle.load(open('data/100_ppl_dump.txt','rb'))
	for x in xrange(len(db_input_list)):
		for keyword in db_input_list[x]['keywords']:
			if '.' in keyword:
				db_input_list[x]['keywords'][keyword.replace('.','-')] = db_input_list[x]['keywords'][keyword]
				del db_input_list[x]['keywords'][keyword]
	return db_input_list

def insert_to_DB():
	db = MongoClient().personafi.people
	db_input_list = preprocess()
	for db_input in db_input_list:
		try:
			db.insert(db_input)
		except Exception,e:
			print e
			print db_input

create_db_input()
insert_to_DB()
