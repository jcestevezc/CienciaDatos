'''
Created on 26/10/2018

@author: CO1012351486
'''

import tweepy
import re
import unidecode
import psycopg2

connection  = psycopg2.connect(
    host="localhost",
    database="data_science", 
    user="postgres", 
    password="root"
)


consumer_key = 'NHAvRKM84myniXPn8FnWi5UZp'
consumer_secret = 'jBOpoWC6xUI42VTg5HNWtqLRqpAKXUFInAEkEkmMT7sLCx8YrL'
access_token = '927301438207864832-o6PIyvPVkPanQyLJQIRHmMTHVWfZViw'
access_token_secret = 'otFwtI872mvQ6oX0CozWyEpEdTlmWQaDpgjOiJdZBbgiG'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def clean(text):
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub('[-!"#$%&()*+,./:;<=>?@\[\\\]_`{|}~]+', '', text)
    #text = re.sub('[ ]+', '_', text)
    text.replace("\n", "")
    text.replace("  ", "")
    text.replace("\t", "")
    text.replace("\r", "")
    print('Texto con reemplazos')
    print(text)
    return text

def main():
    
    cursor = connection.cursor()
    sql_twitter = 'INSERT INTO "DS_TWITTER_DATA" (user_name, user_location, user_followers_count, user_friends_count, user_time_zone, user_following, geo, coordinates, place, full_text, retweet_count, favorite_count, language, created_at, id_tweet,clean_text) VALUES ('

    for tweet in tweepy.Cursor(api.search,q="@RevistaSemana",count=100,lang="es",since="2018-09-03", tweet_mode='extended').items():
        cleanText = clean(str(tweet.full_text))
        sql_twitter = sql_twitter +"'"+ str(tweet.user.name) + "','"+ str(tweet.user.location) + "','"+ str(tweet.user.followers_count) + "','"+ str(tweet.user.friends_count) + "','"+ str(tweet.user.time_zone) + "','"+ str(tweet.user.following) +"','"+ str(tweet.geo) + "','"+ str(tweet.coordinates) + "','" + str(tweet.place) + "','" + str(tweet.full_text) + "','"+ str(tweet.retweet_count) + "','"+ str(tweet.favorite_count) + "','"+ str(tweet.lang) + "','"+ str(tweet.created_at) + "','"+ str(tweet.id) + "','"+ cleanText +"');"
        cursor.execute(sql_twitter)
        break
    
    connection.commit()
    cursor.close()
    connection.close()

main()
    #datos['Date'] = datos.Date.str.replace(r'[a-z]+', '')