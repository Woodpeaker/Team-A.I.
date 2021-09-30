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


#4)
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(encoding='latin-1')

X1 = vectorizer.fit_transform(businessCorpus)
print(vectorizer.inverse_transform(X1))
print(X1.toarray())

X2 = vectorizer.fit_transform(entertainmentCorpus)
print(X2.toarray())

X3 = vectorizer.fit_transform(politicsCorpus)
print(X3.toarray())

X4 = vectorizer.fit_transform(sportCorpus)
print(X4.toarray())

X5 = vectorizer.fit_transform(techCorpus)
print(X5.toarray())

#5)
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X1, test_size=0.20, random_state=None)
print(X_train)


#6)
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(X_train,X_test)
print(clf.predict(X1))