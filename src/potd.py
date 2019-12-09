# Picture of the day
#
# Description:
#   downloads and sorts picture of the day from websites.
#
# Version:
#   v1.7
#   .1 try: downloading; except: print(failed)
#   .6 Guardian UK/Int:  Separated Guardian UK and Int
#   .7 Logger:  implemented a console log file
#   .7 config:  implemented a config yaml file
# Issues:
#   is assuming .jpg good enough?
#   is it possible to add a pyinstaller publisher
# Feature Creep:
#   installer creates shell:startup and sets desktop-wallpaper


import requests
from bs4 import BeautifulSoup
import time
import os
import yaml

class Logger:
	def __init__(self, log:bool, filename:str, newline:str):
		self.log = log
		self.filename = filename
		if self.log:
			print(f'\n\n{newline}', file=open(self.filename,'a'))
	def print(self, x):
		print(x)
		if self.log:
			print(f'\t{x}', file=open(self.filename,'a'))


def config(filename:str='config'):
	'''
	Configuration dictionary loader,
	loads yaml config file,
	safely update config dictionary from defaults
	dumps safe config dict to yaml
	'''
	data = {
		'ids': {
			'bing': True,
			'guardian_uk': True,
			'guardian_int': True,
			'nasa': True,
			'ng': True,
			'smith': True,
			'wiki': True,
			},
		'log': True,
		'save': True,
		}
	if os.path.isfile(filename):
		data_loaded = yaml.load(open(filename, 'r'))
		data = dictUpdateExclusive(data, data_loaded)
	yaml.dump(data, open(filename, 'w'), default_flow_style=False)
	return data

def dictUpdateExclusive(d0:dict, d1:dict):
	'''
	A safe dictionary updator,
	for only keys that are in the old dict
	and ensuring the same value type
	'''
	d2 = d0
	for k0 in d0.keys():
		if k0 in d1.keys():
			v0, v1 = d0[k0], d1[k0]
			if type(v0) == type(v1):
				if isinstance(d0[k0], dict):
					d2[k0] = dictUpdateExclusive(v0, v1)
				else:
					d2[k0] = v1
	return d2


def download(url, path):
	r = requests.get(url)
	assert(r.status_code is 200)
	with open(path, 'wb') as f:
		[f.write(chunk) for chunk in r]

def get_url(id):
	if id == 'bing':
		name = 'Guardian International'
		url = 'http://www.theguardian.com/international'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		url = soup.find('div', {'data-id':'uk-alpha/special-other/special-story'}).find('a', {'class':'js-headline-text'})['href']
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.select('div.u-responsive-ratio')[0].find_all('source')[0]['srcset'].rsplit(',')[-1].strip().split(' ')[0]
		assert(img_url is not None)


		exit()

		name = 'Bing'
		url = 'http://www.bing.com'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.findAll('link')['']

		# img_url = url+r.text.rsplit('g_img={url:',1)[1].split('};',1)[0].split('\\',1)[0].replace('"','').replace("'",'').replace(' ','')
		assert(img_url is not None)
		print(img_url)
		exit()
	elif id == 'guardian_uk':
		name = 'Guardian UK'
		url = 'https://www.theguardian.com/news/series/ten-best-photographs-of-the-day/rss'
		r = requests.get(url)
		assert(r.status_code is 200)
		url = r.text.split('guid')[1].split('>')[1].split('<')[0]
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.select('div.immersive-main-media.immersive-main-media__gallery')[0].find_all('source')[0]['srcset'].rsplit(',')[-1].strip().split(' ')[0]
		assert(img_url is not None)
	elif id == 'guardian_int':
		name = 'Guardian International'
		url = 'http://www.theguardian.com/international'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		url = soup.find('div', {'data-id':'uk-alpha/special-other/special-story'}).find('a', {'class':'js-headline-text'})['href']
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.select('div.u-responsive-ratio')[0].find_all('source')[0]['srcset'].rsplit(',')[-1].strip().split(' ')[0]
		assert(img_url is not None)
	elif id == 'nasa':
		name = 'NASA'
		url = 'http://apod.nasa.gov/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = url+soup.find('img')['src']
	elif id == 'ng':
		name = 'National Geographic'
		url = 'http://www.nationalgeographic.com/photography/photo-of-the-day/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.find('meta',{'property':'og:image'})['content']
		assert(img_url is not None)
	elif id == 'smith':
		name = 'Smithsonian'
		url = 'https://www.smithsonianmag.com/photocontest/photo-of-the-day/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = 'https://'+soup.find('div',class_='photo-contest-detail-image').find('img')['src'].rsplit('https://',1)[1]
		assert(img_url is not None)
	elif id == 'wiki':
		name = 'WikiMedia'
		url = 'https://commons.wikimedia.org/wiki/Main_Page'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.find('img')['src'].replace('thumb/','').rsplit('/',1)[0]
		assert(img_url is not None)
	else:
		name = f'WarningWebID:  {id} not recognised.'
		img_url = None
	return name, img_url

def sort(id, img1, listdir_id, today, hist, save):
	for img2 in listdir_id:
		if os.path.isfile(today+img1) and os.path.isfile(today+img2):
			if save and not open(today+img1,'rb').read()==open(today+img2,'rb').read():
				os.rename(today+img2, hist+img2)
			else:
				os.remove(today+img2)


def main(ids:dict, log:bool, save:bool):
	date = time.strftime('%Y-%m-%d ', time.gmtime())
	log = Logger(log, 'log', f'POTD: {date}')
	path = os.getcwd().replace('\\','/')
	today = path + '/today/'
	if not os.path.isdir(today):
		os.mkdir(today)
	hist = path + '/history/'
	if not os.path.isdir(hist):
		os.mkdir(hist)
	listdir = os.listdir(today)
	for id, v in ids.items():
		if v:
			listdir_id = list(filter(lambda el: id in el, listdir))
			img_name = date+id+'.jpg'
			path = today + img_name
			if img_name not in listdir_id:
				name, url = get_url(id)
				log.print(name)
				download(url, path)
				log.print(f'\tdownloading: {url}')
				log.print(f'\t       into: {path}')
				log.print(f'\t    sorting: {listdir_id}')
				sort(id, img_name, listdir_id, today, hist, save)




if __name__ == '__main__':
	main(**config())
