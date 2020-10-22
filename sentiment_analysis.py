import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from keras import backend as K
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
from keras.layers import Input
from keras.layers.embeddings import Embedding
from keras import optimizers
from keras.layers import Dense, concatenate, Activation, Dropout
from keras.models import Model
from keras.layers.convolutional import Conv1D
from keras.layers.pooling import GlobalMaxPooling1D
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import classification_report


def main():
    # Loading sentiment data
    n = ['id', 'date', 'name', 'text', 'typr', 'rep', 'rtw', 'faw', 'stcount', 'foll', 'frien', 'listcount']

    data_positive = pd.read_csv('data/positive.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])
    data_negative = pd.read_csv('data/negative.csv', sep=';', error_bad_lines=False, names=n, usecols=['text'])

    sample_size = min(data_positive.shape[0], data_negative.shape[0])
    raw_data = np.concatenate((data_positive['text'].values[:sample_size], data_negative['text'].values[:sample_size]), axis=0)
    labels = [1] * sample_size + [0] * sample_size

    def preprocess_text(text):
        text = text.lower().replace("ё", "е")
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub(r'@[^\s]+', 'USER', text)
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        return text.strip()

    data = [preprocess_text(t) for t in raw_data]

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=2)

    # Defining metrics
    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def f1(y_true, y_pred):
        def recall(y_true, y_pred):
            """Recall metric.

            Only computes a batch-wise average of recall.

            Computes the recall, a metric for multi-label classification of
            how many relevant items are selected.
            """
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        def precision(y_true, y_pred):
            """Precision metric.

            Only computes a batch-wise average of precision.

            Computes the precision, a metric for multi-label classification of
            how many selected items are relevant.
            """
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision

        precision = precision(y_true, y_pred)
        recall = recall(y_true, y_pred)
        return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

    # Preparing weights for the embedding layer
    SENTENCE_LENGTH = 26
    NUM = 100000

    def get_sequences(tokenizer, x):
        sequences = tokenizer.texts_to_sequences(x)
        return pad_sequences(sequences, maxlen=SENTENCE_LENGTH)

    tokenizer = Tokenizer(num_words=NUM)
    tokenizer.fit_on_texts(x_train)

    x_train_seq = get_sequences(tokenizer, x_train)
    x_test_seq = get_sequences(tokenizer, x_test)

    # Load trained model
    w2v_model = Word2Vec.load('data/model.w2v')
    DIM = w2v_model.vector_size
    # Initializing the embedding layer matrix with zeros
    embedding_matrix = np.zeros((NUM, DIM))
    # Add NUM=100000 the most common words from the training sample in the embedding layer
    for word, i in tokenizer.word_index.items():
        if i >= NUM:
            break
        if word in w2v_model.wv.vocab.keys():
            embedding_matrix[i] = w2v_model.wv[word]

    # Building the CNN
    tweet_input = Input(shape=(SENTENCE_LENGTH,), dtype='int32')
    tweet_encoder = Embedding(NUM, DIM, input_length=SENTENCE_LENGTH,
                              weights=[embedding_matrix], trainable=False)(tweet_input)

    branches = []
    x = Dropout(0.2)(tweet_encoder)

    for size, filters_count in [(2, 10), (3, 10), (4, 10), (5, 10)]:
        for i in range(filters_count):
            branch = Conv1D(filters=1, kernel_size=size, padding='valid', activation='relu')(x)
            branch = GlobalMaxPooling1D()(branch)
            branches.append(branch)

    x = concatenate(branches, axis=1)
    x = Dropout(0.2)(x)
    x = Dense(30, activation='relu')(x)
    x = Dense(1)(x)
    output = Activation('sigmoid')(x)

    model = Model(inputs=[tweet_input], outputs=[output])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[precision, recall, f1])
    model.summary()

    y_train = np.array(y_train)
    # Training and evaluating the CNN
    Checkpoint = ModelCheckpoint("data/cnn-frozen-embeddings-{epoch:02d}-{val_f1:.2f}.hdf5", monitor='val_f1', save_best_only=True, mode='max', period=1)
    history = model.fit(x_train_seq, y_train, batch_size=32, epochs=10, validation_split=0.25, callbacks=[checkpoint])

    model.load_weights('data/cnn-frozen-embeddings-08-0.76.hdf5')

    predicted = np.round(model.predict(x_test_seq))
    print(classification_report(y_test, predicted, digits=5))

    model.layers[1].trainable = True
    adam = optimizers.Adam(lr=0.0001)
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=[precision, recall, f1])
    model.summary()

    checkpoint = ModelCheckpoint("data/cnn-trainable-{epoch:02d}-{val_f1:.2f}.hdf5",
                                 monitor='val_f1', save_best_only=True, mode='max', period=1)

    history_trainable = model.fit(x_train_seq, y_train, batch_size=32, epochs=5, validation_split=0.25, callbacks=[checkpoint])

    model.load_weights('data/cnn-trainable-05-0.77.hdf5')

    predicted = np.round(model.predict(x_test_seq))
    print(classification_report(y_test, predicted, digits=5))

    def sentiment_analysis():
        text = input("Введите текст: ")
        print(model.predict(get_sequences(tokenizer, [text])))
    sentiment_analysis()


if __name__ == "__main__":
    main()
