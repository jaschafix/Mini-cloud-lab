import time
import os
from itertools import cycle, islice
import pprint

os.chdir('../Klanten')
klanten = os.listdir()

programmaDir= '/home/student/Desktop/VM2/Klanten/'

print("Welkom bij het selfservice portal van VM2\n")
klantKeuze = input("Bent u al een bestaande klant? (y/n)")

klantLiegt = False
gebruiker = ""

if klantKeuze == "y":
	klantnaam = input("Wat is uw naam? (hoofdlettergevoelig)")
	for klant in klanten:
		if klantnaam == klant:
			gebruiker = klantnaam
			break

	if gebruiker == "":
		print("Naam niet gevonden.\n vul eerst uw naam in.")
		klantLiegt = True
if klantKeuze == "n" or klantLiegt:
	gebruiker = input("Wat is uw naam?")
	os.mkdir(gebruiker)
	print("U bent toegevoegd aan het systeem")


os.chdir(f'{programmaDir}{gebruiker}/')

os.system('clear')

print("Dit zijn uw huidige omgevingen:\n")
for omgeving in os.listdir():
	print(omgeving)

omgevingkeuze = input("Wilt u een nieuwe omgeving maken? (y/n)")

if omgevingkeuze == "y":
	print("Geef de omgeving een naam.")
	omgevingsnaam = input("naam: ")
	os.mkdir(omgevingsnaam)
	os.system('clear')
	print("Een nieuwe omgeving is gemaakt.")
	print("Dit zijn uw huidige omgevingen:\n")
	for omgeving in os.listdir():
		print(omgeving)

omgevingsnaam = input("vul de naam in van de omgeving die u wilt aanpassen: (hoofdlettergevoelig)")

os.chdir(f"{os.getcwd()}/{omgevingsnaam}")
files = os.listdir()

keuze =""
isNieuweOmgevingGemaakt = False
isOmgevingAangepast = False
servers_settings = {} 	#variable voor vagrantfile settings
sjabloon = ""	#variable voor sjabloon van de vagrantfile

if 'Vagrantfile' not in files:
	print("Deze omgeving is nog leeg.")
	print("Welke soort omgeving wilt u uitrollen?\nProductie: 2-4 webservers, 1 loadbalancer, 1 database\nTest-omgeving:1 webserver\nAcceptatie-omgeving: 2 webservers, 1 loadbalancer, 1 database")
	keuze = input("Productie, Test of Acceptatie: ").lower()
	isNieuweOmgevingGemaakt = True
else:
	sjabloon = open('Vagrantfile', 'r').readlines()
	#os.system('rm Vagrantfile')
	servers_settings = {
	'AantalWeb' : "", 
	'Naam' : "", 
	'Omgeving' : "", 
	'Netwerk' : "", 
	'Webserver_geheugen' : 0, 
	'Webserver_cpu' : 0,
	'Database_geheugen' : 0, 
	'Database_cpu' : 0, 
	'Loadbalancer_geheugen' : 0,
	'Loadbalancer_cpu' : 0
	}

	for lines in sjabloon:
		for key, setting in servers_settings.items():
			if lines.startswith(key, 2):
				nieuwe_content = lines.strip().split("=")[1].strip()
				servers_settings[key]= nieuwe_content
	print("de huidige omgeving ziet er als volgt uit:")

	#lege values verwijderen
	for key, setting in list(servers_settings.items()):
		if isinstance(setting, int):
			if setting == 0:
				del servers_settings[key]
		else:
			if setting == "":
				del servers_settings[key]

	pprint.pprint(servers_settings)

	Omgeving_aanpassen = input("Wilt u deze (a)anpassen of (v)erwijderen? (a/v)").lower() 
	if Omgeving_aanpassen == 'a':
		for key in servers_settings:
			if key != 'Naam' and key != 'Omgeving' and key != 'Netwerk':
				print("Vul een waarde in\nDe huidige waarde is " + key.lower() + " : " + servers_settings[key])
				servers_settings[key] = input("Welke nieuwe waarde moet de "+ key + " krijgen?")

		nieuwe_config = open('Vagrantfile', 'w')

		isOmgevingAangepast = True

	elif Omgeving_aanpassen == 'v':
		os.system('vagrant destroy')
		os.chdir('../')
		print(os.getcwd())
		os.system('rm '+ omgevingsnaam + " -R")
		exit()

	else:
		print("Ongeldige invoer script wordt gestopt")


if keuze == 'productie' and isNieuweOmgevingGemaakt:
	aantal_webservers = int(input("Hoeveel webservers moet deze omgeving hebben?"))
	sjabloon = open('../../../selfservice_portal/Vagrantfile-productie', 'r').readlines()
if keuze == 'test' and isNieuweOmgevingGemaakt:
	sjabloon = open('../../../selfservice_portal/Vagrantfile-test', 'r').readlines()
	aantal_webservers = 1
if keuze == "acceptatie" and isNieuweOmgevingGemaakt:
	sjabloon = open('../../../selfservice_portal/Vagrantfile-acceptatie', 'r').readlines()
	aantal_webservers = 1

# dictionary met in te voeren settings in de vagrantfile
# 0 = aantal webservers
# 1 = klantnaam
# 2 = Omgevingsnaam
# 3 = netwerkID
# 4 = webserver_geheugen 
# 5 = webserver_cpu 
# 6 = database_geheugen  
# 7 = database_cpu 
# 8 = loadbalancer_geheugen
# 9 = loadbalancer_cpu 
webserver_geheugen = 512
webserver_cpus = 1
database_geheugen = 512
database_cpus = 1
loadbalancer_geheugen = 512
loadbalancer_cpus = 1
netwerkid = "192.168."

