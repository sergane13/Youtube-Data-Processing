from Oauth_for_reddit import *
from textblob import TextBlob
import pprint
import nltk


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


what_you_search = input('WHAT YOU SEARCH?: ')
limit_number = int(input('Number of searches pls : '))

url_oauth, headers = oauth_reddit()
data = search_subreddit(url_oauth, headers, what_you_search, limit_number)

for i in range(limit_number):
    # print(data['data']['children'][i]['data']['title'])
    analysis = TextBlob(data['data']['children'][i]['data']['title'])
    # print(dir(analysis))
    # print(analysis.translate(to='es'))
    print(analysis.sentiment)
