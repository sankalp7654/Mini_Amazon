import requests
import json

def getheadlines():
    try:
        content = requests.get('https://newsapi.org/v2/everything?domains=wsj.com&apiKey=e0c34b118dbc47a0b5b1da58b1aff027')
        text = content.text
        data = json.loads(text)
        #print(json.dumps(data, indent = 4))
        headlines = []
        for article in data['articles']:
            headlines.append(article['title'])
        return headlines 
    
    except:
        return None    