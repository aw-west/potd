# Picture of the day
#
# Description:
#   potd but windows, downloads and sorts.
#
# Version:
#   v1.0
# Issues:
#   pyinstaller set publisher
#   is .jpg good enough
#   installer creates shell:startup and sets desktop-wallpaper

import requests
from bs4 import BeautifulSoup
import time
import os
import ctypes

def download(url, path):
	print(f'\tdownloading: {url}\n\t\tinto: {path}')
	r = requests.get(url)
	assert(r.status_code is 200)
	with open(path, 'wb') as f:
		[f.write(chunk) for chunk in r]
	return None

def get_url(id):
	if id == 'bing':
		print('Bing')
		url = 'http://www.bing.com'
		r = requests.get(url)
		assert(r.status_code is 200)
		img_url = url+r.text.rsplit('g_img={url:',1)[1].split('};',1)[0].split('\\',1)[0].replace('"','').replace("'",'').replace(' ','')
		assert(img_url is not None)
	elif id == 'guardian':
		print('Guardian')
		url = 'http://www.theguardian.com/international'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		url = soup.find("div", {"data-id":"uk-alpha/special-other/special-story"}).find("a", {"class":"js-headline-text"})['href']
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = soup.select("div.u-responsive-ratio")[0].find_all("source")[0]['srcset'].rsplit(',')[-1].strip().split(' ')[0]
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
		img_url = soup.find('meta',{'property':'og:image'})['content']
		assert(img_url is not None)
	elif id == 'smith':
		print('Smithsonian')
		url = 'https://www.smithsonianmag.com/photocontest/photo-of-the-day/'
		r = requests.get(url)
		assert(r.status_code is 200)
		soup = BeautifulSoup(r.content, 'lxml')
		img_url = 'https://'+soup.find('div',class_='photo-contest-detail-image').find("img")['src'].rsplit('https://',1)[1]
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

def sorting(id, img1, listdir_id, today, hist, save):
	print(f'\tsorting: {listdir_id}')
	for img2 in listdir_id:
		if os.path.isfile(today+img1) and os.path.isfile(today+img2):
			if save and not open(today+img1,'rb').read()==open(today+img2,'rb').read():
				os.rename(today+img2, hist+img2)
			else:
				os.remove(today+img2)
	return None

def set_wallpaper(path):
	# Windows Only
	ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
	return None

def main(ids, save):
	path = os.getcwd().replace('\\','/')
	today, hist = path+'/today/', path+'/history/'
	if not os.path.isdir(today): os.mkdir(today)
	if not os.path.isdir(hist): os.mkdir(hist)
	date = time.strftime('%Y-%m-%d ', time.gmtime())

	listdir = os.listdir(today)
	for id in ids:
		listdir_id = list(filter(lambda el: id in el, listdir))
		img_name = date+id+'.jpg'
		if img_name not in listdir_id:
			img_url = get_url(id)
			download(img_url, today+img_name)
			sorting(id, img_name, listdir_id, today, hist, save)
	set_wallpaper(today)
	return None

if __name__ == '__main__':
	ids = [
		'bing',
		'guardian',
		'nasa',
		'ng',
		'smith',
		'wiki'
		]
	main(ids, save=True)
