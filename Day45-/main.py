from bs4 import BeautifulSoup
import requests
#import lxml
print("Starting request...")
response = requests.get("https://news.ycombinator.com/news",timeout=10)
print("Request completed")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")  
print("Page downloaded")
article_tag = soup.find_all(name="a", class_="titlelink")
print("Found", len(article_tag), "articles")
article_texts=[]
article_links=[]
for article in article_tag:
    text = article.getText()
    article_texts.append(text)
    link = article.get("href")
    article_links.append(link)  
    
article_upvote = [
    score.getText()
    for score in soup.find_all(name="span", class_="score")
]
# with open("website.html") as file:
#     contents = file.read()

print(text)
print(link)
for title in article_texts:
    print(title)
print(article_upvote)

