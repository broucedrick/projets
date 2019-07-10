import requests
from bs4 import BeautifulSoup
import ast
import datetime


req = requests.get("https://deals.jumia.ci/abidjan/vehicules/")
link_statut = req.status_code
nb_page = 1
print (nb_page)

#lien_page = "abidjan/vehicules/"

#while lien_page != "abidjan/vehicules?page=10":

	# lien = "https://deals.jumia.ci/" + lien_page
	# #print lien
	# req = requests.get(lien)
	# page = BeautifulSoup(req.text, "lxml")
plus_chere = 0
nb_poste = 0	
	
hier = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
def date_hier(date):
	global jour

	jour = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M').date()
		#print jour
	return jour

	

# def veh_moins_chere():
# 	global moins_chere
# 	global marqe

# 	moins_chere = plus_chere

# 	for poste in page.findAll({'article'}):
# 		date = poste.find('time').get('datetime')
# 		if date_hier(date) == hier.date():
# 			prix = float(ast.literal_eval(poste.get('data-event'))['price'])
# 			marque = ast.literal_eval(poste.get('data-event'))['title']
# 			#print prix
# 			if int(prix) < moins_chere:
# 				moins_chere = int(prix)
# 				marqe = marque
	
while link_statut == 200:
	page = BeautifulSoup(req.text, "lxml")
	for poste in page.findAll({'article'}):
			date = poste.find('time').get('datetime')
			type_vehicule = poste.find('span',{'class':'address'}).getText().strip()[0]
			if date_hier(date) == hier and type_vehicule == 'V':
				nb_poste += 1
				prix = float(ast.literal_eval(poste.get('data-event'))['price'])
				#print (prix)
				marque = poste.find('a',{'class':'post-link post-vip'}).get('title')
				#print prix
				if int(prix) > plus_chere:
					plus_chere = int(prix)
					marq = marque
				else:
					moins_chere = int(prix)
					marqe = marque
	nb_page += 1
	print (nb_page)
	lien = "https://deals.jumia.ci/abidjan/vehicules?page="+ str(nb_page)
	#print (lien)
	req = requests.get(lien)
	link_statut = req.status_code
	# print(nb_page, link_statut)
	# if nb_page == 30:
	# 	break

print ('Hier : ',hier)
print ('Il y a eu ', nb_poste,' voiture(s) postee(s) sur jumia Deals')
print ('La voiture la plus chere etait une ',marq, 'elle vaut ',plus_chere)
print ('La voiture la moins chere etait une ',marqe, 'elle vaut ',moins_chere)