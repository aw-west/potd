#!/usr/bin/python3
#potd: Download the Photo of the Day from various websites and set it as wallpaper of your desktop
#Copyright (C) 2017 Raffaele Mancuso

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
if sys.version_info[0] < 3:
    raise Exception("You must run the script with Python >= 3")
if sys.version_info[0] == 3 and sys.version_info[1] < 6:
    raise Exception("You must run the script with Python >= 3.6")

import requests
from bs4 import BeautifulSoup   
import ctypes
import os.path
import datetime
import json
import argparse
import subprocess
from enum import Enum, unique, auto
import sched
import time
import deskenv

# Set wallpaper on PLASMA 5 desktop
def setWallpaperPlasma5(image_file):
    import dbus
    jscript = """
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file://""" + image_file + """");
        }"""
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript)
    
# Set wallpaper on MAC OSX desktop (untested) (https://stackoverflow.com/questions/431205/how-can-i-programmatically-change-the-background-in-mac-os-x)
def setWallpaperWindows(image_file):
    from appscript import app, mactypes
    app('Finder').desktop_picture.set(mactypes.File(image_file))

# Set wallpaper on Windows desktop
def setWallpaperWindows(image_file):
    SPI_SETDESKWALLPAPER = 20 
    SPIF_UPDATEINIFILE = 1
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(image_file), SPIF_UPDATEINIFILE)

#Set wallpaper on GNOME 3 desktop
#/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///home/raffaele/Pictures/cat.jpeg
def setWallpaperGnome3(image_file):
    image_file = os.path.abspath(image_file)
    command = "/usr/bin/gsettings set org.gnome.desktop.background picture-uri file://" + image_file
    print("COMMAND: "+command)
    subprocess.run(command.split())


