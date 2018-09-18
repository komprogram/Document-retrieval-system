from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring

directory = "index_dir"

def main():
	query = raw_input("Enter Query  :  ")
	
	#Obtaining handle for Index
	ix = open_dir(directory)
	#Object of Query Parser and Parsing Query
	qp = QueryParser("content", ix.schema)
	q = qp.parse(unicode(query))
	#Searching for querry
	with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
		results = searcher_tfidf.search(q, limit=None)
		print results
		#Checking and Displaying results
		"""
		if len(results)!=0:
			for hit in results:
				print "Title  : ", hit['title']
				print hit.highlights("content")
				print hit['path']
		else:
			print "None matched"
		
		"""	
if __name__=="__main__":
	main()

