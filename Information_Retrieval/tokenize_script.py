import sys
import os
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize

    
assert os.path.exists(sys.argv[1]), "I did not find the input directory at, "+str(sys.argv[1])
assert os.path.exists(sys.argv[1]), "I did not find the output directory at, "+str(sys.argv[2])

input_directory = sys.argv[1]
output_directory = sys.argv[2]
for input_filename in os.listdir(input_directory):
    input_file = os.path.join(input_directory, input_filename)
    # checking if it is a file
    assert os.path.isfile(input_file), "The files in the input directory are corrupted"
    file_content = open(input_file).read()
    # print(file_content)
    soup = BeautifulSoup(file_content)
    text = soup.get_text()
    print(text)
    # tokens = nltk.word_tokenize(text)
    tokens = wordpunct_tokenize(text)
    print (tokens)
    output_filename = os.path.join(output_directory, input_filename[:3]+".txt")
    output_file = open(output_filename, "w")
    output_file.writelines("%s\n" % token for token in tokens)
    output_file.close()