def downloadFile(url, output_filepath):
    print("Downloading "+url+" into "+output_filepath)
    r = requests.get(url)
    with open(output_filepath, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

# Get the link of the Smithsonian image of the day
def getSmithLink(out_file):    
    #Download web page
    print("Downloading Smithsonian webpage...")
    r = requests.get('https://www.smithsonianmag.com/photocontest/photo-of-the-day/'+str(datetime.datetime.now().date()))    
    if(r.status_code != 200):
        print("ERROR: no image of the day found for Smithsonian")
        return None
    #get binary response content
    soup = BeautifulSoup(r.content,"lxml")    
    div_item = soup.find("div",class_="photo-contest-detail-image")    
    assert(div_item is not None)
    img_tag = div_item.find("img") 
    assert(img_tag is not None)
    img_link = img_tag['src']
    #get the high resolution version
    img_link = 'https://' + img_link.split("https://")[2]
    downloadFile(img_link, out_file)
    return out_file
    
# Get the link of the WikiMedia image of the day
def getWikiMediaLink(out_file):    
    #Download web page
    print("Downloading WikiMedia webpage...")
    r = requests.get('https://commons.wikimedia.org/wiki/Main_Page')    
    if(r.status_code != 200):
        print("ERROR: status_code: "+r.status_code)
        sys.exit()    
    #get binary response content
    cont = r.content
    soup = BeautifulSoup(cont,"lxml")    
    img_item = soup.find("img")    
    if(img_item is None):
        print("ERROR: img_item not found")    
    img_link = img_item['src'].replace("thumb/","")    
    pos = img_link.rfind("/")
    img_link = img_link[0:pos]
    downloadFile(img_link, out_file)
    return out_file

#Get link of the National Geographics image of the day
def getNGLink(out_file):
    #Download web page
    print("Downloading NG webpage...")
    r = requests.get('http://www.nationalgeographic.com/photography/photo-of-the-day/')    
    if(r.status_code != 200):
        print("ERROR: status_code: "+r.status_code)
        sys.exit()    
    #get binary response content
    cont = r.content
    #print(cont)
    soup = BeautifulSoup(cont,"lxml")    
    s_url = soup.find("meta", {"property":"og:url"})
    s_desc = soup.find("meta", {"name":"description"})
    s_image = soup.find("meta", {"property":"og:image"})    
    if(s_image is None):
        print("ERROR: s_image not found")    
    img_link = s_image['content']
    downloadFile(img_link, out_file)
    return out_file

#Get link of the Bing image of the day
def getBingLink(out_file):
    #Download web page
    print("Downloading Bing webpage...")
    r = requests.get('http://www.bing.com')    
    if(r.status_code != 200):
        print("ERROR: status_code: "+r.status_code)
        sys.exit()    
    #get text
    cont = r.text
    to_find = "g_img={url:"
    pos = cont.find(to_find)
    pos2 = cont.find(",",pos)
    link = cont[pos+len(to_find)+1:pos2].replace('"','').replace("'","")
    img_link = "http://www.bing.com"+link
    downloadFile(img_link, out_file)
    return out_file
    
#Get link of the Guardian image of the day
def getGuardianLink(out_file):
    #Download web page
    print("Downloading Guardian webpage...")
    r = requests.get('http://www.theguardian.com/international')    
    if(r.status_code != 200):
        print("ERROR: status_code is not 200, but instead it's "+str(r.status_code))
        sys.exit()    
    #get binary response content
    soup = BeautifulSoup(r.content,"lxml")    
    div_img = soup.find("div", {"data-id":"uk-alpha/special-other/special-story"})
    assert(div_img is not None)
    
    # using the _class argument, it search for exactly that class combination. Instead using the dictionary, it searches for the elements that contain that class (and possibly other classes too)
    potd_link_a = div_img.find("a", {"class":"js-headline-text"})
    assert(potd_link_a is not None)
    potd_link = potd_link_a['href']
    print("Link: {}".format(potd_link))
    
    #going to the page of the image of the day
    r = requests.get(potd_link)    
    if(r.status_code != 200):
        print("ERROR: status_code is not 200, but instead it's "+str(r.status_code))
        sys.exit()    
        
    #get binary response content
    soup_potd = BeautifulSoup(r.content,"lxml")   
    
    img_el = soup_potd.select("div.immersive-main-media.immersive-main-media__gallery") #select() returns a list
    assert(isinstance(img_el, list))
    assert(len(img_el) == 1)
    
    #img_src = img_el[0].find("source", {"sizes":"135.62646370023418vh"})
    img_list = img_el[0].find_all("source")
    assert(img_list is not None)
        
    img_src = img_list[0]
    assert(img_src is not None)
    
    links = img_src['srcset'] #returns a string
    highest_res_link = links.split(",")[-1].strip().split(" ")[0]
    print(highest_res_link)    
    
    downloadFile(highest_res_link, out_file)
    return out_file
    
#Get link of the NASA image of the day
def getNASALink(out_file):
    #Download web page
    print("Downloading NASA webpage...")
    base_url = 'http://apod.nasa.gov'
    r = requests.get(base_url)    
    if(r.status_code != 200):
        print("ERROR: status_code is not 200, but instead it's "+str(r.status_code))
        sys.exit()    
    #get binary response content
    soup = BeautifulSoup(r.content,"lxml")    
    div_img = soup.find("img")
    highest_res_link = base_url + "/" + div_img['src']
    downloadFile(highest_res_link, out_file)
    return out_file

#Get link of the Bing image for tomorrow
"""
def getBingPreLink(out_file):
    #Download web page
    print("Downloading Bing Preview webpage...")
    r = requests.get('http://www.bing.com')    
    if(r.status_code != 200):
        print("ERROR: status_code: "+r.status_code)
        sys.exit()    
    #get binary response content as text
    cont = r.text
    to_find = "g_prefetch = {'Im': {url:"
    pos = cont.find(to_find)
    if(pos==-1):
        print("Error: string \"{}\" not found".format(to_find))
        exit()
    pos2 = cont.find(",",pos)
    print("pos={}, pos2={}".format(pos,pos2))
    link = cont[pos+len(to_find)+1:pos2].replace('"','').replace("'","").replace("\\/","/")
    img_link = "http://www.bing.com"+link
    downloadFile(img_link, out_file)
"""

def saveMetadata(img_path, site, json_path):
    #Save metadata
    metadata = {'date':str(datetime.datetime.now()), 'source':img_path, 'site':site}
    with open(json_path,"w",encoding="utf-8") as fileh:
        fileh.write(json.dumps(metadata))

def getMetadata(json_path):
    data=dict()
    if os.path.isfile(json_path):
        with open(json_path, "r", encoding="utf-8") as fileh:
            data = json.load(fileh)
    return data
    
def changeWallpaper(env, img_path):
    print("changeWallpaper: changing wallpaper to '{}'".format(img_path))
    if env == ENV.GNOME3:
        setWallpaperGnome3(img_path)
    elif env == ENV.WIN:
        setWallpaperWindows(img_path)
    elif env == ENV.PLASMA5:
        setWallpaperPlasma5(img_path)
    else:
        print("ERROR: Platform not implemented yet")

def changeWallpaperPeriodically(env, filelist, next_file, sch, period, img_dir): 
    # do your stuff
    file_to_use = filelist[next_file]
    next_file = (next_file+1) % len(filelist)
    img_path = os.path.join(img_dir, file_to_use)
    #print("[changeWallpaperPeriodically] Changing wallpaper to: '{}'".format(img_path))
    changeWallpaper(env, img_path)
    
    priority = 1
    pos_args=(env, filelist, next_file, sch, period, img_dir)
    sch.enter(period, priority, changeWallpaperPeriodically, argument=pos_args)
    
def getOutputDir(env):
    if env in ["gnome", "kde"]:
        img_dir = os.path.expandvars("$HOME/.potd")
    elif env=="windows":
        img_dir = os.path.expandvars("%HOMEPATH%/Pictures/potd")
    else:
        raise Exception("Environment not implemented")
    os.makedirs(img_dir, exist_ok=True)
    return img_dir
        
if __name__ == "__main__":  

    parser = argparse.ArgumentParser(description='Download the Photo of the Day of various sites and set it as the wallpaper of your desktop.')
    parser.add_argument('--site', choices=['ng', 'bing', 'wiki', 'guardian','nasa', 'smith', 'all'], help='The website from which to download Photo of the Day.')
    parser.add_argument('--loop', action='store_true', default=False, help='Changes screenshot every x seconds.')
    parser.add_argument('--debug', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--period', type=int, default=60, help='Changes screenshot every x seconds.')
    args = parser.parse_args()

    # Generate file paths
    env = deskenv.get_desktop_environment()
    # name of the output image file
    img_dir = getOutputDir(env)
    img_filename = str(datetime.datetime.now().date()).replace("-","")
    img_path = os.path.join(img_dir, img_filename)
    json_path = os.path.splitext(img_path)[0] + ".json"

    # Download wallpaper images

    spec_path = None
    
    if args.site in ['ng', 'all']:
        spec_path = img_path+"ng.jpg"
        if not os.path.isfile(spec_path):
            getNGLink(spec_path)
        else:
            print("National Geographic wallpaper already downloaded")
            
    if args.site in ['bing', 'all']:
        spec_path = img_path+"bing.jpg"
        if not os.path.isfile(spec_path):
            getBingLink(spec_path)    
        else:
            print("Bing wallpaper already downloaded")
            
    if args.site in ['wiki', 'all']:
        spec_path = img_path+"wiki.jpg"
        if not os.path.isfile(spec_path):
            getWikiMediaLink(spec_path)
        else:
            print("Wikimedia wallpaper already downloaded")
        
    if args.site in ['guardian', 'all']:
        spec_path = img_path+"guardian.jpg"
        if not os.path.isfile(spec_path):
            getGuardianLink(spec_path)
        else:
            print("The Guardian wallpaper already downloaded")
        
    if args.site in ['nasa', 'all']:
        spec_path = img_path+"nasa.jpg"
        if not os.path.isfile(spec_path):
            getNASALink(spec_path)
        else:
            print("NASA wallpaper already downloaded")
    
    if args.site in ['smith', 'all']:
        spec_path = img_path+"smith.jpg"
        if not os.path.isfile(spec_path):
            getSmithLink(spec_path)
        else:
            print("Smithsonian wallpaper already downloaded")
            
    assert(img_path is not None)
    
    # Set the image as the new desktop wallpaper
    #saveMetadata(img_path, args.site, json_path)
    
    if args.loop:
        print("Entering loop....")
        sch = sched.scheduler(time.time, time.sleep)
        next_file = 0
        datestr = str(datetime.datetime.now().date()).replace("-","")
        if args.debug:
            print("datestr="+datestr)
        filelist = [f for f in os.listdir(img_dir) if (os.path.isfile(os.path.join(img_dir, f)) and f[0:8]==datestr)]
        if args.debug:
            print("File list is:")
            print(*filelist, sep='\n')
        pos_args=(env, filelist, next_file, sch, args.period, img_dir)
        #scheduler.enter(delay, priority, action, argument=(), kwargs={})
        # Call it the first time immediately (period=0)
        sch.enter(0, 1, changeWallpaperPeriodically, argument=pos_args)
        sch.run()
        while True:
            time.sleep(args.period*100)
            
    else:
        if spec_path is None:
            print("ERROR: you haven't downloaded any wallpaper")
        else:
            changeWallpaper(env, spec_path)
