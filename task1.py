import matplotlib.pyplot as plt
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np
import math

names = ['Business', 'Entertainment', 'Politics','Sport','Tech']
counts = {}

values = [510, 417, 417,511,401]

plt.bar(names, values)
plt.suptitle('Instance of each class')
plt.ylabel('Number of instances')
plt.xlabel('Class names')
plt.savefig("BBC-distribution.pdf")
plt.show()
# 3)
corpus = load_files('BBC', load_content=True, encoding='latin-1')
X_data, y = corpus.data, corpus.target

# 4)
vectorizer = CountVectorizer(encoding='latin-1')
X_vectorized = vectorizer.fit_transform(X_data)
X = X_vectorized.toarray()
dictionary = vectorizer.get_feature_names_out()

# 5)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=None)

# 6)
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 7)
y_pred = clf.predict(X_test)
with open("bbc-performance.txt",'a') as file:
    file.write('**************MultinomialNB default values, try 1**************\n')
    file.write(str(confusion_matrix(y_test, y_pred))+'\n')
    file.write(str(classification_report(y_test, y_pred, target_names=corpus.target_names))+'\n')
    file.write("Accuracy = "+str(accuracy_score(y_test, y_pred))+'\n')
    file.write("F1 score (macro) = "+str(f1_score(y_test, y_pred, average='macro'))+'\n')
    file.write("F1 score (weighted) = "+str(f1_score(y_test, y_pred, average='weighted'))+'\n')
    file.write('Prior probability\n')
    file.write('P(Business) = 1/5\n'
          'P(Entertainment) = 1/5\n'
          'P(Politics) = 1/5\n'
          'P(Sport) =  1/5\n'
          'P(Tech) = 1/5\n')
    file.write("Vocabulary size = "+str(dictionary.size) +'\n')

sumCountCorpus = clf.feature_count_
idx=0
for sumClass in sumCountCorpus:
    sum = np.sum(sumClass)
    with open("bbc-performance.txt",'a') as file:
        file.write(corpus.target_names[idx]+" class word-token count ="+str(sum)+'\n')
    idx+=1

sumCorpus = np.sum(sumCountCorpus)
with open("bbc-performance.txt",'a') as file:
    file.write("Corpus word-token count = "+str(sumCorpus)+'\n')

idx=0
for sumClass in sumCountCorpus:
    with open("bbc-performance.txt",'a') as file:
        file.write("Number of word with 0 frequency in "+corpus.target_names[idx]+" = "+str(np.count_nonzero(sumClass==0))+"\n")
        file.write("Percentage of word with 0 frequency in "+corpus.target_names[idx]+" = "+str(100*np.count_nonzero(sumClass==0)/dictionary.size)+" %\n")

with open("bbc-performance.txt", 'a') as file:
    file.write("Number of word with 1 frequency in the whole corpus = " + str(np.count_nonzero(sumClass == 1)) + "\n")
    file.write("Percentage of word with 1 frequency in the whole corpus" + str(100 * np.count_nonzero(sumClass==1)/dictionary.size) + " %\n")

index1 = np.where(dictionary == 'bought')[0]
index2 = np.where(dictionary == 'oil')[0]
sum1 = 0
sum2 = 0
for sumClass in sumCountCorpus:
    sum1 += sumClass[index1]
    sum2 += sumClass[index2]
logProb1 = math.log(sum1/sumCorpus)
logProb2 = math.log(sum2/sumCorpus)
with open("bbc-performance.txt",'a') as file:
    file.write("Log-prob of the word 'bought' = "+str(logProb1)+"\n")
    file.write("Log-prob of the word 'oil' = "+str(logProb2)+"\n")

