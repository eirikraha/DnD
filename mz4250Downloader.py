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

urladdress_init = "https://www.shapeways.com/designer/mz4250/creations"
page_init = requests.get(urladdress_init)
soup_init = BeautifulSoup(page_init.content, 'html.parser')

PagesNum = soup_init.findAll('span', {'class':'results-page results-page-selected enabled'})
maxPageNum = 0

for i in str(PagesNum[-1]).split(' '):
	if i.isdigit():
		maxPageNum = int(i)

index_list = [i*48 for i in range(0, maxPageNum)]

#Change FilesList to path of 3Dfiles folder if 
#it's not the same as the folder where the 
#python script is stored.
#E.g. '../figures/*.stl'

FilesList = glob.glob('*.stl')

new_finder = 0
NewFigsList = []

for j in index_list:
	print float(j)/index_list[-1]    #This is just a progress tracker, remove if you find it annoying
	urladdress = "https://www.shapeways.com/designer/mz4250/creations?s=%d#more-products" %j

	page = requests.get(urladdress)
	soup = BeautifulSoup(page.content, 'html.parser')

	#Simplified the scrapping process
	figures = soup.findAll('a', {'class': 'product-url'})

	counter = 0
	for i in range(0, len(figures)):
		switch = 0
		if counter == i/2.:
			text = str(figures[i])
			figureURL = ((text.split('href'))[1].split('&')[0])[2:]
	 		fileURL = figureURL[:34] + 'download/' + figureURL[34:43]
	 		filename = (figureURL[44:]).split('?')[0]

	 		# print fileURL
	 		# print figureURL
	 		# print filename

	 		for k in FilesList:
	 			if k == (filename + '.stl'):
	 				switch = 1
	 		if switch != 1:
	 			print "Found missing link!"
	 			print filename

	 			# This must be changed to download the files to a different folder.
	 			# E.g. '../figures/*.stl'
	 			urllib.urlretrieve(fileURL, '%s.stl' %filename)
	 			NewFigsList.append(filename)
	 			new_finder += 1
			counter += 1