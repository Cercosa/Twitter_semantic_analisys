import re
import sqlite3
import logging
import multiprocessing
import gensim
from gensim.models import Word2Vec


def main():
    def preprocess_text(text):
        text = text.lower().replace("ё", "е")
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub(r'@[^\s]+', 'USER', text)
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        return text.strip()

    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()

    with open('data/tweets.txt', 'w', encoding='utf-8') as f:
        # reading tweets text
        for row in c.execute('SELECT ttext FROM sentiment'):
            if row[0]:
                # write processed tweets to file
                tweet = preprocess_text(row[0])
                print(tweet, file=f)

    # traing Word2Vec-model with Gensim
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)
    # reading file with processed tweets
    data = gensim.models.word2vec.LineSentence('data/tweets.txt')
    # train model
    model = Word2Vec(data, size=200, window=5, min_count=3,
                     workers=multiprocessing.cpu_count())
    model.save("data/model.w2v")


if __name__ == "__main__":
    main()