# 8)
clf = MultinomialNB()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
with open("bbc-performance.txt",'a') as file:
    file.write('\n**************MultinomialNB default values, try 2**************\n')
    file.write(str(confusion_matrix(y_test, y_pred)) + '\n')
    file.write(str(classification_report(y_test, y_pred, target_names=corpus.target_names)) + '\n')
    file.write("Accuracy = " + str(accuracy_score(y_test, y_pred)) + '\n')
    file.write("F1 score (macro) = " + str(f1_score(y_test, y_pred, average='macro')) + '\n')
    file.write("F1 score (weighted) = " + str(f1_score(y_test, y_pred, average='weighted')) + '\n')
    file.write('Prior probability\n')
    file.write('P(Business) = 1/5\n'
               'P(Entertainment) = 1/5\n'
               'P(Politics) = 1/5\n'
               'P(Sport) =  1/5\n'
               'P(Tech) = 1/5\n')
    file.write("Vocabulary size = " + str(dictionary.size) + '\n')

sumCountCorpus = clf.feature_count_
idx = 0
for sumClass in sumCountCorpus:
    sum = np.sum(sumClass)
    with open("bbc-performance.txt", 'a') as file:
        file.write(corpus.target_names[idx] + " class word-token count =" + str(sum) + '\n')
    idx += 1

