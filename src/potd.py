# Picture of the day
#
# Description:
#   downloads and sorts picture of the day from websites.
#
# Version:
#   v1.9
#   .1 try: downloading; except: print(failed)
#   .6 Guardian UK/Int:  Separated Guardian UK and Int
#   .7 Logger:  implemented a console log file
#   .7 config:  implemented a config yaml file
#   .8 is==:  Due to py3.9 assert 'is'->'=='
#   .9 used xpaths
# Issues:
#   is assuming .jpg good enough?
#   is it possible to add a pyinstaller publisher
__version__ = '1.9'
import requests
from lxml import etree
from datetime import datetime
import os
import yaml

class Logger:
	def __init__(self, log:bool, filename:str, newline:str):
		self.log = log
		self.filename = filename
		if self.log:
			print(f'\n\n{newline}', file=open(self.filename,'a'))
	def printr(self, x):
		print(x)
		if self.log:
			print(f'\t{x}', file=open(self.filename,'a'))


def dict_update_exclusive(d0:dict, d1:dict, nested:bool=True):
	'''
	A safe dictionary updater,
	Updates only keys that are in the original dict
	Ensuring the same data type
	And repeats for nested dictionaries, controllable with 'nested' parameter.
	'''
	d2 = d0.copy()
	for k in d0.keys():
		if k in d1.keys() and type(d0[k]) == type(d1[k]):
			if nested and isinstance(d0[k], dict):
				d2[k] = dict_update_exclusive(d0[k], d1[k])
			else:
				d2[k] = d1[k]
	return d2

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
			'smithsonian_drone_aerial': True,
			'smithsonian_artistic': True,
			'smithsonian_people': True,
			'smithsonian_travel': True,
			'smithsonian_natural_world': True,
			'wiki': True,
			},
		'log': True,
		'save': True,
		}
	if os.path.isfile(filename):
		data_loaded = yaml.load(open(filename, 'r'), Loader=yaml.SafeLoader)
		data = dict_update_exclusive(data, data_loaded)
	yaml.dump(data, open(filename, 'w'), default_flow_style=False)
	return data


def get_url_xpath(url, xpath):
    return etree.HTML(requests.get(url).content).xpath(xpath)[0]

def get_smith(id):
    url = 'https://photocontest.smithsonianmag.com'
    cat = '/photocontest/categories/{}/'.format(id.replace('smithsonian_', '').replace('_', '-'))
    xpath1 = '/html/body/div[2]/div[3]/div/div[1]/a'
    url2 = url + get_url_xpath(url+cat, xpath1).get('href')
    xpath2 = '/html/body/div[2]/div[2]/div[1]/img'
    return 'https://' + get_url_xpath(url2, xpath2).get('src').split('/https://')[1]

def download(url, path):
	r = requests.get(url, headers={'User-Agent': 'CoolBot/0.0'})
	assert(r.status_code == 200)
	with open(path, 'wb') as f:
		[f.write(chunk) for chunk in r]

def get_url(id):
	if id == 'bing':
		name = 'Bing'
		url = 'http://www.bing.com'
		xpath = '/html/head/link[2]'
		img_url = url + get_url_xpath(url, xpath).get('href').split('.webp&qlt=')[0] + '.jpg'
	elif id == 'guardian_uk':
		name = 'Guardian UK'
		url = 'https://www.theguardian.com/news/series/ten-best-photographs-of-the-day/'
		xpath = '/html/body/div[3]/div/section[1]/div/div/div/ul/li/div/div/div[1]/div/picture/source[1]'
		img_url = get_url_xpath(url, xpath).get('srcset').split(' ')[0]
	elif id == 'guardian_int':
		name = 'Guardian International'
		url = 'https://www.theguardian.com/international'
		xpath = '/html/body/div[3]/div/section[2]/div/div/div[1]/ul/li[1]/div/div/div[1]/div/picture/source[1]'
		img_url = get_url_xpath(url, xpath).get('srcset').split(' ')[0]
	elif id == 'nasa':
		name = 'NASA'
		url = 'https://apod.nasa.gov/'
		xpath = '/html/body/center[1]/p[2]/a/img'
		img_url = url + get_url_xpath(url, xpath).get('src')
	elif id == 'ng':
		name = 'National Geographic'
		url = 'http://www.nationalgeographic.com/photography/photo-of-the-day/'
		xpath = '/html/body/div[1]/div/div[last()]/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div[1]/div[1]/aside/div/div[1]/div/div/div/div[1]/div/div/div/div/img'
		img_url = get_url_xpath(url, xpath).get('src')
	elif id == 'smithsonian_drone_aerial':
		name = 'Smithsonian Drone/Aerial'
		img_url = get_smith(id)
	elif id == 'smithsonian_artistic':
		name = 'Smithsonian Artistic'
		img_url = get_smith(id)
	elif id == 'smithsonian_people':
		name = 'Smithsonian People'
		img_url = get_smith(id)
	elif id == 'smithsonian_travel':
		name = 'Smithsonian Travel'
		img_url = get_smith(id)
	elif id == 'smithsonian_natural_world':
		name = 'Smithsonian Natural World'
		img_url = get_smith(id)
	elif id == 'wiki':
		name = 'Wikipedia'
		url = 'https://commons.wikimedia.org/'
		xpath = '/html/body/div[3]/div[3]/div[5]/div[1]/div/table[2]/tbody/tr/td[1]/div[1]/div[2]/div[1]/div[1]/a/img'
		img_url = get_url_xpath(url, xpath).get('src').replace('/thumb/', '/').split('.jpg/')[0] + '.jpg'
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
	date = datetime.today().strftime('%Y-%m-%d ')
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
				try:
					name, url = get_url(id)
					log.printr(name)
					download(url, path)
				except:
					pass
				else:
					log.printr(f'\tdownloading: {url}')
					log.printr(f'\t       into: {path}')
					log.printr(f'\t    sorting: {listdir_id}')
					sort(id, img_name, listdir_id, today, hist, save)




if __name__ == '__main__':
	main(**config())
