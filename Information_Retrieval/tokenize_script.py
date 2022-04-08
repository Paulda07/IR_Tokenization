import sys
import os
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
import time
from collections import Counter 
from collections import defaultdict


#Checking the input arguments and storing them
# =============================================================================
# assert os.path.exists(sys.argv[1]), "I did not find the input directory at, "+str(sys.argv[1])
# assert os.path.exists(sys.argv[1]), "I did not find the output directory at, "+str(sys.argv[2])
# input_directory = sys.argv[1]
# output_directory = sys.argv[2]
# =============================================================================

#Iterating through the files in the input directory and performing tokenization and storing in the output directory
def preprocessing(input_directory, num_of_inputs, temporary_directory = ''):
    
    # Time keeping to count the time taken by the program and to run tokenization on the documents
    # start_time = time.time()   
    fifty_iterations = 0
    total_docs = 0
    docs_containing_token = defaultdict(int)
    all_docs_tokens = []
    doc_lengths = []
    token_frequency = Counter()
    lines = []
    input_filenames = []
    with open('stoplist.txt') as f:
        stopwords = f.read().splitlines() 
        #print(lines)
    for input_filename in os.listdir(input_directory):
        input_filenames.append(input_filename)
        #No of documents in the collection
        total_docs+=1
        input_file = os.path.join(input_directory, input_filename)
        # checking if it is a uncorrupted file
        assert os.path.isfile(input_file), "The files in the input directory are corrupted"
        file_content = open(input_file, errors="ignore").read()
        # print(file_content)
        #Beautiful soup used to extract the text lines from the HTML file
        soup = BeautifulSoup(file_content, "html.parser")
        text = soup.get_text()
        #print(text)
        #Couple of tokenizers used and tested. Wordpunkt chosen because it enables removal of unicode escape sequences
        #tokens = nltk.word_tokenize(text)
        tokens = wordpunct_tokenize(text)
        temp_tokens = tokens
        tokens = []
        for token in temp_tokens:
            # Removing Stopwords
            if token.lower() not in stopwords:  
                tokens.append(token.lower())
        #print (tokens)
        # output_filename = os.path.join(temporary_directory, input_filename[:3]+".txt")
        # output_file = open(output_filename, "w")
        
        #Frequency calculation
        token_frequency.update(tokens)
        #print (token_frequency)

        #Removing escape sequences, words occurring once, words of length 1, punctuations and numbers from the tokens list
        iterator = 0
        while iterator < len(tokens):
            if not tokens[iterator].isalpha() or token_frequency[tokens[iterator]]<=1 or len(tokens[iterator])<=1:
                del token_frequency[tokens[iterator]]
                tokens.pop(iterator)
                continue
            tokens[iterator] = tokens[iterator]
            #Number of times the token occurs in all documents (for idf calc) 
            docs_containing_token[tokens[iterator]]+=1
            iterator +=1

        
        
        #TF calculation terms: frequency of term and size of document
        all_docs_tokens.append(token_frequency)
        doc_lengths.append(len(tokens))

        # #Copying the tokens into output files
        # output_file.writelines("%s\n" % token for token in tokens)
        # output_file.close()
        # # print(token_frequency)

        # if (fifty_iterations%50 == 0):
        #     print("Time Taken by the %s document is --- %s seconds ---" %(fifty_iterations, (time.time() - start_time)))
        # fifty_iterations+=1
        num_of_inputs -= 1
        if (num_of_inputs ==0 ):
            return input_filenames, all_docs_tokens, doc_lengths, total_docs, docs_containing_token
    
    # # vocabulary_path = os.path.join(output_directory, "Vocabulary.txt")
    # # frequency_path = os.path.join(output_directory, "Token_Frequency.txt")
    
    # # a file of all tokens and their frequencies sorted by token
    # with open("Vocabulary.txt", 'w') as f:
    #     for k,v in  sorted(token_frequency.items()):
    #         f.write( "{} {}\n".format(k,v) )
    # f.close()
    
    # # a file of all tokens and their frequencies sorted by frequency
    # with open("Token_Frequency.txt", 'w') as f:
    #     for k,v in  token_frequency.most_common():
    #         f.write( "{} {}\n".format(k,v) )
    # f.close()
    # print("Time Taken by the program--- %s seconds ---" % (time.time() - start_time))    
    
    # Time taken by the program = 14.85 secs
    