# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:08:07 2022

@author: Paul Ledala
"""

import sys
import os
import math
import time
import tokenize_script 
from matplotlib import pyplot as plt
from collections import defaultdict
#Calculating the time taken by the program
start_time = time.time() 
#Taking the input and output directory paths from the command line and setting the paths
assert os.path.exists(sys.argv[1]), "I did not find the input directory at, "+str(sys.argv[1])
assert os.path.exists(sys.argv[1]), "I did not find the output directory at, "+str(sys.argv[2])
input_directory = sys.argv[1]
output_directory = sys.argv[2]

#No. of documents to be term weighted and indexed
inputs_taken = [10, 20, 40, 80, 100, 200, 300, 400, 500]
time_taken = [0]
# print(input_directory)
for i in inputs_taken:
    #Getting the data from preprocessed file in terms of term frequency, document size, no of documents and no of docs with the term
    input_filenames, all_docs_tokens, doc_lengths, total_docs, docs_containing_token = tokenize_script.preprocessing(input_directory, i)

    iterator = 0
    while (iterator < len(input_filenames)):
        term_weights = defaultdict(float)
        for token, value in all_docs_tokens[iterator].items():
            #Calculating the tf and idf terms using the tf-idf formula taking the data from preprocessing
            tf = value / doc_lengths[iterator]
            idf = math.log(total_docs/docs_containing_token[token])
            # print(total_docs)
            # print(total_docs/docs_containing_token[token], tf, idf)
            #Calculating the term weights
            term_weights[token] = tf * idf
        #Writing the weighted terms to the output files
        output_filename = os.path.join(output_directory, input_filenames[iterator][:3]+".txt")
        with open(output_filename, 'w') as f:
            for k,v in  sorted(term_weights.items()):
                f.write( "{} {}\n".format(k,v) )
        f.close()    
        iterator += 1

    #Plotting the indexing time 
    time_taken.append(time.time()-start_time-time_taken[-1])
print(time_taken)
plt.plot(inputs_taken, time_taken[1:])
plt.title("Indexing Time")
plt.xlabel("Number of Documents Indexed")
plt.ylabel("Time Taken (in sec)")
plt.show()