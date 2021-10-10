import pandas as pd
import matplotlib.pyplot as plt

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
