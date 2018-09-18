#!/Python27/python
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring

directory = "index_dir"
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
query = form.getvalue('query')
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
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
with ix.searcher(weighting=scoring.BM25F()) as searcher_bm25f:
	results = searcher_bm25f.search(q, limit=None)
		#Checking and Displaying results
	#count=1
	print "Showing %d Results."%(len(results))
	if len(results)!=0:	
		for hit in results:
			print "<br><br>"
			#print "%d" %(count)
			#count=count+1
			url = hit['path']
			s2 = "htdocs\\"
			url = url[url.index(s2) + len(s2):]
			print "<b>"
			print "<a href=\"http://172.16.116.49/%s\" target=\"_blank\">%s</a>" % (url, hit['title'])
			print "</b>"
			print "<br><a href=\"http://172.16.116.49/%s\" target=\"_blank\">%s</a>" % (url, url)
			print "<br>"
			print hit.highlights('content')
			print "<hr>"
			
	else:
		print "<h4>No matching Document.</h4>"
		print "<br>"

print "</body>"
print "</html>"
#if __name__=="__main__":
#	main()

