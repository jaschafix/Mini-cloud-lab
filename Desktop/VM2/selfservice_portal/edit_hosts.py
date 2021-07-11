import sys

nieuwe_hosts = (open('/etc/hosts', 'a'))
netwerk = {}

netwerkid = str(sys.argv[1])
gebruiker = str(sys.argv[2])
keuze = str(sys.argv[3])
aantal = int(sys.argv[4])

if keuze == 'test':
	netwerk[netwerkid + ".10"] = gebruiker + "-" + keuze + "-WS"
else:
	netwerk[netwerkid + ".10"] = gebruiker + "-" +keuze +"-LB"
	netwerk[netwerkid + ".11"] = gebruiker + "-" +keuze +"-DB"
	for x in range(aantal):
		netwerk[netwerkid + "."+str(x+12)] = gebruiker + "-" +keuze +"-WS-" + str(x+1)

nieuwe_hosts.write("\n#"+gebruiker+"-"+keuze+"\n")

for key, x in netwerk.items():
	nieuwe_hosts.write(key + " " + x +"\n")

nieuwe_hosts.close()
