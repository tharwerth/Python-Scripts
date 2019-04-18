#########################################################################
# This script takes the very long FirewallDenyByLocationWithExlusions report, removes duplicate IPs, and runs a whois and reverse DNS for each unique IP
#
# To modify this for you own local use, change the rootdir variable to your own local directory where the logs are stored and rename the report to fdeny
#
# After the script is completed, there will be a txt file named fdeny.txt that will contain all the information parsed in a readable fashion
#########################################################################

#import all libraries
import csv
import pprint
import dns
from dns import resolver
from dns import reversename
import ipwhois
from ipwhois import IPWhois
from ipwhois.exceptions import (ASNLookupError, ASNRegistryError, WhoisLookupError, HTTPLookupError, BlacklistError)
import os
from pprint import pprint

#create variables and lists
ips = []
ports = []
deDupedIPs = []
datearray = []
rootdir = "%filepath%\\logs"
topdir = ""
fdeny = "%filename%"
csvFromLR = ()


#enter the dated folder that holds the report that has been renamed to fdeny
print("Enter first date to parse, seperate with spaces: ")
datearray = [int(x) for x in input().split()] #This will take multiple inputs and parse them seperately (multiple dates)

for date in datearray:
	str(date)
	#opening or creating a new file to write results into.
	report = os.path.join(rootdir,str(date))
	topdest = os.path.join(report,topdir)
	#open file to append all information to
	combinedReport = open(topdest + 'fdeny.txt', 'a') 
	#Opening our csv file and setting it to a Reader object
	csvFromLR = csv.reader(open(topdest + '\\' + 'fdeny.csv'))


	#Creating a function to look up Who Is information
	def getIpInfo(ip):
		ip_addr = ip
		#Try catch to complete the IPWhois lookup for each IP, with robust error checking
		try:
			obj = ipwhois.IPWhois(ip_addr)
		except (ASNLookupError, ASNRegistryError, WhoisLookupError,
				HTTPLookupError):
			print("Unable to complete ASN Lookup. \n")
		except ipwhois.exceptions.IPDefinedError:
			theResults = {}
		except ConnectionRefusedError:
			theResults = {}
			print("Connection refused. \n")
		except urllib.error.HTTPError:
			theResults = {}
			print("Error 503, connection refused. \n")
		except HTTPLookupError:
			theResults = {}
			print("Error 404. \n")
		except HTTPError:
			theResults = {}
			print("Error 404. \n")
		except AttributeError:
			theResults = {}
			print("Error 404. \n")
		except IncompleteRead:
			theResults = {}
			print("Incomplete information passed \n")
		except:
			print("Unexpected error occured. \n")
		else:
			theResults = obj.lookup_rdap(depth=1)
		#theResults = obj.lookup_rdap(depth=1)
		getDNS(ip_addr)

		#Index checking for port number, printing port number.
		forPortLookUp = ip_addr
		ipIndex = ips.index(forPortLookUp)
		thePort = ports[ipIndex]
		print('The port number is ' + thePort)
		
		#Try block to pull specific items out of theResults() dictionary and cast to string to write to file and print
		try:
			#First block prints info to terminal
			print (str(ip_addr) + ' is assocated with the following: \n'
			+ 'ASN Country Code: ' + str(theResults['asn_country_code']) + ' \n'
			+ 'Entities ' + str(theResults['entities']) + ' \n'
			+ 'ASN registry: ' + str(theResults['asn_registry']) + '\n'
			+ 'ASN date: ' + str(theResults['asn_date']) + '\n'
			+ 'ASN CIDR: ' + str(theResults['asn_cidr']) + '\n'
			+ 'ASN number: ' + str(theResults['asn'])
			+'\n'
			)
			
			#This block prints to fdeny.txt
			combinedReport.write(str(ip_addr) + ' is assocated with the following: \n'
			+ 'ASN Country Code: ' + str(theResults['asn_country_code']) + ' \n'
			+ 'Entities ' + str(theResults['entities']) + ' \n'
			+ 'ASN registry: ' + str(theResults['asn_registry']) + '\n'
			+ 'ASN date: ' + str(theResults['asn_date']) + '\n'
			+ 'ASN CIDR: ' + str(theResults['asn_cidr']) + '\n'
			+ 'ASN number: ' + str(theResults['asn']) +'\n'
			+ 'Port Number ' + thePort + '\n'
			+ '******************************************************' + '\n\n')
		except KeyError:
			print("This is a private network IP address, unable to populate. \n")
			combinedReport.write((str(ip_addr) + ' is assocated with the following: \n'
			+ "This is a private network IP address, unable to populate. \n")
			+ '******************************************************' + '\n\n')
		except (ASNLookupError, ASNRegistryError, WhoisLookupError,
                    HTTPLookupError):
			print("Unable to complete ASN Lookup. \n")
		except Exception:
			print("Unable to complete ASN Lookup. \n")
		except:
			print("Error Occured. \n")
			combinedReport.write((str(ip_addr) + 'an error occured'))
		
		
		
		
	#Creating a function to look up DNS resolution information
	def getDNS(ip):
		ip_addr = ip
		try:
			#"Convert an IPv4 or IPv6 address in textual form into a Name object whose value is the reverse-map domain name of the address."
			#http://www.dnspython.org/docs/1.14.0/dns.reversename-module.html#from_address
			addr = reversename.from_address(ip_addr)
			resolved = (resolver.query(addr, "PTR")[0])
			print('The IP ' +str(ip_addr)+' resolved to: ' +str(resolved))
		except:
			print('Reverse DNS does not appear to be set up for ' + str(ip_addr))
			
		

	#Reading data into our lists from specefic rows untill all have been stored. 
	for row in csvFromLR:
		ips.append(row[19])
		ports.append(row[21])
		
	#Here we are using 'set' to remove duplicate items and storing them in deDupedIPs.	
	deDupedIPs = set(ips)


	#creating a counter to track how many unique IP's are going to review
	counter1 = 0

	#Looping through all of the de-duped (deDupedIPs) IP address, passing using 'i' then increasing the counter.
	for i in deDupedIPs:
		getIpInfo(i)	
		counter1 +=1

		

	print('The total number of unique IP address was ' + str(counter1))

