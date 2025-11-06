# From QA dataset
    # Compare each question to our question (using BERT or smth idk)
    # Return the answer with the highest similarity
        # index based???
        # Dictionary to map questions to answers
        # Can use csv library as part of Python Standard libs

import csv
import spacy

def similarity_csv(path, query):
    nlp = spacy.load("en_core_web_lg")
    q_s = []
    a_s = []

    with open (path, 'r', encoding ='utf -8 ') as f:
        reader = csv.DictReader(f)
        for i, line in enumerate(reader):
            
            for(k,v) in line.items():

                match k:
                    case 'Question':
                        q_s.append(v)
                    case 'Answer':
                        a_s.append(v)

    # 3. Process the texts with the nlp object
    # This creates a Doc object for each text , which contains the vector.
    # print("\nGenerating embeddings for documents and query ...")
    query_doc = nlp(query)
    document_docs = [nlp(doc) for doc in q_s]

    # 4. Compute and rank similarity
    # Use the built-in .similarity () method on the Doc objects.
    ranked_results = []
    for i, doc in enumerate(document_docs):
        # The .similarity () method calculates the cosine similarity between two Doc vectors
        score = query_doc.similarity(doc)
        ranked_results.append (( q_s[i], a_s[i], score))

        # Sort the results by score in descending order
        ranked_results.sort(key=lambda x: x[2], reverse=True)

    # 5. Display the results

    answers = []
    threshold = 0.97
    top_score = ranked_results[0][2]
    # print(f"Score: {top_score :.4f}\t Document: {doc}")
    
    if(top_score > threshold):
        for doc, ans, score in ranked_results:
            if(score == top_score):
                
                # print(f"Score: {score :.4f}\t Document: {doc}")
                answers.append(ans)
            else:
                break

    return answers

        

    

# print(similarity_csv('../COMP3074-CW1-Dataset.csv','what are stocks and bonds'))
