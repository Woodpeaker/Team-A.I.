import gensim.downloader as api
import pandas as pd
import csv

def modelAnalysis(model = 'word2vec-google-news-300'):
    wv = api.load(model)
    print('loading synonyms.csv...')
    df = pd.read_csv('synonyms.csv')

    header = ['question', 'answer', 'system guess', 'label']
    C = 0
    nbGuess = 0
    with open(F'{model}-details.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        for data in df.values:
            question = data[0]
            answer = data[1]
            guess = None
            cosineSimilarity = 0
            label = ''
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
            if guess is None:
                label = 'guess'
                nbGuess += 1
            elif guess == answer:
                label = 'correct'
                C += 1
            else:
                label = 'wrong'
            # write the data
            writer.writerow([question, answer, guess, label])
            print(F'Guessed word: {guess}')
            print(F'Answer: {answer}')
            print(F'--------------------------------------------------------')
    V = 80 - nbGuess
    return (len(wv),C, V, C/V)
header = ['Model', 'Vocab size', 'C', 'V', 'Accuracy']
with open(F'analysis.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    # TASK 1
    model = 'word2vec-google-news-300'
    size, C, V, accuracy = modelAnalysis(model=model)
    writer.writerow([model, size, C, V, C/V])
    # TASK 2
    # C1
    model = 'glove-wiki-gigaword-300'
    size, C, V, accuracy = modelAnalysis(model=model)
    writer.writerow([model, size, C, V, C / V])
    # C2
    model = 'fasttext-wiki-news-subwords-300'
    size, C, V, accuracy = modelAnalysis(model=model)
    writer.writerow([model, size, C, V, C / V])
    # C3
    model = 'glove-twitter-100'
    size, C, V, accuracy = modelAnalysis(model=model)
    writer.writerow([model, size, C, V, C / V])
    # C4
    model = 'glove-twitter-200'
    size, C, V, accuracy = modelAnalysis(model=model)
    writer.writerow([model, size, C, V, C / V])
