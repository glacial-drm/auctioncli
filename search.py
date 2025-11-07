# From QA dataset
    # Compare each question to our question (using BERT or smth idk)
    # Return the answer with the highest similarity
        # index based???
        # Dictionary to map questions to answers
        # Can use csv library as part of Python Standard libs

import csv
import nltk
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def output_answer(sorted_similarity, ans_dict):
    pass
    # # 5. Display the results

    # answers = []
    # threshold = 0.97
    # top_score = ranked_results[0][2]
    # # print(f"Score: {top_score :.4f}\t Document: {doc}")
    
    # if(top_score > threshold):
    #     for doc, ans, score in ranked_results:
    #         if(score == top_score):
                
    #             # print(f"Score: {score :.4f}\t Document: {doc}")
    #             answers.append(ans)
    #         else:
    #             break

    # return answers

def search_qa(query, td_matrix): #----------------------------
    from scipy import spatial
    


    # Map search query on the document collection-induced vector space
        # make it a document term matrix (fixed size vector)
    processed_query = process_text(query)

    # Apply term weighting to the query

    # 5.3.1, compute the intersection of all the words in our 
    #for 
    similarity = 1 - spatial.distance.cosine()

    # return list of order docs

def testermweight(diction): # Using countvectorizer
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    all_text = diction.values()
    count_vect = CountVectorizer ( stop_words = stopwords . words("english"))
    X_train_counts = count_vect . fit_transform(all_text)
    # print(X_train_counts[21])
    
    # sparsely populated matrix, rather not use ----------------------
    # however, seemingly only way to apply weighting needs this?
    
    tf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(    X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    print(X_train_tf.getcol(0))

def build_td_matrix(dictionary: dict): # -----------------------------
    from collections import defaultdict
    
    processed_dictionary = {}
    for line in dictionary:
        processed_dictionary[line] = process_text(dictionary[line])
    
    inverted_index = defaultdict(lambda:defaultdict(int))
    for doc_id, tokens in processed_dictionary.items():
        for token in tokens:
            inverted_index[token][doc_id] += 1

    print(processed_dictionary["doc0"])

    # The resulting index is a dict of dicts. To view it as a
    # standard dict for printing :
    final_index = {term: dict(postings) for term, postings in inverted_index.items()}
    # print(final_index['economic'])

    # Apply term weighting somehow ------------------------------------
        # without using countvectorizer???
        # or get inverted index in form of count vectorizer?
            # TF-IDF formula implies weighting terms within the document

def process_text(document): # Method Description
    tokens = nltk.word_tokenize(document)
    # Stemming and lemmatisation?
    # forcing lower case?
    # Drop question marks???
    return tokens

def csv_to_dict(path):
    questions = {}
    answers = {}

    # Get questions and answers from document (given there are "Question" and "Answer" headings)
    with open (path, 'r', encoding ='utf -8 ') as f:
        reader = csv.DictReader(f)

        for i, line in enumerate(reader):
            for(k,v) in line.items():
                
                match k:
                    case 'Question':
                        questions["doc"+str(i)] = v
                    case 'Answer':
                        answers["doc"+str(i)] = v


    return questions, answers

questions, answers = csv_to_dict(path='../COMP3074-CW1-Dataset.csv')
testermweight(questions)
build_td_matrix(dictionary=questions)