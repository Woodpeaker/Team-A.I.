import gensim.downloader as api
import pandas as pd

wv = api.load('word2vec-google-news-300')
print('loading synonyms.csv...')
df = pd.read_csv('synonyms.csv')

for data in df.values:
    question = data[0]
    answer = data[1]
    nbNotFind = 0
    guess = None
    cosineSimilarity = 0
    print(F'Evaluating {question} with:{data[2]} {data[3]} {data[4]} {data[5]}')
    for i in range(2, 6):
        word = data[i]
        # Evaluating each words in the question
        try:
            evalCosine = wv.similarity(question, word)
            # Compare cosine similarity to get the word with the highest score.
            if evalCosine > cosineSimilarity:
                cosineSimilarity = evalCosine
                guess = word
        except KeyError:
            # Word not found in the model vocabulary
            print(F'Could not evaluate {word}')
    print(F'Guessed word: {guess}')
    print(F'Answer: {answer}')
    print(F'--------------------------------------------------------')
