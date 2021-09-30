import glob
import os
#Business
file_list = glob.glob(os.path.join(os.getcwd(), "BBC/business", "*.txt"))

businessCorpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        businessCorpus.append(f_input.read().encode('latin-1'))

#Entertainment
file_list = glob.glob(os.path.join(os.getcwd(), "BBC/entertainment", "*.txt"))

entertainmentCorpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        entertainmentCorpus.append(f_input.read().encode('latin-1'))

#Politics
file_list = glob.glob(os.path.join(os.getcwd(), "BBC/politics", "*.txt"))

politicsCorpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        politicsCorpus.append(f_input.read().encode('latin-1'))

#Sport
file_list = glob.glob(os.path.join(os.getcwd(), "BBC/sport", "*.txt"))

sportCorpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        sportCorpus.append(f_input.read().encode('latin-1'))

#Tech
file_list = glob.glob(os.path.join(os.getcwd(), "BBC/tech", "*.txt"))

techCorpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        techCorpus.append(f_input.read().encode('latin-1'))
