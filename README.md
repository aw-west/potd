# Picture of the Day

## Description
"Picture of the Day" is a Python 3 script that downloads the photo of the day from:
-National Geographic
-Bing
-Wikimedia
-The Guardian
and set it as the wallpaper of your desktop. Windows, GNOME 3 and Plasma 5 desktops are supported.

## Requirements
You need Python 3 and some packages, namely BeautifulSoup 4 and lxml.
In order to install the required packages, run:
```pip install bs4 lxml```

## Example
Call the script:

```
python natgeo.py --site ng
```

to download the Photo of the Day from the National Geographic website and set it as the wallpaper of your desktop.

As the argument to `--site`, you can use
1. `ng` for National Geographic
2. `bing` for Bing
3. `guardian` for The Guardian
4. `wiki` for Wikimedia

## Running at startup

You can set the script to run at startup. The script will check if today it has already downloaded a picture. If so, it won't download it again.

On Windows, create a link in the folder `C:\Users\<your_username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`. 
You can open this folder also by pressing `<windows key>+R` to open the "Run" dialog, type `shell:startup` in the textbox and press "Run".
