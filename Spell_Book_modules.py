import requests
from bs4 import BeautifulSoup

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

		#Initiates spell info dictionary
		spell_info = {'Status': 'Idle'}  
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

	def createPDF(self, rows = 2, columns = 2, height = 8.8, width = 6.3):
		"""
		Takes all the active and inactive spells, sorts them
		after level and name and creates a printable spellbook.
		Card dimensions are in cm and are set to pokémon card standard.
		"""

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
	SpellBook.addSpell('Magic Missile')
	SpellBook.addSpell('Resurrection')
	SpellBook.createTXT('test.txt')