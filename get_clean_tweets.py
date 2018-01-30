# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:07:30 2016

@author: Ang
"""
import re
import json
import os
import pandas as pd

f = open("Trump_friends100tweets.txt","r")
f_tweet = open("Trump_friends100_cleantweets.txt", "w")

f_tweet.write('user'+'\t\t'+"user_ID"+"\t\t" + "user_name" +"\t\t"+ "user_screenname" +"\t\t" + "user_location"+"\t\t"+"user_timezone"+"\t\t"
        +"user_description"+"\t\t"+"tweettime"+"\t\t"+"tweettext"+"\t\t"+"retweet_id"+"\t\t"+"retweet_screename"+"\t\t"
        +"retweet_txt"+"\t\t"+'tweet_reply_to_id'+"\t\t"+'tweet_reply_to_screen_name'+"\t\t"
        +'tweet_mentions1'+"\t\t"+'tweet_mentions2'+"\t\t"+'tweet_hashtags1'+"\t\t"+'tweet_hashtags2'+"\n")
        
n=0
for line in f:
    n+=1
    print (n)
    line = line.strip()
    line_lst = line.split("\t\t") #split into single tweet
    user = line_lst[0]
    #f_tweet.write(str(user)+"\t")
    for tweet in line_lst[1::]:
        try:
            #tweet = tweet.strip()
            tweet_json = json.loads(tweet)
            user_ID = tweet_json['user']['id_str']
            user_name = tweet_json['user']['name'].strip().replace('\t',' ')
            user_screenname = tweet_json['user']['screen_name'].strip().replace('\n',' ').replace('\t',' ')
            user_location = tweet_json['user']['location'] if str(tweet_json['user']['location']) != 'None' else "Unknown"
            user_timezone = tweet_json['user']['time_zone'] if str(tweet_json['user']['time_zone']) != 'None' else "Unknown"
            user_description = re.sub(r'\s+',' ', tweet_json['user']['description'].strip().replace('\n',' ').replace('\t',' '))
            
            tweettime = tweet_json['created_at'] 
            tweettext = re.sub(r'\s+',' ', tweet_json['text'].strip().replace('\n',' ').replace('\t',' '))
            tweet_place = tweet_json['place'] if str(tweet_json['place']) != 'None' else "Unknown"
            tweet_coord = tweet_json['coordinates'] if str(tweet_json['coordinates']) != 'None' else "Unknown"
            tweet_geo = tweet_json['geo'] if str(tweet_json['geo']) != 'None' else "Unknown"
            
            if tweet_json['retweeted']== True: #True or False
                #if true
                retweet_id = tweet_json['retweeted_status']['id_str']
                retweet_screename = tweet_json['retweeted_status']['user']['screen_name'].strip().replace('\n',' ').replace('\t',' ')
                retweet_txt = re.sub(r'\s+',' ', tweet_json['retweeted_status']['text'].strip().replace('\n',' ').replace('\t',' '))#retweet user's text
            else:
                retweet_id = "Unknown"
                retweet_screename = "Unknown"
                retweet_txt = "Unknown"
            
            tweet_reply_to_id = tweet_json['in_reply_to_user_id_str'] if str(tweet_json['in_reply_to_user_id_str']) != 'None' else "Unknown"
            tweet_reply_to_screen_name = tweet_json['in_reply_to_screen_name'].strip().replace('\n',' ').replace('\t',' ') if str(tweet_json['in_reply_to_screen_name']) != 'None' else "Unknown"
            
            #tweet_json['entities']['user_mentions'] #return a list of mentioned
            tweet_mentions1 = (tweet_json['entities']['user_mentions'][0]['screen_name'].strip().replace('\n',' ').replace('\t',' ') if len(tweet_json['entities']['user_mentions']) >= 1 else "Unknown")
            tweet_mentions2 = (tweet_json['entities']['user_mentions'][1]['screen_name'].strip().replace('\n',' ').replace('\t',' ') if len(tweet_json['entities']['user_mentions']) >= 2 else "Unknown")
            tweet_hashtags1 = (tweet_json['entities']['hashtags'][0]['text'].strip().replace('\n',' ').replace('\t',' ') if len(tweet_json['entities']['hashtags']) >= 1 else "Unknown")
            tweet_hashtags2 = (tweet_json['entities']['hashtags'][1]['text'].strip().replace('\n',' ').replace('\t',' ') if len(tweet_json['entities']['hashtags']) >= 2 else "Unknown")
            
            f_tweet.write(str(user)+"\t\t"+str(user_ID)+"\t\t" + user_name +"\t\t"+ user_screenname.strip() +"\t\t" + str(user_location)+"\t\t"+str(user_timezone)+"\t\t"
            +str(user_description.strip().replace('\n',' ').replace('\t',' '))+"\t\t"+str(tweettime)+"\t\t"+str(tweettext.strip().replace('\n',' ').replace('\t',' '))+"\t\t"+str(retweet_id)+"\t\t"+str(retweet_screename.strip())+"\t\t"
            +str(retweet_txt.strip())+"\t\t"+str(tweet_reply_to_id)+"\t\t"+str(tweet_reply_to_screen_name)+"\t\t"
            +str(tweet_mentions1)+"\t\t"+str(tweet_mentions2)+"\t\t"+str(tweet_hashtags1)+"\t\t"+str(tweet_hashtags2)+"\n")
        
        except TypeError: #auth user
            pass

f_tweet.close()
f.close()

#===========================
#write out

friends100_tweet = pd.read_csv("Trump_friends100_cleantweets.txt", sep="\t\t",engine='python')
friends100_tweet.to_csv("Trump_friends100_cleantweets_v2.csv", index=False)

#=========================
#========================
#concat tweets together

hillary_friends100_tweet = pd.read_csv("hillary_100friends_tweets_v2.csv", encoding = "ISO-8859-1")
hillary_friends88_tweet = pd.read_csv("hillary_88friends_tweets_v2.csv", encoding = "ISO-8859-1")
hillary_friends88_tweet['mention_hillary'] = hillary_friends88_tweet['tweettext'].map(lambda x: True if "Hillary" in x or 'hillary' in x else None)
hillary_friends88_tweet['mention_Trump'] = hillary_friends88_tweet['tweettext'].map(lambda x: True if "Trump" in x or 'trump' in x else None)
hillary_friends100_tweet['mention_hillary'] = hillary_friends100_tweet['tweettext'].map(lambda x: True if "Hillary" in x or 'hillary' in x else None)
hillary_friends100_tweet['mention_Trump'] = hillary_friends100_tweet['tweettext'].map(lambda x: True if "Trump" in x or 'trump' in x else None)

frames = [hillary_friends88_tweet, hillary_friends100_tweet]
hillary_alltweets = pd.concat(frames)
hillary_alltweets.reset_index(level=0, inplace=True)
hillary_alltweets.to_csv("hillary_alltweets.csv", index=False)

trump_friends100_tweet = pd.read_csv("Trump_friends100_cleantweets_v3.csv", encoding = "ISO-8859-1")
trump_friends88_tweet = pd.read_csv("Trump_friends86_cleantweets_v3.csv", encoding = "ISO-8859-1")
frames = [trump_friends88_tweet, trump_friends100_tweet]
trump_alltweets = pd.concat(frames)
#trump_alltweets.reset_index(level=0, inplace=True)
trump_alltweets.to_csv("trump_alltweets.csv", index=False)


#===test========================
name = "168838692"

line = f.readline() #this person tweets over top 10 pages
line_lst = line.split("\t\t") #split into single tweet
user = line_lst[0]
tweet_json = json.loads(line_lst[1])

tweet_json['user']['id_str']
tweet_json['user']['name']
tweet_json['user']['screen_name']
tweet_json['user']['location']
tweet_json['user']['time_zone']
tweet_json['user']['description']

tweet_json['created_at']
tweet_json['text']
tweet_json['place']
tweet_json['coordinates']
tweet_json['geo']

tweet_json['retweeted']#True or False
#if true
tweet_json['retweeted_status']['id_str']
tweet_json['retweeted_status']['user']['screen_name']
tweet_json['retweeted_status']['text']#retweet user's text

tweet_json['in_reply_to_user_id_str']
tweet_json['in_reply_to_screen_name']

#tweet_json['entities']['user_mentions'] #return a list of mentioned
mentions1 = [(tweet_json['entities']['user_mentions'][0]['screen_name'] if len(tweet_json['entities']['user_mentions']) >= 1 else None)]
mentions2 = [(tweet_json['entities']['user_mentions'][1]['screen_name'] if len(tweet_json['entities']['user_mentions']) >= 2 else None)]
hashtags1 = [(tweet_json['entities']['hashtags'][0]['text'] if len(tweet_json['entities']['hashtags']) >= 1 else None)]
hashtags2 = [(tweet_json['entities']['hashtags'][1]['text'] if len(tweet_json['entities']['hashtags']) >= 2 else None)]

#mentions1 = [(T['entities']['user_mentions'][0]['screen_name'] if len(T['entities']['user_mentions']) >= 1 else None) for T in tweet_json]
#mentions2 = [(T['entities']['user_mentions'][1]['screen_name'] if len(T['entities']['user_mentions']) >= 2 else None) for T in tweet_json]
#hashtags1 = [(T['entities']['hashtags'][0]['text'] if len(T['entities']['hashtags']) >= 1 else None) for T in tweet_json]
#hashtags2 = [(T['entities']['hashtags'][1]['text'] if len(T['entities']['hashtags']) >= 2 else None) for T in tweet_json]

