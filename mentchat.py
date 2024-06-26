import streamlit as st
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
lemmatizer = nltk.stem.WordNetLemmatizer()

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

with open('Mental_Health_FAQ.csv', 'r', encoding='utf-8', errors='ignore') as file:
hist_list = []

data = pd.read_csv('Mental_Health_FAQ.csv')
data.drop('Question_ID', axis = 1, inplace = True)

def preprocess_text(text):
    # Identifies all sentences in the data
    sentences = nltk.sent_tokenize(text)
    
    # Tokenize and lemmatize each word in each sentence
    preprocessed_sentences = []
    for sentence in sentences:
        tokens = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence) if word.isalnum()]

        preprocessed_sentence = ' '.join(tokens)
        preprocessed_sentences.append(preprocessed_sentence)
    
    return ' '.join(preprocessed_sentences)

data['tokenized Questions'] = data['Questions'].apply(preprocess_text)

x = data['tokenized Questions'].to_list()

# Vectorize corpus
tfidf_vectorizer = TfidfVectorizer()
corpus = tfidf_vectorizer.fit_transform(x)

st.markdown("<h1 style = 'color: #31363F; text-align: center; font-family: Copperplate Gothic Semibold'>MENTAL HEALTH CHATBOT</h1>", unsafe_allow_html = True)
st.markdown("<h4 style = 'margin: -30px; color: #222831; text-align: center; font-family: Copperplate Gothic Semibold '>Built By REEDA: Daintree Cohort</h4>", unsafe_allow_html = True)
st.markdown("<br>", unsafe_allow_html= True)

st.markdown("<br>", unsafe_allow_html= True)
st.markdown("<br>", unsafe_allow_html= True)

chat_response, robot_image = st.columns(2)
with robot_image:
    robot_image.image('10209766.jpg', caption = 'I reply all your questions', width = 800)

with chat_response:
    user_word = chat_response.text_input('Hello there you can ask your questions: ')
    def get_response(user_input):
        user_input_processed = preprocess_text(user_input) # ....................... Preprocess the user's input using the preprocess_text function

        user_input_vector = tfidf_vectorizer.transform([user_input_processed])# .... Vectorize the preprocessed user input using the TF-IDF vectorizer

        similarity_scores = cosine_similarity(user_input_vector, corpus) # .. Calculate the score of similarity between the user input vector and the corpus (df) vector

        most_similar_index = similarity_scores.argmax() # ..... Find the index of the most similar question in the corpus (df) based on cosine similarity

        return data['Answers'].iloc[most_similar_index] # ... Retrieve the corresponding answer from the df DataFrame and return it as the chatbot's response

    # create greeting list 
    greetings = ["Hey There.... I am a creation of Ehiz Danny Agba Coder.... How can I help",
                "Hi Human.... How can I help",
                'Twale baba nla, wetin dey happen nah',
                'How far Alaye, wetin happen',
                "Good Day .... How can I help", 
                "Hello There... How can I be useful to you today",
                "Hi GomyCode Student.... How can I be of use"]

    exits = ['thanks bye', 'bye', 'quit', 'exit', 'bye bye', 'close']
    farewell = ['Thanks....see you soon', 'Babye, See you soon', 'Bye... See you later', 'Bye... come back soon']

    random_farewell = random.choice(farewell) # ---------------- Randomly select a farewell message from the list
    random_greetings = random.choice(greetings) # -------- Randomly select greeting message from the list

    # Test your chatbot
    # while True:
    # user_input = input("You: ")
    if user_word.lower() in exits:
        chat_response.write(f"\nChatbot: {random_farewell}!")

    elif user_word.lower() in ['hi', 'hello', 'hey', 'hi there']:
        chat_response.write(f"\nChatbot: {random_greetings}!")

    elif user_word == '':
        chat_response.write('')
        
    else:   
        response = get_response(user_word)
        chat_response.write(f"\nChatbot: {response}")

 # history starting 
        hist_list.append(user_word)

# # Save the history of the texts 
with open('history.txt', 'a') as file:
        for item in hist_list:
            file.write(str(item) + '\n')
            file.write(response)    

import csv
files = 'history.txt'
try:
    with open(files, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        data_hist = list(reader)
except UnicodeDecodeError:
    with open(files, encoding='latin-1') as f:
        reader = csv.reader(f)
        data_hist = list(reader)
        
history = pd.DataFrame(data_hist)
st.sidebar.subheader('Chat History', divider=True)
st.sidebar.write(history)
# history = pd.Series(data)
# st.sidebar.subheader('Chat History', divider = True)
# st.sidebar.write(history)

st.header('Project Background Information', divider = True)
st.write("The objectives of a mental health chatbot include providing supportive conversations, offering immediate assistance in crisis situations, normalizing mental health discussions, assessing and monitoring mental health, providing psychoeducation and coping strategies, facilitating access to resources, maintaining user privacy, continuously improving through feedback, and collaborating with mental health professionals to enhance support effectiveness.")

st.markdown("<br>", unsafe_allow_html= True)
st.markdown("<br>", unsafe_allow_html= True)

