from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import pandas as pd

# 3)
corpus = load_files('BBC', load_content=True, encoding='latin-1')
X_data, y = corpus.data, corpus.target

# 4)
vectorizer = CountVectorizer(encoding='latin-1')
X_vectorized = vectorizer.fit_transform(X_data)
X = X_vectorized.toarray()
dictionary = vectorizer.get_feature_names_out()
# print(vectorizer.get_feature_names_out())
# print(X)

# 5)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=None)

# 6)
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 7)
print('**************MultinomialNB default values, try 1**************')
y_pred = clf.predict(X_test)

print('(b)')
print(confusion_matrix(y_test, y_pred))

print('(c)')
print(classification_report(y_test, y_pred, target_names=corpus.target_names))

print('(d)')
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))
print(f1_score(y_test, y_pred, average='weighted'))

print('(e)')
print('Prior probability')
print('P(Business) = 1/5\n'
      'P(Entertainment) = 1/5\n'
      'P(Politics) = 1/5\n'
      'P(Sport) =  1/5\n'
      'P(Tech) = 1/5\n')

print('(f)')
print(dictionary.size)

print('(g)')
classIdx = 0
for currClass in corpus.target_names:
    count = 0
    for dat in X[y == classIdx]:
        for num in dat:
            count = count + num
    print(count)
    classIdx = classIdx + 1

print('(h)')
count = 0
for dat in X:
    for num in dat:
        count = count + num
print(count)

print('(i)')
classIdx = 0
for currClass in corpus.target_names:
    freq = 0
    idx = 0
    for word in dictionary:
        if sum(X[y == classIdx, idx]) == 0:
            freq = freq + 1
        idx = idx + 1
    print(freq/dictionary.size)
    classIdx = classIdx + 1

print('(j)')
classIdx = 0
for currClass in corpus.target_names:
    freq = 0
    idx = 0
    for word in dictionary:
        if sum(X[y == classIdx, idx]) == 1:
            freq = freq + 1
        idx = idx + 1
    print(freq/dictionary.size)
    classIdx = classIdx + 1

print('(k)')
