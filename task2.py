# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('drug200.csv')

df_dummies = pd.get_dummies(df)

print(df_dummies)
df_category = pd.Categorical(df_dummies, ordered=True, categories=['Drug_drugA', 'Drug_drugB', 'Drug_drugC', 'Drug_drugX', 'Drug_drugY'])

print(df_category)

# X_train, X_test, y_train, y_test = train_test_split(df_dummies.values, df_category.ordered, test_size=0.20, random_state=None)
