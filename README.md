# Picture of the Day

## Description
"Picture of the Day" is a Python 3 script that downloads the photo of the day from:
* National Geographic
* Bing
* Wikimedia
* The Guardian
* The Smithsonian
and set it as the wallpaper of your desktop. Windows, GNOME 3 and Plasma 5 desktops are supported.

## Requirements
You need Python 3 and some packages, namely BeautifulSoup 4 and lxml.

In order to install the required packages, run:
```pip install bs4 lxml```

## Example
Call the script:

```
python potd.py --site ng
```

to download the Photo of the Day from the National Geographic website and set it as the wallpaper of your desktop.

As the argument to `--site`, you can use
* `ng` for National Geographic
* `bing` for Bing
* `guardian` for The Guardian
* `wiki` for Wikimedia
* `smith` for The Smithsonian
* `all` for all of the above in one call of the script

## Running at startup

You can set the script to run at startup. The script will check if today it has already downloaded a picture. If so, it won't download it again.

On Windows, create a link in the folder `C:\Users\<your_username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`. 
You can open this folder also by pressing `<windows key>+R` to open the "Run" dialog, type `shell:startup` in the textbox and press "Run".
