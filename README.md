# SmartEngage AI - Spam Email Classifier

A machine learning web application that detects whether a given message/email is **Spam** or **Not Spam** using NLP and a classification model.

## Live Demo

[Click here to view the app](https://smartengage-ai-sbi.streamlit.app/)

## Project Overview

This project uses Natural Language Processing and Machine Learning to classify text messages as spam or ham. The model is trained on a labeled dataset of messages and uses text preprocessing, TF-IDF vectorization, and Multinomial Naive Bayes for prediction.

## Features

- Detects spam and non-spam messages
- Text preprocessing using NLP techniques
- TF-IDF based feature extraction
- Multinomial Naive Bayes classifier
- Simple Streamlit web interface
- Saved model and vectorizer for reuse

## Tech Stack

- Python
- Pandas
- NLTK
- Scikit-learn
- Joblib
- Streamlit

## Machine Learning Concepts Used

- Supervised Learning
- Classification
- Natural Language Processing
- Text Preprocessing
- Stopword Removal
- Stemming
- TF-IDF Vectorization
- Naive Bayes Classification
- Model Evaluation
- Model Serialization

## Project Structure

```text
SPAMEMAILCLASSIFIER
│
├── data
│   └── spam.csv
│
├── models
│   ├── spam_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src
│   ├── app.py
│   ├── predict.py
│   └── train.py
│
└── requirements.txt
