#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Autor Andrei Bastos
#  You can contact me by email (andreibastos@outlook.com) or write to:
#  Via Labic/Ufes - Vitória/ES - Brazil

############### IMPORT's ###############
import json, datetime, time
from dateutil.parser import *

import threading, tweepy, socket, traceback, sys

import requests, urllib

#######################################


############### VARIÁVEIS GLOBAIS ###################

##### CONSTANTES #####
URL_API_DATABASE = 'https://inep-api-v2-dev.herokuapp.com/v2/tweets'
URL_API_CATEGORIZE = 'http://188.166.40.27:5001/twitter?'
PATH_KEYS = 'keys_exemplo.json';
PATH_QUERYS = 'querys.json';
NUM_PER_INSERT = 10;
DATE_FORMAT_TWITTER = "%a %b %d %H:%M:%S %z %Y";

##### VARIÁVEIS ######
log_system = ''
index_key = 0;
keys = []
querys = []
log_system = ''
active_collectors = []

#####################################################

######################### Classes  ###############################
class log_collector():
	logs = []	
	"""docstring for log_collector"""
	def __init__(self):	
		date = time.strftime("%Y%m%d_%H%M",time.gmtime());
		log = '\"date_created\";\"text\"\n'
		self.filename = 'log_' + date + '.log';		
		self.file = open(self.filename, 'a');
		self.file.write(log)

	def read_file(self, filename):		
		text = 'read file: {0}.'.format(filename);		
		self.new(text);

	def error(self, e):		
		text = 'error: {0}.'.format(str(e)) 
		self.new(text);		

	def insert_tweets(self, NUM_PER_INSERT):
		text = 'insert: {0} tweets.'.format(NUM_PER_INSERT);
		self.new(text);		

	def streaming_tweets(self, query):
		text = "streaming retweets for query '{0}'" .format(unicode(query))
		self.new(text);		

	def new(self, text):				
		log = "\"{0}\";\"{1}\"\n".format(str(string_time_now()),text)			
		self.write(log);

	def write(self, log):
		pass
		# self.file.write(log)

class Collector(threading.Thread):
	def __init__(self, query, languages, key, log=None):
		self.query = query        
		self.languages = languages
		self.key = key
		self.log = log
		self.auth = {}
		self.count = 0
		self.active = False
		self.connected = False
		self.stream = None
		self.list_temp_tweets_to_insert = []  
		super(Collector, self).__init__()


	def swap_key(self, key):
		self.key = key
		return "troquei"

	def swap_auth(self):
		self.stop()
		## pega as informações da chave de identificação
		consumer_key, consumer_secret, \
			access_token, access_token_secret = self.key

		## cria a autenticação 
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_token, access_token_secret)

		

	def main(self):
		global log_system

		self.swap_auth()

		## Adiciona no log
		log_system.streaming_tweets(self.query)
		print(self.query)
		
		log_system.streaming_tweets(unicode(self.query))
		listener = StreamingListener(self)

		#cria uma escuta 
		self.stream = tweepy.streaming.Stream(self.auth, listener, timeout=60.0)
		self.active = True
		
		self.stream.filter(track=self.query, languages=self.languages)

		#enqunto estiver ativo
		while (self.active):
			try:
				self.connected = True

			except socket.gaierror as sg:
				log_system.error(sg)   
				self.connected = False
				c = active_collectors.pop(int(job_id) - 1)
				c.stop()
				time.sleep(60)
			except Exception as e:
				print e
				log_system.error(e)   
				self.connected = False
				traceback.print_exc(file=sys.stdout)
				sys.stdout.flush()
				time.sleep(60)
				print("Collector stopped.")

		return 0

	def run(self):        
		self.main()

	def stop(self):				
		print "Stopping collector: " +  " ,".join(c for c in self.query)
		self.active = False	
		if 	self.stream is not None:
			self.stream.disconnect()		
		# print dir(self.stream)
		
