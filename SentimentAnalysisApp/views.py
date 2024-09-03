import praw
from textblob import TextBlob
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from io import BytesIO
import base64
import numpy as np


def get_reddit_instance():
    return praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT
    )


def analyze_sentiment(request):
    asset = request.GET.get('asset', None)
    if asset:
        reddit = get_reddit_instance()
        subreddit = reddit.subreddit(asset)

        sentiments = []

        for submission in subreddit.hot(limit=100):
            analysis = TextBlob(submission.title)
            sentiment_polarity = analysis.sentiment.polarity

            if sentiment_polarity != 0.0:
                sentiments.append(sentiment_polarity)

        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

        # Tworzenie histogramu z mniejszym rozmiarem
        plt.figure(figsize=(8, 4), dpi=150)  # Zmniejszamy rozmiar i zwiększamy jakość (DPI)
        plt.hist(sentiments, bins=np.linspace(-1, 1, 20), edgecolor='black')
        plt.title(f'Sentiment Analysis for {asset}')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Number of Posts')

        # Zapisanie wykresu w pamięci
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        image_base64 = base64.b64encode(image_png).decode('utf-8')

        return render(request, 'SentimentAnalysisApp/results.html', {
            'avg_sentiment': avg_sentiment,
            'sentiment_chart': image_base64,
            'asset': asset,
        })
    return render(request, 'SentimentAnalysisApp/index.html')
