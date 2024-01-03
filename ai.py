from random import choice, random
import spacy

# Load spaCy pre-trained model with word vectors
nlp = spacy.load('en_core_web_md')

# Define your own set of custom Q&A pairs
custom_qa_pairs = {
    "Weather": ["example fetch weater ... in code", "you can look code snippets in github", "i cant provide weater api currently"],
    "What is your name?": ["I am a chatbot.", "You can call me SpaCyBot."],
    "How are you?": ["I'm just a program, so I don't have feelings, but thanks for asking!"],
    "Python programming": ["Python is a versatile programming language.", "It is known for its readability and ease of use."],
    "Hello": ["Hi there!", "Greetings!", "Hello! How can I assist you?"],
    "Good morning": ["Good morning! How can I help?", "Morning! What can I do for you?"],
    "Parse this sentence": ["Sure! I can help analyze the sentence structure."],

}

def get_response(user_input):
    user_input_doc = nlp(user_input.lower())

    for question, answers in custom_qa_pairs.items():
        question_doc = nlp(question.lower())
        if question_doc.similarity(user_input_doc) > 0.7:
            return choice(answers)

    return "I'm sorry, I don't understand that."

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("SpaCyBot: Goodbye!")
        break
    response = get_response(user_input)
    print("SpaCyBot:", response)

