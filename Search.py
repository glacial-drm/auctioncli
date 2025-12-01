# From QA dataset
    # Compare each question to our question (using BERT or smth idk) | LOL NO DO IT MANUALLY
    # Return the answer with the highest similarity
        # index based???
        # Dictionary to map questions to answers
        # Can use csv library as part of Python Standard libs

import csv
import nltk
from collections import defaultdict
import numpy as np
from scipy import spatial
from os import walk


class Similarity:

    def __init__(self):
        self.__inverted_index = {}
        self.__term_counts = {}
        self.__processed_dictionary = {}
        self.__term_total = 0
        self.__doc_total = 0
    
    def search_cosines(self, query:str, sort_desc:bool): # returns cosine similarities of a query against the calling Similarity object's corpus
        
        query_dict = {
            'query': query
        }

        query_index = self.to_inverted_index(dictionary=query_dict, sparse=True, is_corpus=False) # Map query onto vector space, making a sparse term-document matrix
        
        weighted_query_index = self.TF_IDF_weighting(inverted_index=query_index, is_corpus=False) # Weight the query
        
        query_cosines = self.cosine_similarities(weighted_query_index) # Compute similarities between corpus docs and query
        
        if(sort_desc):
            sorted_similarites = dict(sorted(query_cosines.items(), key=lambda item:item[1], reverse=True)) # REFERENCE ME: ----------------------------------------------------------------

            return sorted_similarites
        
        return query_cosines    

    def cosine_similarities(self, query_inverted_index: dict): # cosine similarity on query with whole document, returns array
        

        # Cosine Similarity # NEED TO ACCOUNT FOR ORDERING
            
            # for each document in inverted index (document count)
                
                # for each term in query

                    # get corresponding term in inverted_index
                        # get count of current document
                    # append to array
                
            # perform cosine similiarity
        
        cosine_similarities = {}
        cos_query = []

        for i in range(self.__doc_total):
            
            doc_counts = []

            for term in query_inverted_index.keys():
            
                if i == 0: # Only add to query array on first iteration
                    cos_query.append(query_inverted_index[term]["query"])
                
                doc_counts.append(self.__inverted_index[term]["doc"+str(i)])
            cos_sim = 1 - spatial.distance.cosine(cos_query, doc_counts)
            cosine_similarities["doc"+str(i)] = cos_sim
        return cosine_similarities

    def TF_IDF_weighting(self, inverted_index: dict, is_corpus: bool):
        
        if(is_corpus):
            inverted_index = self.__inverted_index
        
        for term in inverted_index.items(): # "term" is the token key -> dict of docs containing term
            for doc in term[1].items(): # "doc" is the dict of documents from "term" -> count of terms in the doc | matrix is now sparse, so this is total docs log10(1) = 0 --------------------------------------------------------------------------

                if(doc[1] != 0.0): # If term exists in doc
                    TF = np.log10(1 + doc[1]) # log(1+ freq of term in doc)
                    
                    if(self.__term_counts[term[0]] == 0):
                        IDF = np.log10(self.__doc_total / 1) # log(total docs/docs containing word) | len(term[1].items())
                    else:
                        IDF = np.log10(self.__doc_total / self.__term_counts[term[0]]) # log(total docs/docs containing word) | len(term[1].items())
                    
                    # Tuples are immutable, reassign instead
                    inverted_index[term[0]][doc[0]] = TF * IDF # Stop hallucinating, TF-IDF can be greater than 1
        
        # print(inverted_index["stocks"])
        if(not is_corpus):
            return inverted_index
        
    def to_inverted_index(self, dictionary: dict, sparse:bool, is_corpus:bool):
        
        processed_dictionary = {}
        for doc in dictionary: # for document (key) in dictionary
            processed_dictionary[doc] = self.process_text(dictionary[doc]) # preprocessing
        
        if(is_corpus): # if not corpus then method call is for query
            self.__processed_dictionary = processed_dictionary
        
        # Make inverted index (term-document)
        np.set_printoptions(legacy='1.25') # Remove numpy wrapper (permanent?)
        inverted_index = defaultdict(lambda:defaultdict(int))
        for doc_id, tokens in processed_dictionary.items(): # "doc_id" is the name of the document, "tokens is the list of terms" | Issue of order: terms won't be in the same order for cosine similarity, but terms not in corpus will be accounted for - alternative is iterating on corpus dictionary and checking if term is in current dictionary, preserving order but ignoring terms not in corpus

            for token in tokens: # For all the tokens in a doc
                
                if(sparse and is_corpus):
                    for i in range (0, self.__doc_total): # Instantiate all doc frequencies as 0 (sparse matrix)
                        inverted_index[token]["doc"+str(i)] += 0
                
                inverted_index[token][doc_id] += 1 # Dict ints are init to 0, doesn't mean the other non assigned tokens exist
            
        # print(processed_dictionary.values())
        # print(inverted_index["committees"])
        # print(inverted_index['committees']['doc54'])
        # The resulting index is a dict of dicts. To view it as a standard dict for printing :
        # final_index = {term: dict(postings) for term, postings in inverted_index.items()}

        if(not is_corpus):
            
            if(sparse):
                for doc, terms in self.__processed_dictionary.items():
                    for term in terms:
                        inverted_index[term]['query'] += 0
                
            # print(inverted_index["stocks"])
            
            return inverted_index # return inverted index for query for 

        self.__inverted_index = inverted_index

    def compute_corpus_shape(self, dictionary: dict): # dictionary here is a non inverted index, such as CSV_QA.questions
        
        terms = []
        self.__term_total = 0
        self.__doc_total = 0

        for doc in dictionary.items():
            
            term_list = self.process_text(doc[1])
            self.__doc_total += 1

            for term in term_list:
                
                if term in terms:
                   continue
                
                self.__term_total += 1
                terms.append(term)
                
    def compute_term_counts(self): # Compute word counts of a term-document matrix, return term-count dictionary
        
        counts = defaultdict(int)

        for docs in self.__inverted_index.items():
            for count in docs[1].items():
                if(count[1] > 0):
                    counts[docs[0]] += 1
        
        self.__term_counts = counts

    def process_text(self, document): # Text splitting into list of words, then preprocessing and returning list
        tokens = nltk.word_tokenize(document)
        tokens = [token.lower() for token in tokens]
        # Stemming and lemmatisation?
        # Drop question marks???
        return tokens

