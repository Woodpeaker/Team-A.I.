# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd

df = pd.read_csv('drug200.csv')

print(df.to_string())
import matplotlib.pyplot as plt

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
