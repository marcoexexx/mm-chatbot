import random
import spacy
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


load_dotenv()

APIKEY = "74cf32adb0msha9568d15b271819p103232jsnfd977803a28b"

nlp = spacy.load('en_core_web_md')

## Data
question_answers = {
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

    for question, answers in question_answers.items():
        question_doc = nlp(question.lower())
        if question_doc.similarity(user_input_doc) > 0.7:
            return random.choice(answers)

        return "I'm sorry, I don't understand that."


def weather(city: str):
    url = f"https://open-weather13.p.rapidapi.com/city/{city}"
    headers = {
        "X-RapidAPI-Key": APIKEY,
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    print(response.json())


def translate(payload: dict) -> Optional[str]:
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": APIKEY,
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

    return None



app = FastAPI()


class Message(BaseModel):
    user_input: str
    # lang: Literal["en", "my"]
    lang: str


@app.post("/api/v1/chatbot")
async def index(message: Message):
    user_input = message.user_input

    if message.lang == "my":
        user_input = translate(payload={"source": "my", "target": "en", "q": message.user_input})
        if not user_input:
            assert HTTPException(status_code=400, detail="failed translate")

    bot_response = get_response(user_input)
    mm_bot_response = translate(payload={"source": "en", "target": "my", "q": bot_response})
    if not mm_bot_response:
        assert HTTPException(status_code=400, detail="failed translate")

    return { "bot": mm_bot_response, "user_input": user_input }
