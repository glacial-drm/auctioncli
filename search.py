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

    # cosine similarity with search query (for each doc in the collection)
        # map query onto td_matrix, then cosine similarity with each other column (document)
    #for 
    similarity = 1 - spatial.distance.cosine()

    # return list of order docs (decreasing similarity ranking)

def testermweight(diction): # Using countvectorizer
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    all_text = diction.values()

    # add query to corpus beforehand

    count_vect = CountVectorizer(stop_words=stopwords.words("english"))
    X_train_counts = count_vect.fit_transform(all_text)
    # print(X_train_counts.getrow(54))
    # print(X_train_counts[54]) # this is a term count

    tf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    
    # Fit vectorizer to original data
    # Fit vectorizer to query
    # Transform result on fitted transforms 

    # For each column (document-term matrix)
        # get values somehow
        # compute cosine similarity


    print(X_train_tf.shape)
    print(X_train_tf.getrow(54)) # this is a document??? ----------------------

def build_td_matrix(dictionary: dict): # -----------------------------
    from collections import defaultdict
    import numpy as np
    
    processed_dictionary = {}
    for line in dictionary:
        processed_dictionary[line] = process_text(dictionary[line])
    
    inverted_index = defaultdict(lambda:defaultdict(int))
    for doc_id, tokens in processed_dictionary.items():
        for token in tokens:
            inverted_index[token][doc_id] += 1

    

    # The resulting index is a dict of dicts. To view it as a
    # standard dict for printing :
    final_index = {term: dict(postings) for term, postings in inverted_index.items()}

    print(processed_dictionary["doc54"])
    print(final_index['committees'])

    # Apply term weighting somehow ------------------------------------
        # without using countvectorizer???
        # or get inverted index in form of count vectorizer?
            # TF-IDF formula implies weighting terms within the document
            # we access documents column by column in td matrix
                # how?
    
    # TF-IDF = log(1+ freq of term in doc)*log(total docs/docs containing word)
    # for docs in inverted_index.items():
    #     for term in docs:
    #         print(term.items())
    #     doc = np.log10(1 + doc) * np.log10( inverted_index.len() / docs.len())

    # final_index2 = {term: dict(postings) for term, postings in inverted_index.items()}
    # print(final_index2['committees'])
        



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
# testermweight(questions)
build_td_matrix(dictionary=questions)