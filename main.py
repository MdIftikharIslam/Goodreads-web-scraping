from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.goodreads.com/quotes' 

request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')
quotes = soup.find('div', attrs={'class':'quotes'})

quote = quotes.findAll('div', attrs={'class':'quote'})

final_quotes = []


for item in quote:
    qts = item.find('div', attrs={'class':'quoteText'})
    author = item.find('span', attrs={'class':'authorOrTitle'}).text
    qts.span.decompose()
    if qts.find('script'):
        qts.script.decompose()
        qts.span.decompose()

    quotations = {
        'quote':qts.text.strip().replace('“', '').replace('”', '').replace('\n    ―', ''),
        'author':author.strip().replace(',', ''),
        'likes':item.find('div', {'class':'right'}).get_text().replace('\n', '').replace('likes', '').strip()
    }
    final_quotes.append(quotations)
    # print(quotations)
df = pd.DataFrame(final_quotes)
df.to_csv('output.csv', index=False)
print(final_quotes)