if isNieuweOmgevingGemaakt:
	#volgend netwerk id uit /etc/hosts halen
	Alle_ipadress = []
	oude_hosts = (open('/etc/hosts', 'r').readlines())

	for index, lines in enumerate(islice(cycle(oude_hosts), len(oude_hosts))):
		next = index +1
		if lines.startswith('#'):			
			ipadress = oude_hosts[next].split()
			ipadress = ipadress[0].split('.')
			derde_octet = ipadress[2]
			Alle_ipadress.append(int(derde_octet))

	#kijken of een netwerk id mist, dit kan zijn door een verwijderde omgeving di een klant eerder heeft gemaakt.
	for index, ip in enumerate(Alle_ipadress):
		verwachte_octet = int(ip) 
		if verwachte_octet+1 not in Alle_ipadress:
			netwerkid += str(verwachte_octet+1)
			break
		elif index +1 == len(Alle_ipadress):
			netwerkid += str(verwachte_octet+1)

	#settings voor de vagrant file opstellen
	print("De default specificaties voor de servers zijn 512MB geheugen en 1 cpu")
	default_values = input("Wilt u de default specificaties? (y/n)").lower()

	if default_values == 'y':
		pass
	elif default_values == 'n':
		webserver_geheugen = int(input('Hoeveel geheugen moeten de webservers hebben?'))
		webserver_cpus = int(input('Hoeveel virtuele cpu\'s moeten de webservers hebben?(1-2)'))
		if keuze == 'acceptatie' or keuze == 'productie':
			database_geheugen = int(input('Hoeveel geheugen moeten de databaseservers hebben?'))
			database_cpus = int(input('Hoeveel virtuele cpu\'s moeten de databaseserver hebben?(1-2)'))
			loadbalancer_geheugen = int(input('Hoeveel geheugen moeten de loadbalancer hebben?'))
			loadbalancer_cpus = int(input('Hoeveel virtuele cpu\'s moeten de loadbalancer hebben?(1-2)'))
	else:
		print('ongeldige invoer')
		quit()

	servers_settings= {
	'AantalWeb' : aantal_webservers, 
	'Naam' : '"'+gebruiker+'"', 
	'Omgeving' : '"'+keuze+'"', 
	'Netwerk' : '"'+netwerkid+'"', 
	'Webserver_geheugen' : webserver_geheugen, 
	'Webserver_cpu' : webserver_cpus,
	'Database_geheugen' : database_geheugen, 
	'Database_cpu' : database_cpus, 
	'Loadbalancer_geheugen' : loadbalancer_geheugen,
	'Loadbalancer_cpu' : loadbalancer_cpus
	}

	# /etc/hosts updaten
	command = 'sudo ../../../selfservice_portal/Proxy-sudo.sh ' + netwerkid + " "+ gebruiker + " " + keuze + " " + str(aantal_webservers)
	os.system(command)

#vagrant file updaten of schrijven met nieuwe waarden.
vagrant_config = open('Vagrantfile', 'w')

for lines in sjabloon:
	keys = list(servers_settings.keys())	
	nieuwe_content = ""
	for key in keys:
		if lines.startswith(key, 2):
			if isinstance(servers_settings[key],int):
				nieuwe_content = "  "+ key + " = "+ str(servers_settings[key])+ "\n"
			else:
				nieuwe_content = "  "+ key + " = "+ (servers_settings[key])+ "\n"
			break
	if nieuwe_content == "":
		nieuwe_content = lines
	vagrant_config.write(nieuwe_content)
vagrant_config.close()

if isNieuweOmgevingGemaakt:
	os.system('vagrant up')
	print("wachten tot machines klaar zijn met opstarten.")
	time.sleep(30)
	
	#ssh keys toevoegen aan known_hosts
	if keuze != 'test':
		os.system('ssh-keyscan ' + netwerkid + ".10 " + gebruiker + "-" + keuze + "-"+ "LB >> ~/.ssh/known_hosts")
		os.system('ssh-keyscan ' + netwerkid + ".11 " + gebruiker + "-" + keuze + "-"+ "DB >> ~/.ssh/known_hosts")
		for x in range(aantal_webservers):
			os.system('ssh-keyscan ' + netwerkid + "." + str(12+x) + " " +gebruiker + "-" + keuze + "-"+ "WS" + str(x+1) + ">> ~/.ssh/known_hosts")
	else:
		os.system('ssh-keyscan ' + netwerkid + ".10 " + gebruiker + "-" + keuze + "-"+ "WS" + " >> ~/.ssh/known_hosts")

	#ansible inventory file maken
	ansible_inventory = open('inventory.ini', 'w')
	if keuze != 'test':
		ansible_inventory.write("[loadbalancer]\n")
		ansible_inventory.write(netwerkid + ".10\n\n")
		ansible_inventory.write("[database]\n")
		ansible_inventory.write(netwerkid + ".11\n\n")
		ansible_inventory.write("[web]\n")
		for x in range(aantal_webservers):
			ansible_inventory.write(netwerkid + "." + str(x+12) + "\n")
	else:
		ansible_inventory.write("[web]\n")
		ansible_inventory.write(netwerkid + ".10\n")
	ansible_inventory.close()

	#ansible playbooks uitvoeren
	os.system('cp ../../../selfservice_portal/ansible.cfg ansible.cfg')
	if keuze != 'test':
		os.system('ansible-playbook ../../../Playbooks/LAMP-omgeving.yml')
	else:
		os.system('ansible-playbook ../../../Playbooks/TEST-omgeving.yml')

if isOmgevingAangepast:
	os.system('vagrant reload') 