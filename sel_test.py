# mz4250 has made some truly pretty 3D models of monsters from DnD 5e
# I wanted to download them all and update whenever I saw I uploaded more
# so I thought: "It's time to look more into HTML which I don't know anything about"
# and this is the result.
# I have asked mz4250 permission to share this code, and he said it was cool
# Let's share this code (or improve it and upload a better version if that's what you want,
# just send me a message and I will make you a contributor on github)
# and enjoy DnD with many monster minis!
# 
# When you run the program it checks which figures you have already downloaded in the folder
# the program is run from. If you want to download the files to another folder, please update
# urllib.urlretrieve(fileURL, '%s.stl' %filename) on line 103
# If you want it to check another folder, please update FilesList on line 56.
# to your preferred folder relative to the folder the program is in.
# Every mini the program finds that is not in this folder, will be downloaded.
#
# mz4250 didn't ask me to put this in, but I think it's just fair to advertise a bit:
# mz4250 have provided these 3D files free of charge. Please support him by either
# going to his patreon or buying his figures directly from him on shapeways.
#
# TL;DR Made the program, it's my first time using HTML code in any way. mz4250 makes great
# figures. This program downloads them all, and mz4250 said it was ok. The program downloads
# all figures not already downloaded to the same folder as you have the program in. The 
# download folder can be changed.
#
# Made by u/scuper42
#
# Please enjoy!
#
# Edit 1: Finally making some progress! So sorry that I uploaded a non-working script
# The problem was, as pointed out by some that the programmed hadn't logged anyone in.
# This turned out to be an bigger issue than I had expected. I tried different libraries
# but ended up with one called Selenium which works great when it actually works. To get it
# working, I had do download the file chromedriver.exe from: 
# and once it was downloaded I put it in the same folder as the program. It didn't work at first
# but I found that the solution was to open another terminal, navigate to the same folder and 
# activate it by typing: "./chromedriver.exe" then I could run this script.
#
# So, please do the same and try it out. This is still very early in the process and I will
# improve upon the script. I just wanted to give you guys a working script while I figure out
# how to make it better.
#
# As it is now you have to use chrome as your browser and you have to login for each time. In the
# future I will also add firefox support and probably check if you are already logged in or not.
#
# When you run the script now you log in with the username and password defined below. You have to
# manually alter the script to take your username and your password before running the script.
#
# After the program has logged you in, you have to verify that you are not a robot. The script pauses until
# you have passed this robot test. Then you have to start it again by going to you console/terminal and 
# press Enter. The program will now continue and download all the files from mz4250. I only tested for about
# 30 downloads before I quit (I have extremely little space left on my SSD), but I hope it will work for
# all 900 and something files. The progrem does NOT check which you have already downloaded as for now.
# This will be added in the futere
#
# The code is a mashup of different contributers and two different ways of accessing shapeways. It is
# not pretty, but what was most important to me now was to get it working. I will tidy up soon :)
#
# To install pip by writing in the console: sudo apt-get install python-pip
# And to install selenium you write: sudo pip install selenium 
#
# If you have any problems, please pm me or write to me in the reddit post.
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import urllib, urllib2
#import sys
#import glob
#import browsercookie
from pathlib import Path

LoginURL = "https://www.shapeways.com/login"
WebURL = "https://www.shapeways.com/product/AWEZRHCJY/roc?optionId=57876021&li=marketplace"
FileURL = "https://www.shapeways.com/product/download/AWEZRHCJY"
driver = webdriver.Chrome('chromedriver.exe')

cookies = driver.get_cookies()
driver.get(LoginURL)

username = driver.find_element_by_id('login_username')
password = driver.find_element_by_id('login_password')

username.send_keys("YourUsernameHere")   #Write your username here!
password.send_keys("YourPasswordHere")	 #Write your password here!

driver.find_element_by_id('sign_in_button').click()

raw_input('Press enter to continue')    #The program will not continue until you press Enter
print "Enter has been pressed"


folder = 'C:/Users/Eirik/'

urladdress_init = "https://www.shapeways.com/designer/mz4250/creations"
page_init = requests.get(urladdress_init)
soup_init = BeautifulSoup(page_init.content, 'html.parser')

PagesNum = soup_init.findAll('span', {'class':'results-page results-page-selected enabled'})
maxPageNum = 0

for i in str(PagesNum[-1]).split(' '):
	if i.isdigit():
		maxPageNum = int(i)

index_list = [i*48 for i in range(0, maxPageNum)]

for j in index_list:
	urladdress = "https://www.shapeways.com/designer/mz4250/creations?s=%d#more-products" %j

	page = requests.get(urladdress)
	soup = BeautifulSoup(page.content, 'html.parser')

	#Simplified the scrapping process
	figures = soup.findAll('div', {'class': 'product-info'})

	for figure in figures:
		#Forward slashes are bad on unix filesystems, so remove them.
		fileName = figure['title'].replace('/', '') 
		fileURL = 'https://www.shapeways.com/product/download/' + figure['data-spin'] 
		my_file = Path(folder + fileName)
		if my_file.is_file():
			print fileName + ' already exists.'
		else:
			# passman.add_password(None, fileURL, username, password)
			# authhandler = urllib2.HTTPBasicAuthHandler(passman)

			# opener = urllib2.build_opener(authhandler)

			# urllib2.install_opener(opener)

			# pagehandle = urllib2.urlopen(fileURL)
			# data = pagehandle.read()
			# with open(folder + filename, "wb") as code:
			# 	code.write(data)

			# r = s.get(fileURL, auth=(username, password))
			# print fileURL
			# print r.headers
			# # urllib.urlretrieve(fileURL, folder + fileName)
			# print fileName + ' has been downloaded'

			driver.get(fileURL)

driver.close()