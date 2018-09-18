import os
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
from whoosh.index import create_in

def main():
	create_index()

#Function Defining Schema for Indexing File
def define_schema():
	print ("Schema Definition")
	return Schema(path=ID(stored=True),
				  title=TEXT(stored=True),  
				  content=TEXT(stored=True, analyzer=StemmingAnalyzer()))
	
#function to get document's path
def doc_path():
	base_dir = os.path.abspath('.') + '/' + 'dataset2/'
	docs = []
	print ("directory ---> %s"%(base_dir))
	for d in os.listdir(base_dir):
				docs.append(base_dir + d)
	return docs
	
	
#Function to read the content of the documents	
def read_content(path):
	try:
		f_obj = open(path, 'r+')
		#print ("%s opened"%path)
		content=f_obj.read()
		#print ("%s read"%path)
		f_obj.close()
	except IOError:
		print ('Unable to read %s file'%(path))

	return content
	
#Function to read the title of the page
def read_title(path):
	try:
		f_obj = open(path, 'r+')
		#print ("%s opened"%path)
		string=f_obj.readline()
		title = ""
		for s in string:
			if s=='&' or s=='l' or s=='t' or s==';' or s=='>':
                                #Do nothing
                                s=""
			else:
				title = title+s
                print ("Title : %s"%title)
		f_obj.close()
	except IOError:
		print ('Unable to read %s file'%(path))
		
	return title

#Funtion to add document to index.writer	
def add_doc(writer, path, title, content):
	print ("document adding")
	writer.add_document(path=unicode(path), title=unicode(title, "utf-8"), content=unicode(content, "utf-8"))
   	#print ("%s added"%title)

#Function to Create Index
def create_index():
	#Creating Index Direcory, if it does not exist
	if not os.path.exists("index_dir2"):
		os.mkdir("index_dir")
		print ("index_dir CREATED")
		
		
		#Schema Definition
		schema = define_schema()
		print ("Schema Defined")
	
		#Creating Index Object
		ix = create_in("index_dir", schema)
		print ("Index Created")	

		#Creating writer to add documents to index object
		writer = ix.writer()
		print ("Writer Created")
		count=0
		#Fetching Path
		#Reading Content
		#Reading Title
		#adding to the index.writer
		paths = doc_path()
		for path in paths:
			content=read_content(path)
			title=read_title(path)
			#print ("ad_doc called")
			add_doc(writer, path, title, content)
                        #print (content)
			count += 1
			print (count)
                        
		writer.commit()
		print ("Writer Commited")
	else:
		print ("index_dir already exist")

if __name__=="__main__":
	main()
