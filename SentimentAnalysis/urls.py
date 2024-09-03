from django.contrib import admin
from django.urls import path
from SentimentAnalysisApp.views import analyze_sentiment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analyze_sentiment, name='analyze_sentiment'),
]

