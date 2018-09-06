import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import json
import pickle

sent = input("write a sentence")

words = []

# read the json file and load the training data
with open('data.json') as json_data:
    data = json.load(json_data)

# get a list of all categories to train for
with open("categories.txt", "rb") as fp:   # Unpickling
    categories = pickle.load(fp)


with open("words.txt", "rb") as fp:   # Unpickling
   words = pickle.load(fp)


training = np.load("training_data.npy")

stemmer = LancasterStemmer()

# trainX contains the Bag of words and train_y contains the label/ category
train_x = list(training[:, 0])
train_y = list(training[:, 1])


# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('model.tflearn')


def get_tf_record(sentence):
    global words
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    # bag of words
    bow = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bow[i] = 1

    return(np.array(bow))


# PREDICT THE SENTENCE
sent_4 = "i am taking better of myself to stay healthy and  strong the rest of my life."
sent_1 = "My daughter is getting married next spring.  I know she'll make a beautiful bride."
sent_3 = "I am trying to increase my earnings, as money has been tight. If I don’t have enough for every day expenses, I will be in trouble."
print(categories[np.argmax(model.predict([get_tf_record(sent_4)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent_1)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent_3)]))])
print(categories[np.argmax(model.predict([get_tf_record(sent)]))])
