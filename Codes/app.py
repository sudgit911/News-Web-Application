import os
from flask import Flask, render_template, request
from newsapi import NewsApiClient
from dotenv import load_dotenv
from newspaper import Article
import logging

load_dotenv()

app = Flask(__name__)

# Load the API key from .env file
api_key = os.getenv('NEWSAPI_KEY')

# Initialize the NewsApiClient with the API key
newsapi = NewsApiClient(api_key=api_key)

# Logging setup
logging.basicConfig(level=logging.INFO)

def fetch_articles(page, topic=None):
    try:
        params = {
            'language': 'en',
            'page': page,
            'page_size': 4
        }
        if topic:
            params['category'] = topic
        top_headlines = newsapi.get_top_headlines(**params)
        articles = top_headlines.get('articles', [])
        
        total_results = top_headlines.get('totalResults', 0)
        total_pages = (total_results // 4) + (1 if total_results % 4 else 0)

        processed_articles = []
        for article in articles:
            try:
                a = Article(article['url'])
                a.download()
                a.parse()
                processed_articles.append({
                    'title': a.title,
                    'content': a.text[:200],  # Truncate content to first 200 characters
                    'link': article['url'],
                    'image': article['urlToImage'] or 'https://via.placeholder.com/150',
                })
            except Exception as e:
                logging.error(f"Error processing article: {e}")

        return processed_articles, total_pages
    except Exception as e:
        logging.error(f"Error fetching articles: {e}")
        return [], 0

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    topic = request.args.get('topic', None)
    articles, total_pages = fetch_articles(page, topic)
    return render_template('index.html', articles=articles, page=page, total_pages=total_pages, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)
