import os
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score , f1_score , confusion_matrix

# NEXT STEPS -------------------------------------------
    # GATHER DATA
    # IMPLEMENT CROSS VALIDATION/BOOTSTRAPPING

# import all data first
label_dir = {
    "greeting": "./intent-classification/greeting.txt",
    # "small-talk": "",
    "discoverability": "./intent-classification/discoverability.txt",
    "name-calling": "./intent-classification/name-calling.txt",
    "question-greeting": "./intent-classification/question-greeting.txt",
    "question-answering": "./intent-classification/question-answering.txt",
    # "transaction": ""
        # split into sub transactions, using keyword
        # regex keyword to effectively create a given keyword
    
    "help": "./intent-classification/help.txt",
    "exit": "./intent-classification/exit.txt",
    
    "yes": "./intent-classification/yes.txt",
    "no": "./intent-classification/no.txt"
    # maybe???
    # thank you???
    # still there???
    # repeat???
    # name asking???
    # time telling
}
data = []
labels = []

for label, filepath in label_dir.items() :
    
    with open(filepath, encoding ='utf8 ', errors ='ignore ', mode ='r') as review:
        for line in review:
            data.append(line.strip())
            labels.append(label)

X_train, X_test, y_train, y_test = train_test_split(data, labels, stratify = labels, test_size =0.25, random_state =42)

print(y_train)
count_vect = CountVectorizer(stop_words = stopwords.words ('english'))
X_train_counts = count_vect.fit_transform(X_train)

tfidf_transformer = TfidfTransformer(use_idf = True, sublinear_tf = True).fit (
X_train_counts)
X_train_tf = tfidf_transformer.transform(X_train_counts)

clf = LogisticRegression(random_state =0).fit(X_train_tf , y_train)

X_new_counts = count_vect.transform(X_test)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

print(confusion_matrix(y_test , predicted))
print(accuracy_score(y_test , predicted))
# print(f1_score(y_test , predicted , pos_label ='positive'))
# Export Model

new_data = "nuh uh"
def classify_text(classifier:LogisticRegression, text:str):
    processed_newdata = count_vect.transform([text])
    processed_newdata = tfidf_transformer.transform(processed_newdata)
    
    return(classifier.predict(processed_newdata))

print(classify_text(clf, new_data))

from joblib import dump
dump(clf, "../objects/log_reg_clf.joblib")