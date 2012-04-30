#!/usr/bin/env python
import time
import string
import httplib,sys
from socket import *
import re
import getopt

print "\n*************************************"
print "*TheHarvester Ver. 1.1              *"
print "*Coded by laramies                  *"
print "*Edge-Security Research             *"
print "*cmartorella@edge-security.com      *"
print "*************************************\n\n"

global word
global w
global result
result =[]

def usage():
 print "TheHarvester 1.0\n"
 print "usage: theharvester options \n"
 print "       -d: domain to search\n"
 print "       -l: limit the number of results to work with(msn goes from 50 to 50 results and google 100 to 100)\n"
 print "       -b: search engine(google,msn)\n"
 print "example:./theharvester.py -d microsoft.com -l 500 -b google\n" 
 sys.exit()

def howmanymsn(w):
	h = httplib.HTTP('search.msn.com')
	h.putrequest('GET',"/results.aspx?q=%40"+w+"&FORM=QBHP")
	h.putheader('Host', 'search.msn.com')
	h.putheader('User-agent', 'Internet Explorer 6.0 ')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data=h.getfile().read()
	r1 = re.compile('of [0123456789,]* results')
	result = r1.findall(data)
	for x in result:
		clean = re.sub('of','',x)
		clean = re.sub('results','',clean)
		clean = re.sub(',','',clean)
	return clean

def howmanygoogle(w):
         h = httplib.HTTP('www.google.com')
         h.putrequest('GET',"/search?num=10&hl=en&btnG=B%C3%BAsqueda+en+Google&meta=&q=%40"+w)
         h.putheader('Host', 'www.google.com')
         h.putheader('User-agent', 'Internet Explorer 6.0 ')
         h.endheaders()
         returncode, returnmsg, headers = h.getreply()
         data=h.getfile().read()
         r1 = re.compile('about <b>[0123456789,]*</b> for')
         result = r1.findall(data)
         for x in result:
                clean = re.sub(' <b>','',x)
                clean = re.sub('</b> ','',clean)
                clean = re.sub('about','',clean)
                clean = re.sub('for','',clean)
                clean = re.sub(',','',clean)
         return clean

def run(w,i,eng):
	if eng=="msn":
		h = httplib.HTTP('search.msn.com')
		h.putrequest('GET',"/results.aspx?q=%40"+w+"&FORM=QBHP&first="+str(i))
		h.putheader('Host', 'search.msn.com')
		h.putheader('Cookie','SRCHUID=V=1&NRSLT=50;')
	elif eng=="google":
		h = httplib.HTTP('www.google.com')
		h.putrequest('GET',"/search?num=100&start="+str(i)+"&hl=es&btnG=B%C3%BAsqueda+en+Google&meta=&q=%40\""+w+"\"")
		h.putheader('Host', 'www.google.com')
	h.putheader('User-agent', 'Internet Explorer 6.0 ')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data=h.getfile().read()
	if eng=="msn":
 		data=string.replace(data,'<strong>','')
 		data=string.replace(data,'</strong>','')
	else:
		data=re.sub('<b>','',data)
    	for e in ('>',':','=','<','/','\\',';'):
		data = string.replace(data,e,' ')	
	r1 = re.compile('[a-zA-Z0-9.-_]*'+'@'+w)	
	res = r1.findall(data) 
	return res 

def test(argv):
	global limit
	limit = 100
	if len(sys.argv) < 2: 
		usage() 
	try :
	       opts, args = getopt.getopt(argv,"l:d:b:")
 
	except getopt.GetoptError:
  	     	usage()
		sys.exit()
	
	for opt,arg in opts :
       		if opt == '-l' :
       			limit=int(arg)
    	   	elif opt == '-d' :
			word=arg
		elif opt == '-b':
			engine=arg
	
	print "Searching for "+word+" in "+ engine
	print "========================================"
	if engine=="msn":
		total = int(howmanymsn(word))
	elif engine=="google":
		total = int(howmanygoogle(word))
	
	print "Total results: ",total
	cant = 0
	if total < limit:
 			limit=total
	print "Limit: ",limit	
	while cant < limit:
		print "Searching results: " + str(cant) +"\r"
		res = run(word,cant,engine)
		for x in res:
	                if result.count(x) == 0:
               		        result.append(x)
		if engine =='google':
			cant+=100
		elif engine =='msn':
			cant+=50	

	print "\nAccounts found:"
	print "====================\n"
	t=0
	if result==[]:
		print "No results were found"
	else:
		for x in result:
			x= re.sub('<li class="first">','',x)
			x= re.sub('</li>','',x)
			print x
			t+=1
	print "====================\n"
	print "Total results: ",t
	
if __name__ == "__main__":
        try: test(sys.argv[1:])
	except KeyboardInterrupt:
		print "Search interrupted by user.."
	except:
		sys.exit()


