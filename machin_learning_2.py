import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
import re
import logging
import multiprocessing
import gensim
from gensim.models import Word2Vec

n = ['id', 'date', 'name', 'text', 'typr', 'rep', 'rtw', 'faw', 'stcount',
     'foll', 'frien', 'listcount']
data_positive = pd.read_csv('positive.csv', sep=';', error_bad_lines=False,
                            names=n, usecols=['text'])
data_negative = pd.read_csv('negative.csv', sep=';', error_bad_lines=False,
                            names=n, usecols=['text'])

sample_size = min(data_positive.shape[0], data_negative.shape[0])
raw_data = np.concatenate((data_positive['text'].values[:sample_size],
                           data_negative['text'].values[:sample_size]), axis=0)
labels = [1] * sample_size + [0] * sample_size


def preprocess_text(text):
    text = text.lower().replace("ё", "е")
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()


data = [preprocess_text(t) for t in raw_data]

if __name__ == "__main__":
    pass

x_train, x_test, y_train, y_test = train_test_split(data,
                                                    labels, test_size=0.2,
                                                    random_state=1)
conn = sqlite3.connect('sentiment.db')
c = conn.cursor()


def writing_tweets():
    with open('tweets.txt', 'w', encoding='utf-8') as f:
        for row in c.execute('SELECT ttext FROM sentiment'):
            if row[0]:
                tweet = preprocess_text(row[0])
                print(tweet, file=f)


if __name__ == "__main__":
    pass

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

data_tweets = gensim.models.word2vec.LineSentence('tweets.txt')
model = Word2Vec(data_tweets, size=200, window=5, min_count=3,
                 workers=multiprocessing.cpu_count())

model.save("model.w2v")
