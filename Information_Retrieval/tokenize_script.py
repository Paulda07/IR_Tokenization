import sys
import os
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
import time
from collections import Counter 

# Time keeping to count the time taken by the program and to run tokenization on the documents
start_time = time.time()   

#Checking the input arguments and storing them
assert os.path.exists(sys.argv[1]), "I did not find the input directory at, "+str(sys.argv[1])
assert os.path.exists(sys.argv[1]), "I did not find the output directory at, "+str(sys.argv[2])
input_directory = sys.argv[1]
output_directory = sys.argv[2]

#Iterating through the files in the input directory and performing tokenization and storing in the output directory
fifty_iterations = 0
token_frequency = Counter()
for input_filename in os.listdir(input_directory):
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
    #print (tokens[52])
    output_filename = os.path.join(output_directory, input_filename[:3]+".txt")
    output_file = open(output_filename, "w")
    
    #Removing escape sequences, punctuations and numbers from the tokens list
    iterator = 0
    while iterator < len(tokens):
        if not tokens[iterator].isalpha():
            tokens.pop(iterator)
            continue
        tokens[iterator] = tokens[iterator].lower()
        iterator +=1
    
    #Copying the tokens into output files
    output_file.writelines("%s\n" % token for token in tokens)
    #Frequency calculation
    token_frequency.update(tokens)
    output_file.close()
    if (fifty_iterations%50 == 0):
        print("Time Taken by the %s document is --- %s seconds ---" %(fifty_iterations, (time.time() - start_time)))
    fifty_iterations+=1
# print(token_frequency)

# vocabulary_path = os.path.join(output_directory, "Vocabulary.txt")
# frequency_path = os.path.join(output_directory, "Token_Frequency.txt")

# a file of all tokens and their frequencies sorted by token
with open("Vocabulary.txt", 'w') as f:
    for k,v in  sorted(token_frequency.items()):
        f.write( "{} {}\n".format(k,v) )
f.close()

# a file of all tokens and their frequencies sorted by frequency
with open("Token_Frequency.txt", 'w') as f:
    for k,v in  token_frequency.most_common():
        f.write( "{} {}\n".format(k,v) )
f.close()
print("Time Taken by the program--- %s seconds ---" % (time.time() - start_time))    

# Time taken by the program = 14.85 secs