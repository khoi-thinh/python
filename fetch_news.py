# Use newsapi key to fetch news, save results if there is in CSV to user desktop folder and notify user
# register here: https://newsapi.org/
import requests
import csv 
from datetime import datetime
from plyer import notification
from pathlib import Path

# Define keyword and API key
key_word = "japan"
today = datetime.today().strftime('%Y-%m-%d')
api_key = "KEY_HERE"
query = f"q={key_word}&from={today}&to={today}&sortBy=popularity&apiKey={api_key}"

def get_news(query):
    news_url = f"https://newsapi.org/v2/everything?{query}"
    response = requests.get(news_url)

    if response.status_code == 200:
        articles = response.json().get("articles")

        if not articles:
            return None
        
        return articles

    else:
        print("Can not fetch news.", response.status_code, response.text)
        return None

def save_to_csv(articles):
    desktop = Path.home() / "Desktop"  
    csv_file_path = desktop / "news_articles.csv"

    # Write articles to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL"])  

        for article in articles:
            title = article.get("title")
            url = article.get("url")
            writer.writerow([title, url])  

    print(f"Articles have been saved to {csv_file_path}")

def notify_me(content):
    notification_title = "Hello Khoi!"
    notification_message = content
    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=5
    )

articles = get_news(query)

if articles:
    save_to_csv(articles)
    notify_me(f"Saved {len(articles)} articles to CSV on desktop.")
else:
    notify_me("No articles founded.")
