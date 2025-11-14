import os
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix

import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import cross_val_score,StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
# NEXT STEPS -------------------------------------------
    # GATHER DATA
    # IMPLEMENT CROSS VALIDATION/BOOTSTRAPPING

class Intent_Classifier:
    def __init__(self):
        # import all data first
        self.__label_dir = {
            "greeting": "./intent-classification/greeting.txt",
            # "small-talk": "",
            # "discoverability": "./intent-classification/discoverability.txt", # BAD
            "name-calling": "./intent-classification/name-calling.txt", # identity management
            "question-greeting": "./intent-classification/question-greeting.txt", # BAD
            # "transaction": ""
                # split into sub transactions, using keyword
                # regex keyword to effectively create a given keyword
            
            "help": "./intent-classification/help.txt",
            "exit": "./intent-classification/exit.txt",
            
            "yes": "./intent-classification/yes.txt",
            "no": "./intent-classification/no.txt",
            # maybe???
            # thank you???
            # still there???
            # repeat???
            # name asking???
            # time telling
            
            "question-answering": "./intent-classification/question-answering.txt" # Issues here apparently --------------------------
                # Question answering should be catch all (default case), then if no response, reply with not understood
                # Impossible as we always predict something

        }
        

        self.__data = []
        self.__labels = []
        for label, filepath in self.__label_dir.items() :
            
            with open(filepath, encoding ='utf8 ', errors ='ignore ', mode ='r') as review:
                for line in review:
                    self.__data.append(line.strip())
                    self.__labels.append(label)

        self.__count_vect = CountVectorizer(stop_words = stopwords.words ('english'))
        self.__tfidf_transformer = TfidfTransformer(use_idf = True, sublinear_tf = True)
        self.__log_reg_clf = LogisticRegression(random_state =0)
    
    def build_log_reg_clf(self):
        X_train, X_test, y_train, y_test = train_test_split(self.__data, self.__labels, stratify = self.__labels, test_size =0.25, random_state =42)

        print(y_train)
        X_train_counts = self.__count_vect.fit_transform(X_train)

        self.__tfidf_transformer.fit(X_train_counts)
        X_train_tf = self.__tfidf_transformer.transform(X_train_counts)

        self.__log_reg_clf.fit(X_train_tf,y_train)

        X_new_counts = self.__count_vect.transform(X_test)
        X_new_tfidf = self.__tfidf_transformer.transform(X_new_counts)

        predicted = self.__log_reg_clf.predict(X_new_tfidf)

        print(confusion_matrix(y_test,predicted))
        print(accuracy_score(y_test,predicted))
        # print(f1_score(y_test,predicted,pos_label ='positive'))
        # Export Model

    def build_k_fold(self):
        kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        # Define classifiers to evaluate
        classifiers = {
        " Multinomial Naive Bayes ": MultinomialNB () ,
        " Support Vector Machine ": SVC () ,
        " Random Forest ": RandomForestClassifier ()
        }

        # Define the ( stratified ) k- fold cross - validation (k =10)
        kfold = StratifiedKFold ( n_splits =10,shuffle = True,random_state =42)

        # Iterate over classifiers
        for name,classifier in classifiers.items () :
            pipeline = make_pipeline ( TfidfVectorizer ( stop_words ='english'),classifier )
            scores = cross_val_score ( pipeline,self.__data,self.__labels,cv = kfold,scoring ='accuracy')
            print (f"{ name }:")
            print (" Cross - validation scores :", scores )
            print (" Average accuracy :", np.mean ( scores ))
            print ()        

    def classify_text(self, text:str):
        processed_newdata = self.__count_vect.transform([text])
        processed_newdata = self.__tfidf_transformer.transform(processed_newdata)
        
        return self.__log_reg_clf.predict(processed_newdata)[0]
    
    def export_model(self):
        from joblib import dump
        dump(self.__log_reg_clf, "../objects/log_reg_clf.joblib")

d = Intent_Classifier()
# d.build_log_reg_clf()
#  print(d.classify_text("nuh uh"))

d.build_k_fold()