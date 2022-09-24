#Script di backend per la raccolta dei tweets, la pulizia e la generazione delle word clouds

import tweepy # tweepy module to interact with Twitter
import pandas as pd # Pandas library to create dataframes
from tweepy import OAuthHandler # Used for authentication
from tweepy import Cursor # Used to perform pagination
from wordcloud import WordCloud, STOPWORDS 
from matplotlib import pyplot as plt
import re
#from stop_words import get_stop_words
#from nltk.corpus import stopwords
import datetime
import sys
#from io import BytesIO
#from PIL import Image
#import numpy as np
import os
#from dotenv import load_dotenv
#load_dotenv()


"""
Twitter Authentification Credentials
Please update with your own credentials
"""
cons_key = os.getenv('cons_key')
cons_secret = os.getenv('cons_secret')
acc_token = os.getenv('acc_token')
acc_secret = os.getenv('acc_secret')

# (1). Athentication Function

import tweepy

auth = tweepy.OAuthHandler(cons_key, cons_secret)
auth.set_access_token(acc_token, acc_secret)

api = tweepy.API(auth)

def get_tweets_from_user(twitter_user_name, page_limit=16, count_tweet=200):
    
    all_tweets = []
    
    for page in Cursor(api.user_timeline, 
                        screen_name=twitter_user_name, 
                        count=count_tweet,tweet_mode='extended').pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['date'] = tweet.created_at
            parsed_tweet['author'] = tweet.user.name
            parsed_tweet['twitter_name'] = tweet.user.screen_name
            parsed_tweet['text'] = tweet.full_text
            parsed_tweet['number_of_likes'] = tweet.favorite_count
            parsed_tweet['number_of_retweets'] = tweet.retweet_count
                
            all_tweets.append(parsed_tweet)
    
    # Create dataframe 
    df = pd.DataFrame(all_tweets)
    
    # Revome duplicates if there are any
    df = df.drop_duplicates( "text" , keep='first')
    
    return df




def wordcloud(nome_utente):
  user = get_tweets_from_user(nome_utente)
  # Prendo solo i dati da quando è caduto il governo Draghi 
  user["date"] = pd.to_datetime(user["date"]).dt.tz_localize(None)
  user = user[user["date"]> datetime.datetime.strptime('2022-07-21',"%Y-%m-%d")]
  user = user.sort_values('number_of_likes',ascending=False)
  
  user_list = user.text.apply(str)  
  user_list_nort = [x for x in user_list if not x.startswith('RT')]
  user_txt = ('').join(user_list_nort)


  #Un po' di pulizia (si può sicuramente fare di più)

  user_txt = re.sub(r'\&\w*;', '', user_txt)
      #Convert @username to AT_USER
  user_txt = re.sub('@[^\s]+','',user_txt)
      # Remove tickers
  user_txt = re.sub(r'\$\w*', '', user_txt)
      # To lowercase
  user_txt = user_txt.lower()
      # Remove user_txt
  user_txt = re.sub(r'https?:\/\/.*\/\w*', '', user_txt)
  user_txt = re.sub(r'italia', '', user_txt)
  user_txt = re.sub(r'settembre', '', user_txt)
      # Remove hashtags
  user_txt = re.sub(r'#\w*', '', user_txt)
  
  #Remove single character
  user_txt = re.sub(r'\b\w\b', '', user_txt)
  
  #Remove Punctuation and split 's, 't, 've with a space for filter
  user_txt = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#)|(\w+:\/\/\S+)|(\S*\d\S*)|([,;.?!:])",
                                            " ", user_txt).split())
    

  #Remove stopwords
  
  with open("STOP.txt", "r") as f:
    STOP = f.read()

  stop = STOP.split(",")

  pattern = r'\b(?:' + '|'.join(re.escape(s) for s in stop) + r')\b'
  clean = re.sub(pattern, '', user_txt)
  
  
  #mask per generare wordcloud in una forma personalizzata (opzionale per ora)
  
  #masked_im = np.array(Image.open('italy.jpg'))

  # Create and generate a word cloud image:
  wordcloud = WordCloud(width=3000, height=2000,
                        random_state=1, colormap='RdGy',
                        collocations=False, stopwords = STOPWORDS, font_path="DIN Condensed Bold.ttf",
                        mode = "RGBA", background_color=None).generate(clean)
  
  return [wordcloud, user.shape[0]]
  









