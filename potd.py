# Picture of the day
#
# Description:
#   potd but downloading and sorting only.
#
# Version:
#   v1.0
# Issues:
#   pyinstaller set publisher
#   .jpg is good enough
#   installer creates shell:startup and sets desktop-wallpaper

import requests
from bs4 import BeautifulSoup
import time
import os

def download(url, path):
	print('    downloading: ' + url + "\n           into: " + path)
	r = requests.get(url)
	assert(r.status_code is 200)
	with open(path, 'wb') as f:
		[f.write(chunk) for chunk in r]
	return

def geturl(id):
	if id == 'bing':
		print('Bing')
		url = 'http://www.bing.com'
		r = requests.get(url)
		assert(r.status_code is 200)
		img_url = url+r.text.rsplit('g_img={url:',1)[1].split('};', 1)[0].split('\\',1)[0].replace('"','').replace("'",'').replace(' ','')
		assert(img_url is not None)
	elif id == 'guardian':
		print('Guardian')
		url = 'http://www.theguardian.com/international'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		url = soup.find("div", {"data-id":"uk-alpha/special-other/special-story"}).find("a", {"class":"js-headline-text"})['href']
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'lxml')
		assert(r.status_code is 200)
		img_url = soup.select("div.immersive-main-media.immersive-main-media__gallery")[0].find_all("source")[0]['srcset'].rsplit(',')[1].strip().split(' ')[0]
		assert(img_url is not None)
	elif id == 'nasa':
		print('NASA')
		url = 'http://apod.nasa.gov/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = url+soup.find('img')['src']
	elif id == 'ng':
		print('National Geographic')
		url = 'http://www.nationalgeographic.com/photography/photo-of-the-day/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.find('meta', {'property':'og:image'})['content']
		assert(img_url is not None)
	elif id == 'smith':
		print('Smithsonian')
		url = 'https://www.smithsonianmag.com/photocontest/photo-of-the-day/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = 'https://'+soup.find('div', class_='photo-contest-detail-image').find("img")['src'].rsplit('https://', 1)[1]
		assert(img_url is not None)
	elif id == 'wiki':
		print('WikiMedia')
		url = 'https://commons.wikimedia.org/wiki/Main_Page'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.find('img')['src'].replace('thumb/','').rsplit('/',1)[0]
		assert(img_url is not None)
	else:
		print(f'WarningWebID:  {id} not recognised.')
	return img_url

def oldimg(id, listdir, path, today, hist, save):
	print('    old image sorting')
	for el in listdir:
		if id in el:
			if save and not os.path.isfile(path+hist+el):
				os.rename(path+today+el, path+hist+el)
			else:
				os.remove(path+today+el)
			listdir.remove(el)
	return listdir

def setslideshow(path, today):
	shell = r'''
	ctypes.windll.uder32.SystemParametersInfoW(20, 0, path+today, 0)
	'''
	return

def main(ids, save):
	path = os.getcwd().replace('\\','/')
	today = '/today/'
	if not os.path.isdir(path+today): os.mkdir(path+today)
	hist = '/history/'
	if not os.path.isdir(path+hist): os.mkdir(path+hist)
	date = time.strftime('%Y-%m-%d ', time.gmtime())
	listdir = os.listdir(path+today)
	for id in ids:
		img_name = date+id+'.jpg'
		if img_name not in listdir:
			img_url = geturl(id)
			download(img_url, path+today+img_name)
			oldimg(id, listdir, path, today, hist, save)
	return

if __name__ == '__main__':
	# ids = ['bing', 'guardian', 'nasa', 'ng', 'smith', 'wiki']
	ids = ['bing', 'ng', 'smith', 'wiki']
	main(ids, save=True)
