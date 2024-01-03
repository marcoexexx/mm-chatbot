import random
import spacy
import requests
import os
from typing import Optional
from flask import Flask, abort, jsonify, request


## Data
question_answers = {
    "Hello": ["hi", "hey", "how is going"],
    "The weather": ["example fetch weater ... in code", "you can look code snippets in github", "i cant provide weater api currently"],
    "What is your name?": ["I am a chatbot.", "You can call me SpaCyBot."],
    "How are you?": ["I'm just a program, so I don't have feelings, but thanks for asking!"],
    "Python programming": ["Python is a versatile programming language.", "It is known for its readability and ease of use."],
}


def get_response(user_input):
    user_input_doc = nlp(user_input.lower())

    for question, answers in question_answers.items():
        question_doc = nlp(question.lower())
        if question_doc.similarity(user_input_doc) > 0.7:
            return random.choice(answers)

        return "I'm sorry, I don't understand that."


def weather(city: str):
    url = f"https://open-weather13.p.rapidapi.com/city/{city}"
    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    print(response.json())


def translate(payload: dict) -> Optional[str]:
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data")
        translations = data.get("translations", [])

        if not translations:
            return None

        tranlsated = translations[0].get("translatedText")

        if not tranlsated:
            return None

        return tranlsated

    print(payload, response)


    return None




app = Flask(__name__)

nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})
    return response


@app.route("/api/v1/chatbot", methods=["GET"])
def index():
    user_input = request.args.get("input", "help")
    lang = request.args.get("lang", None)
    bot_response = None

    if not lang:
        return abort(400, 'must provide lang :: en, my')

    if lang == "en":
        translated_user_input = translate(payload = {
            "source": "en",
            "target": "my",
            "q": user_input
        })

        if not translated_user_input:
            return abort(400, "Failed translate")

        bot_response = get_response(translated_user_input.lower())
    elif lang == "my":
        translated_user_input = translate(payload = {
            "source": "my",
            "target": "en",
            "q": user_input
        })

        if not translated_user_input:
            return abort(400, "Failed translate")

        bot_response = get_response(translated_user_input.lower())

    bot_response = translate(payload={
        "source": "en",
        "target": "my",
        "q": bot_response
    })

    if not bot_response:
        return abort(400, "Failed translate")

    return jsonify({ "user": user_input, "bot": bot_response })


@app.route("/api/v1/may-error", methods=["GET"])
def maybe_error():
    return abort(status=500)