class Transaction():
    pass
    # difference is checking for [intent] as a keyword in text? 

class TXT_Intent():
    def __init__(self, folder_path):
        super().__init__()
        
        self.intents = [] # list of intents
        self.intent_corpora = {} # dict that maps intent to dict of corresponding docs (corpus)
        self.intent_similarities = {} # dict that maps intent to Similarity objects

        self.folder_to_dicts_intent(folder_path=folder_path)
        
        obj: Similarity
        for intent, obj in self.intent_similarities.items():

            obj.compute_corpus_shape(dictionary=self.intent_corpora[intent])
            obj.to_inverted_index(dictionary=self.intent_corpora[intent], sparse=True, is_corpus=True)
            obj.compute_term_counts() # Compute term and dictionary counts for TF_IDF weighting
            obj.TF_IDF_weighting(inverted_index={}, is_corpus=True) # Weight the corpus

            # print(obj.__processed_dictionary)
        

    def search_intent(self, query:str):
        intent_scores = {}


        obj: Similarity
        for intent, obj in self.intent_similarities.items(): 

            # Potential threshold checking to avoid always computing against all dicts
                # if greater than threshold then return intent
            # as well as opposite if nothing is found
                # return no-intent/None/[]
                    # implication is that this leads to question-answering
                        # then question answering will return nothing found if not relevant
            
            sorted_similarities = obj.search_cosines(query=query, sort_desc=True)
            x = next(iter(sorted_similarities))
            
            intent_scores[intent] = sorted_similarities[x]
            print(intent, sorted_similarities[x])
        
        best_intent = next(iter(dict(sorted(intent_scores.items(), key=lambda item:item[1], reverse=True))))
        
        # return intent and value (value for three tiered)
        return (best_intent, intent_scores[best_intent])

    def folder_to_dicts_intent(self, folder_path):
        filenames = next(walk(folder_path), (None, None, []))[2]  # [] if no file | https://tinyurl.com/45cwzxw8
        
        for file in filenames:
            intent = file.split('.')[0]
            
            self.intents.append(intent)
            self.intent_corpora[intent] = {}
            self.intent_similarities[intent] = Similarity()

            with open(folder_path+"/"+file, encoding ='utf8 ', errors ='ignore ', mode ='r') as text_data:
                for i, line in enumerate(text_data):
                    self.intent_corpora[intent]['doc'+str(i)] = line.strip()
            
            # print(self.intent_corpora[intent])


class CSV_QA(Similarity):
    # TALK ABOUT DEGRADATION BUG IN REPORT (there was no need to tfidf weight the corpus and compute term counts each search_qa call) -----------------------------------------
    def __init__(self, path):
        super().__init__()
        
        self.__path = path
        self.questions, self.answers = self.csv_to_dict_qa()
        
        self.compute_corpus_shape(dictionary=self.questions)
        self.to_inverted_index(dictionary=self.questions, sparse=True, is_corpus=True)
        self.compute_term_counts() # Compute term and dictionary counts for TF_IDF weighting
        self.TF_IDF_weighting(inverted_index={}, is_corpus=True) # Weight the corpus
    
    def search_qa(self, query:str): #-----------------------------------------------------------------------
        sorted_similarities = self.search_cosines(query=query, sort_desc=True)
        
        # Return similarities
        threshold = 0.97
        query_answers = []
        
        for doc, sim in sorted_similarities.items():
            
            if(threshold > sim):
                break

            query_answers.append(self.answers[doc])
        
        # for ans in query_answers:
        #     print(ans)
        
        return query_answers

    def csv_to_dict_qa(self): # Get questions and answers from document (given there are "Question" and "Answer" headings in csv)
        
        questions = {}
        answers = {}
        with open (self.__path, 'r', encoding ='utf -8 ') as f:
            reader = csv.DictReader(f)

            for i, line in enumerate(reader):
                for(k,v) in line.items():
                    
                    match k:
                        case 'Question':
                            questions["doc"+str(i)] = v
                        case 'Answer':
                            answers["doc"+str(i)] = v
        
        return questions, answers

# d = TXT_Intent(folder_path='./resources/intent-classification')
# print(d.search_intent("what's is my name"))