import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn import svm
from sklearn.metrics import f1_score
import sklearn.datasets
import glob

def main():
    print("Reading Content from the Training documents....")
    content = readContent('train_new/')

    y = content.target

    #Vectorizing Training Documents
    X_train = tfidNEla(content)

    #FeatureSelection TrainData
    X_train = chi2FS(X_train, y)

    #BuildClassifier
    clf = buildSVMClassifier(X_train, y)

    print("Reading Content from the Test documents, Vectorizing & FeatureSelection....")
    test_content = content = readContent('test_new/')
    fo = open("beforeClassification.txt","w+")
    for c, i in zip(test_content.filenames, test_content.target):
        st = str(c) +"--->"+ str(i) + "\n"
        fo.write(st)
    fo.close()
    #Vectorizing Test Documents
    X_test = tfidNEla(content)
    #FeatureSelection TrainData
    X_test = chi2FS(X_test, test_content.target)
    #Test Classifier
    y_predicted = clf.predict(X_train)
    test_predicted = clf.predict(X_test)
    fo = open("afterClassification.txt","w+")
    for c, i in zip(test_content.filenames, test_predicted):
        st = str(c) +"--->"+ str(i) + "\n"
        fo.write(st)
    fo.close()

    #F1-Score
    calculateF1Score(y, y_predicted)

#function copies the content of directory into a list
def readContent(dirName):
    base_dir = os.path.abspath('.') + '/' + dirName
    docs = glob.glob(base_dir)
    docs = docs[0]
    content = sklearn.datasets.load_files(docs)
    return (content)

def tfidNEla(content):
    print("Creatinng TF_IDF Vectorizer")
    vector = TfidfVectorizer(sublinear_tf=True, stop_words='english', norm=u'l2').fit(content.data)
    print("Transforming Document into Matrix Using TF_IDF Vectorizer & Implementing ELA....")
    #vect.transform(train) uses the fitted vocabulary to build a document-term matrix from the training data
    X=vector.transform(content.data)
    X_Array = X.toarray()
    features = vector.get_feature_names()
    print("Total Number of Features : %d",len(features))
    return X_Array

def chi2FS(X, y):
    print("Implementing Chi2....")
    print("Selecting top 1000 features....")
    ch2 = SelectKBest(chi2, k=1000)
    x_new = ch2.fit(X, y).transform(X)
    return x_new

def buildSVMClassifier(X, y):
    print("Building Classifier....")
    #clf = svm.SVC(kernel='linear')
    #clf = svm.SVC()
    clf = svm.LinearSVC()
    print("Training Classifier....")
    clf.fit(X, y)
    return clf

def calculateF1Score(y, y_predicted):
    #Performing F1 Test
    print("Calculating F1-Score....")
    f1_macro = f1_score(y, y_predicted, average='macro')
    print ("F1-SCORE MACRO  ----> "+str(f1_macro))
    f1_micro = f1_score(y, y_predicted, average='micro')
    print ("F1-SCORE MICRO  ----> "+str(f1_micro))

if __name__ == '__main__':
    main()