sumCorpus = np.sum(sumCountCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Corpus word-token count = " + str(sumCorpus) + '\n')

idx = 0
for sumClass in sumCountCorpus:
    with open("bbc-performance.txt", 'a') as file:
        file.write("Number of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            np.count_nonzero(sumClass == 0)) + "\n")
        file.write("Percentage of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            100 * np.count_nonzero(sumClass == 0) / dictionary.size) + " %\n")

with open("bbc-performance.txt", 'a') as file:
    file.write("Number of word with 1 frequency in the whole corpus = " + str(np.count_nonzero(sumClass == 1)) + "\n")
    file.write("Percentage of word with 1 frequency in the whole corpus" + str(
        100 * np.count_nonzero(sumClass == 1) / dictionary.size) + " %\n")

index1 = np.where(dictionary == 'bought')[0]
index2 = np.where(dictionary == 'oil')[0]
sum1 = 0
sum2 = 0
for sumClass in sumCountCorpus:
    sum1 += sumClass[index1]
    sum2 += sumClass[index2]
logProb1 = math.log(sum1 / sumCorpus)
logProb2 = math.log(sum2 / sumCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Log-prob of the word 'bought' = " + str(logProb1) + "\n")
    file.write("Log-prob of the word 'oil' = " + str(logProb2) + "\n")

# 9)
clf = MultinomialNB(alpha=0.0001)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
with open("bbc-performance.txt",'a') as file:
    file.write('\n**************MultinomialNB smoothing value of 0.0001, try 3**************\n')
    file.write(str(confusion_matrix(y_test, y_pred)) + '\n')
    file.write(str(classification_report(y_test, y_pred, target_names=corpus.target_names)) + '\n')
    file.write("Accuracy = " + str(accuracy_score(y_test, y_pred)) + '\n')
    file.write("F1 score (macro) = " + str(f1_score(y_test, y_pred, average='macro')) + '\n')
    file.write("F1 score (weighted) = " + str(f1_score(y_test, y_pred, average='weighted')) + '\n')
    file.write('Prior probability\n')
    file.write('P(Business) = 1/5\n'
               'P(Entertainment) = 1/5\n'
               'P(Politics) = 1/5\n'
               'P(Sport) =  1/5\n'
               'P(Tech) = 1/5\n')
    file.write("Vocabulary size = " + str(dictionary.size) + '\n')

sumCountCorpus = clf.feature_count_
idx = 0
for sumClass in sumCountCorpus:
    sum = np.sum(sumClass)
    with open("bbc-performance.txt", 'a') as file:
        file.write(corpus.target_names[idx] + " class word-token count =" + str(sum) + '\n')
    idx += 1

sumCorpus = np.sum(sumCountCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Corpus word-token count = " + str(sumCorpus) + '\n')

idx = 0
for sumClass in sumCountCorpus:
    with open("bbc-performance.txt", 'a') as file:
        file.write("Number of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            np.count_nonzero(sumClass == 0)) + "\n")
        file.write("Percentage of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            100 * np.count_nonzero(sumClass == 0) / dictionary.size) + " %\n")

with open("bbc-performance.txt", 'a') as file:
    file.write("Number of word with 1 frequency in the whole corpus = " + str(np.count_nonzero(sumClass == 1)) + "\n")
    file.write("Percentage of word with 1 frequency in the whole corpus" + str(
        100 * np.count_nonzero(sumClass == 1) / dictionary.size) + " %\n")

index1 = np.where(dictionary == 'bought')[0]
index2 = np.where(dictionary == 'oil')[0]
sum1 = 0
sum2 = 0
for sumClass in sumCountCorpus:
    sum1 += sumClass[index1]
    sum2 += sumClass[index2]
logProb1 = math.log(sum1 / sumCorpus)
logProb2 = math.log(sum2 / sumCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Log-prob of the word 'bought' = " + str(logProb1) + "\n")
    file.write("Log-prob of the word 'oil' = " + str(logProb2) + "\n")

# 9)
clf = MultinomialNB(alpha=0.9)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
with open("bbc-performance.txt",'a') as file:
    file.write('\n**************MultinomialNB smoothing value of 0.9, try 4**************\n')
    file.write(str(confusion_matrix(y_test, y_pred)) + '\n')
    file.write(str(classification_report(y_test, y_pred, target_names=corpus.target_names)) + '\n')
    file.write("Accuracy = " + str(accuracy_score(y_test, y_pred)) + '\n')
    file.write("F1 score (macro) = " + str(f1_score(y_test, y_pred, average='macro')) + '\n')
    file.write("F1 score (weighted) = " + str(f1_score(y_test, y_pred, average='weighted')) + '\n')
    file.write('Prior probability\n')
    file.write('P(Business) = 1/5\n'
               'P(Entertainment) = 1/5\n'
               'P(Politics) = 1/5\n'
               'P(Sport) =  1/5\n'
               'P(Tech) = 1/5\n')
    file.write("Vocabulary size = " + str(dictionary.size) + '\n')

sumCountCorpus = clf.feature_count_
idx = 0
for sumClass in sumCountCorpus:
    sum = np.sum(sumClass)
    with open("bbc-performance.txt", 'a') as file:
        file.write(corpus.target_names[idx] + " class word-token count =" + str(sum) + '\n')
    idx += 1

sumCorpus = np.sum(sumCountCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Corpus word-token count = " + str(sumCorpus) + '\n')

idx = 0
for sumClass in sumCountCorpus:
    with open("bbc-performance.txt", 'a') as file:
        file.write("Number of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            np.count_nonzero(sumClass == 0)) + "\n")
        file.write("Percentage of word with 0 frequency in " + corpus.target_names[idx] + " = " + str(
            100 * np.count_nonzero(sumClass == 0) / dictionary.size) + " %\n")

with open("bbc-performance.txt", 'a') as file:
    file.write("Number of word with 1 frequency in the whole corpus = " + str(np.count_nonzero(sumClass == 1)) + "\n")
    file.write("Percentage of word with 1 frequency in the whole corpus" + str(
        100 * np.count_nonzero(sumClass == 1) / dictionary.size) + " %\n")

index1 = np.where(dictionary == 'bought')[0]
index2 = np.where(dictionary == 'oil')[0]
sum1 = 0
sum2 = 0
for sumClass in sumCountCorpus:
    sum1 += sumClass[index1]
    sum2 += sumClass[index2]
logProb1 = math.log(sum1 / sumCorpus)
logProb2 = math.log(sum2 / sumCorpus)
with open("bbc-performance.txt", 'a') as file:
    file.write("Log-prob of the word 'bought' = " + str(logProb1) + "\n")
    file.write("Log-prob of the word 'oil' = " + str(logProb2) + "\n")

