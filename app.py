"""MD Central Webserver"""
import os

from typing import Any

import requests

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
app = Flask(__name__)

KANYE_URL = "https://api.kanye.rest/text"
TENNIS_URL = "https://tennis-live-data.p.rapidapi.com"

def get_kanye_quote(amount: int=1) -> list[str]:
    """returns kanye quotes"""
    quotes = []
    for _ in range(amount):
        quote = requests.get(KANYE_URL, timeout=5)
        if quote.status_code != 200:
            return []
        quotes.append(quote.text)
    return quotes

def get_tennis_stats() -> Any:
    """Returns stats about tennis"""
    key = os.environ.get('API_KEY')
    if not key:
        print("NO API KEY")
        return None
    url = TENNIS_URL + "/players/ATP"
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "tennis-live-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response = response.json()
    return response['results']['players'][:4]

@app.route('/')
def homepage() -> str:
    """Homepage"""
    return render_template("index.html")

@app.route('/kanye')
def kanye_quote() -> str:
    """Kanye Page"""
    quotes = request.args.get('quotes', type=int)
    if not quotes:
        quotes = 1
    return render_template("kanye.html", quotes=get_kanye_quote(quotes))

@app.route('/tennis')
def tennis() -> str:
    """Tennis Page"""
    return render_template("tennis.html", players=get_tennis_stats())

@app.route('/gpt')
def gpt() -> str:
    """gpt"""
    return render_template("gpt.html")

if __name__ == "__main__":
    app.run(debug=True)
    