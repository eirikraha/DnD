import requests
from bs4 import BeautifulSoup
from numpy import ceil

class SpellBookCreator():

	def __init__(self, SpellBookName):
		"""
		Initiates the spell book.
		"""
		self.SpellBookName = SpellBookName
		self.SpellBook = {}

	def readSpell_online(self, spellname):
		"""
		Reads spell information from
		the web. For now it's just 
		read from roll20.com, however
		I will hopefully update to cross
		referencing multiple websites in the 
		future.
		"""

		spellname = spellname.replace(' ', '%20')  #Checks if there are any spaces and replaces them
		spell_url = "https://roll20.net/compendium/dnd5e/%s" %spellname

		spell_page = requests.get(spell_url)   #Reads URL
		soup_spell = BeautifulSoup(spell_page.content, 'html.parser')


		#Finds the spell parameters and the spell description
		spell_url_info = soup_spell.findAll('div', {'class': 'attrListItem row'})
		spell_url_text = soup_spell.findAll('meta', {'name': 'description'})
		spell_url_text2 = soup_spell.findAll('div', {'class': 'value'})[-1]  #possible better source of text
		spell_url_text2 = (' '.join(((str(spell_url_text2).split('<div class="value">'))[1].split('<br>')))).split('</br>')[0]


		if str(spell_url_text2)[-6:] == '</div>':
				spell_url_text2 = str(spell_url_text2)[:-6]

		#Initiates spell info dictionary
		spell_info = {'Status': 'Idle'}
		print (spell_url_text2, spell_url_text)
		print (len(spell_url_text2), len(str(spell_url_text).split('"')[1]))  
		if len(spell_url_text2) > len(str(spell_url_text).split('"')[1]):

			spell_info.update({'Text': str(spell_url_text2)})
		else:
			spell_info.update({'Text': str(spell_url_text).split('"')[1]})   #Sets spell description

		for i in spell_url_info:
			classifier = i.findAll('div', {'class': 'col-md-3 attrName'})   #Finds parameter name
			value = i.findAll('div', {'class': 'value'})                    #Finds parameter value

			#Updates spell parameters
			spell_info.update({(str(classifier).split('>')[1].split('<')[0]): ((str(value).split('>')[1].split('<')[0]))})

		return spell_info

	def readSpell_userInput(self, spellname):
		"""
		Reads spell information from
		user input.
		"""

		#Spell dictionary defined with the same parameters as found
		#at roll20.com
		spell_info = {'Duration': 0, 'Text': 0, 'School': 0, 'Status': 'Idle', 
						'Save': 0, 'Casting Time': 0, 'Range': 0, 'Damage': 0, 
						'Damage Type': 0, 'Classes': 0, 'Components': 0,
						'Damage Progression': 0, 'Level': 0, 'Material': 0}

		#Asks the user for what to fill in
		for i in spell_info:
			spell_info[i] = input('What is the value for the %s?' %i)

		return spell_info

	def addSpell(self, spellname, fromWeb = True):
		"""
		Adds a new spell to the spell book either from
		roll20.com or from user input.
		The spell is set to idle by default.
		"""

		if fromWeb:
			spell_info = self.readSpell_online(spellname)

		if not fromWeb:
			spell_info = self.readSpell_userInput(spellname)

		self.SpellBook.update({spellname: spell_info})


	def removeSpell(self, spellname):
		"""
		Entirely removes spell from spell book.
		"""
	
		self.SpellBook.pop(spellname, None)

	def set_as_active(self, spellname):
		"""
		Sets a spell as active, i.e. prepared.
		"""

		(self.SpellBook[spellname])['Status'] = 'Active'

	def set_as_idle(self, spellname):
		"""
		Sets a spell as idle, i.e. not prepared.
		"""

		(self.SpellBook[spellname])['Status'] = 'Idle'

	def createTEX(self, filename, rows = 2, columns = 2, height = 8.8, width = 6.3):
		"""
		Takes all the active and inactive spells, sorts them
		after level and name and creates a printable spellbook using LaTeX.
		Card dimensions are in cm and are set to pokémon card standard.
		"""

		file = open(filename + '.tex', 'w')
		file.write('%s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n \n %s \n \n'
					%('\\documentclass[a4paper,portrait]{article}',	
					 '\\usepackage[margin=15mm]{geometry}',
					 '\\usepackage[ngerman]{babel}',
					 '\\usepackage{tikz}',
					 '\\usepackage{pifont}',
					 '\\usepackage{pifont}',
					 '\\usepackage{graphicx}',
					 '\\usepackage{adjustbox}',
					 '\\input{tikz-lib}'))

		file.write('%s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n \n%s \n' 
					%('\\usepackage{geometry}',
					  '\\geometry{',
  					  'top=0.5in,',
  					  'inner=0.1in,',
  					  'outer=0.1in,',
  					  'bottom=0.5in,',
  					  'headheight=1ex,',
  					  'headsep=1ex,}',
  					  '\\setlength{\\tabcolsep}{0pt}',
 					  '\\begin{document} '))
		spellcounter = 0

		for i in self.SpellBook:
			n = 70.
			if (len(str(self.SpellBook[i]['Text']).split())) > n:
				str_len = (len(str(self.SpellBook[i]['Text']).split()))
				text_list = (str(self.SpellBook[i]['Text']).split())

				for j in range(0, int(ceil(str_len/n))):
					if spellcounter == 3 or spellcounter == 6 or spellcounter == 9:
						file.write('%s' 
						%('\\\\ \n'))
					elif spellcounter == 0:
						file.write('\\begin{tabular}{c c c} \n')
					else:
						file.write('& \n')

					file.write('%s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n\n' 
					%('\\begin{tikzpicture}',
					  '\\SetBackground{spellbkg.jpg}',
					  '\\SetTitle{%s (%d/%d)}' %(self.SpellBook[i]['Name'], j+1, int(ceil(str_len/n))),
					  '\\SetCastingTime{%s}' %self.SpellBook[i]['Casting Time'],
					  '\\SetRange{%s}' %self.SpellBook[i]['Range'],
					  '\\SetComponents{%s}' %self.SpellBook[i]['Components'],
					  '\\SetDuration{%s}' %self.SpellBook[i]['Duration'],
					  '\\SetText{%s}' %' '.join(text_list[int(ceil(((j)/int(ceil(str_len/n)) * str_len))):int(ceil(((j+1)/int(ceil(str_len/n)) * str_len)))]),
					  '\\end{tikzpicture}'
					  ))
					spellcounter += 1

					if spellcounter == 9:
						file.write('%s \n %s \n' 
								 %('\\end{tabular}', '\\\\'))

						spellcounter = 0

			else:
				if spellcounter == 3 or spellcounter == 6 or spellcounter == 9:
					file.write('%s' 
						%('\\\\ \n'))
				elif spellcounter == 0:
					file.write('\\begin{tabular}{c c c} \n')
				else:
					file.write('& \n')

				file.write('%s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n\n' 
						%('\\begin{tikzpicture}',
						  '\\SetBackground{spellbkg.jpg}',
						  '\\SetTitle{%s}' %self.SpellBook[i]['Name'],
						  '\\SetCastingTime{%s}' %self.SpellBook[i]['Casting Time'],
						  '\\SetRange{%s}' %self.SpellBook[i]['Range'],
						  '\\SetComponents{%s}' %self.SpellBook[i]['Components'],
						  '\\SetDuration{%s}' %self.SpellBook[i]['Duration'],
						  '\\SetText{%s}' %self.SpellBook[i]['Text'],
						  '\\end{tikzpicture}'
						  ))

				spellcounter += 1

				if spellcounter == 9:
					file.write('%s \n %s \n' 
						%('\\end{tabular}', '\\\\'))

					spellcounter = 0
		if spellcounter != 0:
			file.write('\\end{tabular} \n')
		file.write('\\end{document}')



	def createTXT(self, filename):
		"""
		Takes all the active and inactive spells, sorts them
		after level and name and creates a printable spellbook.
		"""

		file = open(filename, 'w')
		for i in self.SpellBook:
			file.write('%s \n\n' %i)
			for j in self.SpellBook[i]:
				file.write('%s: %s' %(j, self.SpellBook[i][j]))
				file.write('\n')

			file.write('\n\n\n')

if __name__ == '__main__':
	SpellBook = SpellBookCreator('Spell Book')
	SpellBook.addSpell('Vicious Mockery')
	SpellBook.addSpell('Light')
	SpellBook.addSpell('Prestidigitation')
	SpellBook.addSpell('Charm Person')
	SpellBook.addSpell('Healing Word')
	SpellBook.addSpell('Identify')
	SpellBook.addSpell('Thunderwave')
	SpellBook.addSpell('Detect Thoughts')
	SpellBook.addSpell('Invisibility')
	#SpellBook.addSpell('Phantasmal Force')
	SpellBook.createTEX('Odd Spell Book lvl 4')