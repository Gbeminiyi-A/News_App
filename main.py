import datetime
import requests
from flask import Flask, render_template, request
import os

NEWS_APIKEY = os.environ.get('NEWS_APIKEY')


app = Flask(__name__)

year = datetime.datetime.now().year


@app.route("/", methods=['GET', 'POST'])
def home_page():
    url = ('https://newsapi.org/v2/top-headlines?'
           f'apiKey={NEWS_APIKEY}&language=en')
    response = requests.get(url)
    articles = response.json()['articles']
    if request.method == 'POST':
        keyword = request.form.get('search')
        search_url = (f'https://newsapi.org/v2/top-headlines?'
                      f'apiKey={NEWS_APIKEY}&q={keyword}')
        search_response = requests.get(search_url)
        search_articles = search_response.json()['articles']
        return render_template('search.html', search_articles=search_articles)
    return render_template('home.html', articles=articles, year=year, category='World')


@app.route("/nigeria", methods=['GET', 'POST'])
def nigerian_news():
    url = ('https://newsapi.org/v2/top-headlines?'
           f'apiKey={NEWS_APIKEY}&country=ng')
    response = requests.get(url)
    articles = response.json()['articles']
    if request.method == 'POST':
        keyword = request.form.get('search')
        search_url = (f'https://newsapi.org/v2/top-headlines?'
                      f'apiKey={NEWS_APIKEY}&q={keyword}')
        search_response = requests.get(search_url)
        search_articles = search_response.json()['articles']
        if len(search_articles) == 0:
            return "Nothing Found"
        return render_template('search.html', search_articles=search_articles)
    return render_template('nigeria.html', articles=articles)


@app.route("/<category>")
def category_page(category):
    url = ('https://newsapi.org/v2/top-headlines?'
           f'apiKey={NEWS_APIKEY}&category={category}')
    response = requests.get(url)
    articles = response.json()['articles']
    return render_template('category.html', articles=articles, year=year, category=category.upper())


@app.route("/<country>")
def country_page(country):
    url = ('https://newsapi.org/v2/top-headlines?'
           f'apiKey={NEWS_APIKEY}&country={country}')
    response = requests.get(url)
    articles = response.json()['articles']
    return render_template('category.html', articles=articles, year=year, category=country.upper())


@app.route("/subscribe", methods=['GET', 'POST'])
def subscribe_page():
    return render_template('subscribe.html')


if __name__ == "__main__":
    app.run()
