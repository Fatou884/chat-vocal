import streamlit as st
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
import math

nltk.download('stopwords')

# Fonction de prétraitement du texte
def preprocess_text(text):
    # Convertir le texte en minuscules
    text = text.lower()
    # Supprimer la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Supprimer les mots inutiles
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    return words

# Exemple de texte de base pour le chatbot
chatbot_corpus = "Bienvenue sur le chatbot à commande vocale. Posez-moi des questions, je suis là pour vous aider."
preprocessed_corpus = preprocess_text(chatbot_corpus)
# Fonction pour transcrire la parole en texte
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            st.success(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            st.error("La reconnaissance vocale n'a pas compris l'audio.")
            return ""
        except sr.RequestError:
            st.error("Erreur avec le service de reconnaissance vocale.")
            return ""


# Fonction du chatbot qui utilise le texte prétraité pour générer une réponse
def chatbot_response(user_input):
    if not user_input:
        return "Veuillez fournir une entrée textuelle ou vocale."

    user_input = preprocess_text(user_input)

    # Exemple basique de génération de réponse
    common_words = set(user_input).intersection(preprocessed_corpus)
    if common_words:
        return "J'ai trouvé des mots-clés dans votre question, je vais vous aider."
    else:
        return "Je ne suis pas sûr de comprendre, pouvez-vous reformuler ?"
# Titre de l'application
st.title("Chatbot à Commande Vocale")

# Choix de l'entrée utilisateur
input_type = st.radio("Choisissez le type d'entrée :", ("Texte", "Vocal"))

# Entrée textuelle
if input_type == "Texte":
    user_input = st.text_input("Tapez votre message ici :")
    if st.button("Envoyer"):
        response = chatbot_response(user_input)
        st.write("Réponse du chatbot :", response)

# Entrée vocale
elif input_type == "Vocal":
    if st.button("Parler"):
        user_input = speech_to_text()
        if user_input:
            response = chatbot_response(user_input)
            st.write("Réponse du chatbot :", response)


