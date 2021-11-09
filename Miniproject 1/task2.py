import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
import statistics
import numpy
import warnings
import sklearn.exceptions
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore")

df = pd.read_csv('drug200.csv')

names = ['DrugA', 'DrugB', 'DrugC', 'DrugX', 'DrugY']
countA = 0
countB = 0
countC = 0
countX = 0
countY = 0
for Drug in df['Drug']:
    if Drug == 'drugA':
        countA = countA+1
    if Drug == 'drugB':
        countB = countB+1
    if Drug == 'drugC':
        countC = countC+1
    if Drug == 'drugX':
        countX = countX+1
    if Drug == 'drugY':
        countY = countY+1
values = [countA, countB, countC, countX, countY]

plt.bar(names, values)
plt.suptitle('Instance of each class')
plt.ylabel('Number of instances')
plt.xlabel('Class names')
plt.savefig("drug-distribution.pdf")
plt.show()


df_dummies = df['Age']
df_category = pd.Categorical(df['Sex'], ordered=False, categories=['M', 'F'])
df_dummies = pd.Series(df_category.codes, name='Sex')
df_dummies = pd.concat([df_dummies, pd.get_dummies(df['Sex'])], axis=1)
df_category = pd.Categorical(df['BP'], ordered=True, categories=['LOW', 'NORMAL', 'HIGH'])
df_dummies = pd.concat([df_dummies, pd.Series(df_category.codes, name='BP')], axis=1)
df_category = pd.Categorical(df['Cholesterol'], ordered=True, categories=['NORMAL', 'HIGH'])
df_dummies = pd.concat([df_dummies, pd.Series(df_category.codes, name='Cholesterol')], axis=1)
df_dummies = pd.concat([df_dummies, df['Na_to_K']], axis=1)
df_category = pd.Categorical(df['Drug'], ordered=False, categories=['drugA', 'drugB', 'drugC', 'drugX', 'drugY'])

X_train, X_test, y_train, y_test = train_test_split(df_dummies, pd.Series(df_category.codes))
#####################################################################################################
y_pred= GaussianNB().fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('**************NB**************\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
y_pred= DecisionTreeClassifier().fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('\n**************Base DT**************\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
param = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [60,80],
    'min_samples_split': [20, 60, 80],
}
grid  = GridSearchCV(DecisionTreeClassifier(), param)
y_pred= grid.fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('\n**************Top DT**************\n')
    file.write(str(grid.best_params_)+'\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
y_pred= Perceptron().fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('\n**************Perceptron**************\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
y_pred= MLPClassifier(hidden_layer_sizes=[100], activation='logistic', solver='sgd', max_iter=2000).fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('\n**************BASE-MLP,hidden_layer_sizes: 100, activation: logistic, solver: sgd**************\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
param = {
    'hidden_layer_sizes': [(30,50), (10,10,10)],
    'activation': ['tanh', 'relu', 'identity'],
    'solver': ['sgd', 'adam'],
}
grid = GridSearchCV( MLPClassifier(), param)
y_pred= grid.fit(X_train, y_train).predict(X_test)
cm=confusion_matrix(y_test, y_pred)
cr = classification_report(y_test, y_pred, target_names=df_category.categories)
ac =accuracy_score(y_test, y_pred)
f1m=f1_score(y_test, y_pred, average='macro')
f1w=f1_score(y_test, y_pred, average='weighted')
with open('drugs-performance.txt', 'a') as file:
    file.write('\n**************Top MLP*************\n')
    file.write(str(grid.best_params_)+'\n')
    file.write(str(cm)+'\n')
    file.write(str(cr)+'\n')
    file.write("Accuracy = "+str(ac)+'\n')
    file.write("f1 score (macro) = "+str(f1m)+'\n')
    file.write("fi score (weighted) = "+str(f1w)+'\n')
#####################################################################################################
arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= GaussianNB().fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running GaussianNB 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')

arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= DecisionTreeClassifier().fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running DecisionTreeClassifier 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')

param = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [60,80],
    'min_samples_split': [20, 60, 80],
}
arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= GridSearchCV(DecisionTreeClassifier(), param).fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running GridSearchCV - DecisionTreeClassifier 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')

arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= Perceptron().fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running Perceptron 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')

arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= MLPClassifier(hidden_layer_sizes=[100], activation='logistic', solver='sgd', max_iter=2000).fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running MLPClassifier 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')

param = {
    'hidden_layer_sizes': [(30,50), (10,10,10)],
    'activation': ['tanh', 'relu', 'identity'],
    'solver': ['sgd', 'adam'],
}
arrayAc =[]
arrayF1m =[]
arrayF1w=[]
for i in range(10):
    y_pred= GridSearchCV( MLPClassifier(), param).fit(X_train, y_train).predict(X_test)
    arrayAc.append(accuracy_score(y_test, y_pred))
    arrayF1m.append(f1_score(y_test, y_pred, average='macro'))
    arrayF1w.append(f1_score(y_test, y_pred, average='weighted'))
avgAc= statistics.mean(arrayAc)
stdAc = numpy.std(arrayAc)
avgF1m= statistics.mean(arrayF1m)
stdF1m = numpy.std(arrayF1m)
avgF1w= statistics.mean(arrayF1w)
stdF1w = numpy.std(arrayF1w)
with open('drugs-performance.txt', 'a') as file:
    file.write("\n************************************************\n")
    file.write("Running GridSearchCV - MLPClassifier 10 times:\n")
    file.write("Average accuracy = "+str(avgAc)+'\n')
    file.write("Average f1 score (macro) = "+str(avgF1m)+'\n')
    file.write("Average fi score (weighted) = "+str(avgF1w)+'\n')
    file.write("Standard deviation accuracy = "+str(stdAc)+'\n')
    file.write("Standard deviation f1 score (macro) = "+str(stdF1m)+'\n')
    file.write("Standard deviation fi score (weighted) = "+str(stdF1w)+'\n')


