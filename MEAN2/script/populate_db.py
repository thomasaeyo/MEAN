import pycrunchbase
from alchemyapi import AlchemyAPI
import csv
import pickle
from pymongo import MongoClient

alchemyapi = AlchemyAPI()
API_KEY = [
	"9abd8b0e3660d0af36170779e95abdba",
	"2cc5308e35927f10d8401fc6d1c38b43",
	# "d4575a0b5179e993ef03d688b50b1c9f",
	# "8fa2532bb5d27713be8189371de45074"
	]
cb = pycrunchbase.CrunchBase(API_KEY[0])

def parse_csv():
	people_list = [] # first_name, last_name, crunchbase_url, img_url, facebook_url, twitter_url, linkedin_url
	with open('/../data/cb_custom_export/people.csv') as f:
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
	pickle.dump(people_list, open('/../data/pickle/people_list_dump.txt','wb'))

def populate_db():
	N = 1000
	db = MongoClient().personafi.people
	filename = "/Users/thomasaeyo/Desktop/Thomas/data/pickle/people_list_dump.txt"
	people_list = pickle.load(open(filename,'rb'))[1:N]
	for idx,person in enumerate(people_list):
		db_input = {}
		db_input['first_name'] = person['first_name']
		db_input['last_name'] = person['last_name']
		db_input['img_url'] = person['img_url']
		db_input['facebook_url'] = person['facebook_url']
		db_input['twitter_url'] = person['twitter_url']
		db_input['linkedin_url'] = person['linkedin_url']
		db_input['jobs'] = []
		db_input['educations'] = []
		db_input['news'] = []
		db_input['experiences'] = []
		db_input['keywords'] = []

		# get permalink from crunchbase url
		permalink = person['crunchbase_url'].split('?')[0].split('/')[4]
		try:
			cb_person = cb.person(permalink)

			# jobs
			primary_affiliation = cb_person.primary_affiliation
			if(type(primary_affiliation) != pycrunchbase.resource.relationship.NoneRelationship):
				for affiliation in primary_affiliation:
					db_input['jobs'].append({
						'organization':affiliation.organization_name,
						'title':affiliation.title
						})
			# educations
			degrees = cb_person.degrees
			if(type(degrees) != pycrunchbase.resource.relationship.NoneRelationship):
				for degree in degrees:
					db_input['educations'].append({
						'school': degree.organization_name,
						'major': degree.degree_subject,
						'degree_type': degree.degree_type_name,
						'graduation_year': degree.completed_on
						})
			# news
			news = cb_person.news
			if(type(news) != pycrunchbase.resource.relationship.NoneRelationship):
				for a_news in news:
					db_input['news'].append({
						'title': a_news.title,
						'author': a_news.author,
						'url': a_news.url,
						})
			# experience
			experiences = cb_person.experience
			if(type(experiences) != pycrunchbase.resource.relationship.NoneRelationship):
				for experience in experiences:
					db_input['experiences'].append({
						'title': experience.title,
						'organization': experience.organization_name
						})
			# location
			location = cb_person.primary_location
			if(type(location) != pycrunchbase.resource.relationship.NoneRelationship):
				db_input['location'] = str(location[0])

			# keywords
			try:
				alchemy_keywords = alchemyapi.keywords('text',cb_person.bio)
				for keyword in alchemy_keywords['keywords']:
					db_input['keywords'].append({
						'keyword': keyword['text'].replace('.','(dot)').lower(), 
						'relevance': keyword['relevance']
						})
			except Exception,e:
				print "Error in keywords"
				print alchemy_keywords
				print repr(e)
				pass

		except Exception,e:
			print "Error in CB API"
			print repr(e)
			pass

		print idx

		# Write to DB
		try:
			db.insert(db_input)
		except Exception,e:
			print "Error in DB insertion"
			print repr(e)
			pass

populate_db()