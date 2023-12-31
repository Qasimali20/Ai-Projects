# -*- coding: utf-8 -*-
"""Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gE2HC5t5sdiaeUCUPpfMuWUgq2uIeLEX
"""

import os
os.environ['KAGGLE_USERNAME']="KAGGLE_USERNAME"
os.environ['KAGGLE_KEY']="KAGGLE_KEY"
!kaggle datasets download yasserh/twitter-tweets-sentiment-dataset

!unzip twitter-tweets-sentiment-dataset

import pandas as pd
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer ,TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

df = pd.read_csv('Tweets.csv')
df.head()
df = df.dropna(subset=['text'])

# Convert any non-string values in the 'text' column to strings
df['text'] = df['text'].astype(str)

stop_words = set(stopwords.words('english'))
df['tokenized_text'] = df['text'].apply(lambda x: word_tokenize(x.lower()))
df['tokenized_text'] = df['tokenized_text'].apply(lambda x: [word for word in x if word not in stop_words])

# Convert tokens back to text
df['cleaned_text'] = df['tokenized_text'].apply(lambda x: ' '.join(x))

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['sentiment'], test_size=0.2, random_state=42)
# Vectorize the text data using CountVectorizer
vectorizer = CountVectorizer(max_features=5000)  # You can adjust max_features
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Initialize and fit the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust max_features
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

clf = LogisticRegression()
clf.fit(X_train_vec, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test_vec)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display classification report with precision, recall, and F1-score
print(classification_report(y_test, y_pred))