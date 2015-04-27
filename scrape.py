import pycrunchbase
import pickle
from pymongo import MongoClient

API_KEY = ["2cc5308e35927f10d8401fc6d1c38b43",
			"d4575a0b5179e993ef03d688b50b1c9f",
			"9abd8b0e3660d0af36170779e95abdba",
			"8fa2532bb5d27713be8189371de45074"]
cb = pycrunchbase.CrunchBase(API_KEY[0])
db = MongoClient().personafi.people


N = 100
filename = "/Users/thomasaeyo/Desktop/MEAN/data/people_list_dump.txt"
people_list = pickle.load(open(filename,'rb'))[1:N+1]

try:
	for idx,person in enumerate(people_list):
		if idx < 65:
			continue
		permalink = person['first_name'] + " " + person['last_name']
		permalink = permalink.replace(" ", "-")
		print permalink
		p = cb.person(permalink)
		try:
			primary_affiliation = p.primary_affiliation[0]
			db.update(
				{'first_name':person['first_name'],'last_name':person['last_name']},
				{'$set': {'primary_role':primary_affiliation.title, 'primary_organization':primary_affiliation.organization_name}}
				)
			print idx
		except IndexError:
			print "%d IndexError" % idx
except Exception,e:
	print repr(e)
	pass
