#!/Python27/python
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
import os

directory = "index_dir"
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
query = form.getvalue('class')
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"



#query = raw_input("Enter Query  :  ")
	
	#Obtaining handle for Index
ix = open_dir(directory)
	#Object of Query Parser and Parsing Query
qp = QueryParser("content", ix.schema)
q = qp.parse(unicode(query))
	#Searching for querry
	#with ix.searcher() as searcher_tfidf:
with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
	results = searcher_tfidf.search(q, limit=None)
		#Checking and Displaying results
	#count=1
	print "Showing %d Results.\n"%(len(results))
	if len(results)!= 0:
		for hit in results:
			print "<br><br>"
			#print "%d" %(count)
			#count=count+1
			url = hit['path']
			s2 = "htdocs\\"
			url = url[url.index(s2) + len(s2):]
			print "<b>"
			print "<a href=\"http://172.16.116.49/%s\" target=\"_blank\">%s</a>" % (url, hit['title'])
			t = hit['title']
			tt = len(t)
			print "</b>"
			print "<br><a href=\"http://172.16.116.49/%s\" target=\"_blank\">%s</a>" % (url, url)
			#print '<a href="%s">%s</a>' % (hit['path'].encode('UTF-8','replace'), "Link")
			print "<br>"
			print hit.highlights("content")
			print "<hr>"
			
		
	else:
		print "<h4>No matching Results.</h4>"
		print "<br>"
		
#if __name__=="__main__":
#	main()

print "</body>"
print "</html>"