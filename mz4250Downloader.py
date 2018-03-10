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


import requests
from bs4 import BeautifulSoup
import urllib
import sys
import glob
from pathlib import Path

######## Change this to change destination folder ##############
######## Include trailing slash ################################
folder = ''
################################################################

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
		fileName = figure['title'].replace('/', '') + '.stl'
		fileURL = 'https://www.shapeways.com/product/download/' + figure['data-spin'] 
		my_file = Path(folder + fileName)
		if my_file.is_file():
			print fileName + ' already exists.'
		else:
			urllib.urlretrieve(fileURL, folder + fileName)
			print fileName + ' has been downloaded'