class StreamingListener(tweepy.StreamListener):
	def __init__(self, collector, *args, **kwargs):
		self.collector = collector
		self.count = 0
		self.list_temp_tweets_to_insert = []
		super(StreamingListener, self).__init__(*args, **kwargs)

	def on_data(self, data):

		try:
			status = json.loads(data)		
           
			user = status['user']
			user = user['screen_name']
			text = ""
			try:
				text = str(unicode(status['text']).encode('utf-8')).replace("\n","")
			except Exception as e:
				text = status['text']				
			

			# print 'user:{0}\ttext:{1}'.format(user, text )
			
			categories = categoriza(status)		
			
			keywords = []
			reverse_geocode = []

			if categories:
				keywords = categories.get("keywords")			
				reverse_geocode = categories.get("reverse_geocode")


		except Exception as e:  
			log_system.error(e) 			
			print e					     
			return False

		twitter_obj = {}				
		twitter_obj['status'] = status
		twitter_obj['keywords'] = keywords
		twitter_obj['reverse_geocode'] = reverse_geocode


		# print(json.dumps(twitter_obj,indent=4))
		self.collector.count += 1

		self.collector.list_temp_tweets_to_insert.append(twitter_obj)        
        
		try:
			if((self.collector.count % NUM_PER_INSERT) == 0):             
				# twitter_collection.insert(self.collector.list_temp_tweets_to_insert)
				saveData(self.collector.list_temp_tweets_to_insert)
				print 'save in database [{0}]'.format(NUM_PER_INSERT)
				log_system.insert_tweets(NUM_PER_INSERT)
				self.collector.list_temp_tweets_to_insert = []			
		except Exception as e:
			log_system.error(e)
			return False

		super(StreamingListener, self).on_data(data)

	def on_error(self, status_code):
		print(status_code)
		if status_code == 401:
			raise Exception("Authentication error")
		if status_code == 420:
			self.collector.swap_key(get_key());
			print self.collector.swap_auth()
			self.collector.main()
			# raise Exception("Enhance Your Calm")
	def on_status(self, status):
		# print(status)
		pass

##################################################################

######################### Funções ################################
# chaves de idenficação
def read_keys():
	global log_system
	# ler arquivo	
	f = open(PATH_KEYS,'r')

	log_system.read_file(PATH_KEYS)
	return json.loads(f.read());	

def get_key():
	global keys
	global index_key;
	## troca a chave atual por outra.
	key = keys[index_key];
	index_key +=1
	return key

# querys 
def read_querys():
	global log_system
	f = open(PATH_QUERYS,'r')
	log_system.read_file(PATH_QUERYS)
	return json.loads(f.read());

# conversões de data
def string_time_now():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def string_to_date(date_string):	 
	return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_string,"%a %b %d %H:%M:%S +0000 %Y")), None)

def string_to_date(date_string,date_format):	 
	return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_string,date_format)), None)

def categoriza(status):
	
	
	text = str(unicode(status['text'].replace("\n", "")).encode('utf-8'))
	username = status['user']['screen_name']
	location = status['user']['location']
	place = status['place'] 
	if place:		
		place = place['full_name']
		place = str(unicode(place).encode('utf-8'))		
		print place

	else:
		place = ""

	if not location:
		location = ""
	else:
		location = str(unicode(location).encode('utf-8'))

	params = {'text':text, 'username':username, 'location':location, 'place':place}

	try:			
		r = requests.get(URL_API_CATEGORIZE, params=params)
		
		r.raise_for_status()
		categories = r.json()
		# print json.dumps(r.json(), indent=4)

		print '[user]:{0}\t[text]:{1}\t[categories]:{2}\t[location]:{3}\t[place]:{4}'.format(username, text, json.dumps(categories), location, place)
		return categories
	except Exception as e:
		print e
		return {}


def saveData(data):
	data=json.dumps(data)
	try:
		headers = {'user-agent': 'coletor-tweets', 'content-type': 'application/json'}		

		r = requests.post(URL_API_DATABASE, data=data, headers=headers)
		r.raise_for_status()
		
		return {'ok':1, 'msg':'gravado com sucesso'}			
	except requests.exceptions.HTTPError as e:
		print e


###################################################################

######################## Rotina Principal #########################
def main():
	global log_system, keys
	# cria o objeto de log do sistema
	log_system = log_collector();

	# ler as chaves
	keys = read_keys();
	key = get_key(); 

	#ler as querys
	querys = read_querys();
	
	index_query = 1;
	for query in querys:
		if index_query % 2 == 0:
			key = get_key(); 


		query['track'] = [str(unicode(x).encode('utf-8')).decode("utf-8") for x in query['track']]
		# print query['track'][0]
		c = Collector(query['track'], query['languages'], key)
				
		c.start()
		active_collectors.append(c)
		index_query =+ 1
	
	while True:
		try:
			raw_input('Ctrl+C stop program')
		except (KeyboardInterrupt, EOFError):
			print 'stopping program...'
			for c in active_collectors:
				c.stop();				
			print 'program stop.'			
			sys.exit()
		
		


if __name__ == '__main__':
	main()