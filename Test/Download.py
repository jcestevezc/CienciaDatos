'''
Created on 26/10/2018

@author: CO1012351486
'''

import tweepy
import csv
import pandas as pd
import psycopg2

connection  = psycopg2.connect(
    host="localhost",
    database="data_science", 
    user="postgres", 
    password="root"
)
####input your credentials here
consumer_key = 'NHAvRKM84myniXPn8FnWi5UZp'
consumer_secret = 'jBOpoWC6xUI42VTg5HNWtqLRqpAKXUFInAEkEkmMT7sLCx8YrL'
access_token = '927301438207864832-o6PIyvPVkPanQyLJQIRHmMTHVWfZViw'
access_token_secret = 'otFwtI872mvQ6oX0CozWyEpEdTlmWQaDpgjOiJdZBbgiG'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


cursor = connection.cursor()
#sql_digital_press = 'INSERT INTO "DS_DIGITAL_PRESS" ("TITLE", "AUTHOR", "DATE", "MEDIO", "TYPE_ARTICLE", "KEY_WORDS","CONTENT")  VALUES ('
sql_twitter = 'INSERT INTO "DS_TWITTER_DATA" (user_name, user_location, user_followers_count, user_friends_count, user_time_zone, user_following, geo, coordinates, place, full_text, retweet_count, favorite_count, language, created_at, id_tweet) VALUES ('


csvFile = open('data.csv', 'a')
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="@RevistaSemana",count=100,lang="es",since="2018-09-03", tweet_mode='extended').items():
    #print (tweet.created_at, tweet.text)
    csvWriter.writerow([
                        tweet.id,
                        tweet.user.name.encode('utf-8'),
                        tweet.user.location.encode('utf-8'),
                        tweet.user.followers_count,
                        tweet.user.friends_count,
                        tweet.user.time_zone,
                        tweet.user.following,
                        tweet.geo,
                        tweet.coordinates,
                        tweet.place,
                        tweet.full_text.encode("utf-8"),
                        tweet.retweet_count,
                        tweet.favorite_count,
                        #tweet.text.encode('utf-8'),
                        tweet.lang,
                        tweet.created_at])
    sql_twitter = sql_twitter +"'"+ str(tweet.user.name.encode('utf-8')).replace("b'", "") + "','"+ str(tweet.user.location.encode('utf-8')) + "','"+ str(tweet.user.followers_count) + "','"+ str(tweet.user.friends_count) + "','"+ str(tweet.user.time_zone) + "','"+ str(tweet.user.following) +"','"+ str(tweet.geo) + "','"+ str(tweet.coordinates) + "','" + str(tweet.place) + "','" + str(tweet.full_text.encode("utf-8")) + "','"+ str(tweet.retweet_count) + "','"+ str(tweet.favorite_count) + "','"+ str(tweet.lang) + "','"+ str(tweet.created_at) + "','"+ str(tweet.id) +"');"
    print(sql_twitter)
    #cursor.execute(sql_twitter)
    break
    