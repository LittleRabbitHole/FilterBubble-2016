# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 09:36:59 2016
@author: angli
"""

import tweepy
import json
import os


# Variables that contains the user credentials to access Twitter API
CONSUMER_KEY    = 
CONSUMER_SECRET = 
ACCESS_TOKEN    = 
ACCESS_TOKEN_SECRET = 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)
#api2 = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60,parser=tweepy.parsers.JSONParser())
#http://docs.tweepy.org/en/v3.5.0/api.html#api-reference

#get my timeline
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)


#get users' most recent tweets  
user = api.user_timeline(screen_name = "KLSouth", count=10, parser=tweepy.parsers.JSONParser())

#get the users' followers
followers = api.followers(screen_name = "Fei-Fei Li",parser=tweepy.parsers.JSONParser())
followers['users'][0]

def get_followers(user_id):
    users = []
    page_count = 0
    for user in tweepy.Cursor(api.followers, id=user_id, count=100).pages():
        page_count += 1
        if page_count==10: break
        print ('Getting page {} for followers'.format(page_count))
        users.extend(user)
    return users
    
def get_friends(user_id):
    users = []
    page_count = 0
    for user in tweepy.Cursor(api.friends, id=user_id, count=100).pages():
        page_count += 1
        if page_count==10: break
        print ('Getting page {} for friends'.format(page_count))
        users.extend(user)
    return users

def get_followers_ids(user_id):
    ids = []
    page_count = 0
    for page in tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages():
        page_count += 1
        if page_count==10: break
        print ('Getting page {} for followers ids'.format(page_count))
        ids.extend(page)
    return ids

def get_friends_ids(user_id):
    ids = []
    page_count = 0
    for page in tweepy.Cursor(api.friends_ids, id=user_id, count=5000).pages():
        page_count += 1
        if page_count==10: break
        print ('Getting page {} for friends ids'.format(page_count))
        ids.extend(page)
    return ids

followers = get_followers_ids("lyndarowe12")
following = get_friends_ids("lyndarowe12")

# bi-diractory friendship of jeremiah3525
friends1 = list(set(followers) & set(following))

f = open("lyndarowe12.txt", "w")
for item in friends1:
    f.write(str(item)+",")
f.close()

def bi_directary_friends(user_id):
    followers = get_followers_ids(user_id)
    following = get_friends_ids(user_id)
    friend_lst = list(set(followers) & set(following))
    return friend_lst 

#---------------------------------------------------
#----will last long
# for evert friend in frienbi-diractary friendship of level1 friend
friends_level2 = {}
n=0
for friend in friends1:
    n+=1
    print (n)
    if n>90: break
    try:
        friend_2 = bi_directary_friends(friend)
        friends_level2[friend] = friend_2
    except tweepy.TweepError:
        pass
#------------------
#write out
f_original = open('friends_Trump.txt', 'w')
f_friends = open('friendslist_Trump.txt', 'w')

for key, list in friends_level2.items():
    f_original.write(str(key)+"\n")
    for item in list:
        f_friends.write(str(item)+",")
    f_friends.write("\n")

f_original.close()
f_friends.close()   
#------------------------

f_friend1 = open('friends_Trump.txt', 'r') #friends86
level1_friends = f_friend1.readlines()    

f_friend2 = open('friendslist_Trump.txt', 'r') 
level2_friends = f_friend2.readlines()

level2_friends_lst = []
for friendline in level2_friends:
    friends = friendline.split(",")
    level2_friends_lst.append(friends)

#--------
#count the most popular friends
flat_friendslst_level2 = sum(level2_friends_lst, [])
from collections import Counter
count_dict = Counter(flat_friendslst_level2)
top100 = [x[0] for x in Counter(flat_friendslst_level2).most_common(101)]
f_top100= open('Top100list_Trump.txt', 'w')
for userID in top100:
    f_top100.write(str(userID)+",")
f_top100.close()

common_friends_lst = []
for friend_lst in level2_friends_lst:
    common_friends = list(set(friend_lst) & set(top100))
    common_friends_lst.append(common_friends)

f_common= open('commonfriendslist_Trump.txt', 'w')
for i in range(len(common_friends_lst)):
    f_common.write(str(level1_friends[i].strip())+",")
    for item in common_friends_lst[i]:
        f_common.write(str(item)+",")
    f_common.write("\n")
f_common.close()
   

# get users' most recent tweets  
# user = api.user_timeline(screen_name = "KLSouth", count=10, parser=tweepy.parsers.JSONParser())

def get_timeline(user_id):
    timeline = []
    page_count = 0
    for page in tweepy.Cursor(api.user_timeline, id=user_id, count=200).pages():
        page_count += 1
        if page_count==10: break
        print ('Getting page {} for followers ids'.format(page_count))
        timeline.extend(page)
    return timeline


#----------------
f = open("friends86_Trump.txt","r")
allnames = f.readlines()
namelist = [x.strip() for x in allnames]
f.close()


friends_tweets_dict={}
n=0
for friend in namelist:
    n+=1
    print (n)
    if friend != "":
        try:
        # get the tweets for one friend    
            friend_timeline = get_timeline(friend)
            #get the data into Json
            timeline=[]
            for item in friend_timeline:
                timeline.append(item._json)
            # insert into data dictionary
            friends_tweets_dict[friend] = timeline
        except tweepy.TweepError:
            friends_tweets_dict[friend] = "Autheticate User"

f= open('Trump_friends86_tweets.txt', 'w')
for key, list in friends_tweets_dict.items():
    print (key)
    f.write(str(key)+"\t\t")
    for item in list:
        f.write(json.dumps(item)+"\t\t")
    f.write("\n")
f.close()  
#------------------

f = open("Top100list_Trump.txt","r")
allnames = f.readlines()
namelist = allnames[0].split(",")
f.close()


friends_tweets_dict={}
n=0
for friend in namelist:
    n+=1
    print (n)
    if friend != "":
        try:
            # get the tweets for one friend
            friend_timeline = get_timeline(friend)
            #get the data into Json
            timeline=[]
            for item in friend_timeline:
                timeline.append(item._json)
            # insert into data dictionary
            friends_tweets_dict[friend] = timeline
        except tweepy.TweepError:
            friends_tweets_dict[friend] = "Autheticate User"


f= open('Trump_friends100tweets.txt', 'w')
for key, list in friends_tweets_dict.items():
    print (key)
    f.write(str(key)+"\t\t")
    for item in list:
        f.write(json.dumps(item)+"\t\t")
    f.write("\n")
f.close()  


"https://dev.twitter.com/rest/reference/get/users/suggestions"
"https://dev.twitter.com/rest/reference/get/statuses/user_timeline"



    


#--------------------------------------------------------------------------------
#search based on query
query = "steeler"
tweets = api.search(q=query, result_type='recent', lang='en', count=10,
                    parser=tweepy.parsers.JSONParser())

tweets['statuses'][0]['user']['name']
tweets['statuses'][0]['user']['screen_name']
tweets['statuses'][0]['user']['location']
tweets['statuses'][0]['user']['time_zone']
tweets['statuses'][0]['user']['description']

tweets['statuses'][0]['created_at']
tweets['statuses'][0]['text']
tweets['statuses'][0]['place']
tweets['statuses'][0]['coordinates']
tweets['statuses'][0]['geo']

#check the time, earliest one start with index [-1], last one is [0]
tweets['statuses'][0]['created_at'] # this is the most recent tweet
tweets['statuses'][-1]['created_at']#this is the oldest tweet 

#when do the loop, need to set the max_id=last call's oldest time id to catch the older data
oldest_id = tweets['statuses'][-1]['id']

#second call
#check to see the second call, this will return same result as the first call
twitter2 = api.search(q="steeler",result_type='recent', lang='en', count=100, 
                            max_id=oldest_id, parser=tweepy.parsers.JSONParser())
#Check the time
twitter2['statuses'][0]['created_at'] 
twitter2['statuses'][-1]['created_at'] #this is the oldest tweet for this turn

#function to get the tweets json
def get_tweet(query, max_id):
    t = api.search(q=query, result_type='recent', lang='en', count=100, 
                            max_id=max_id, parser=tweepy.parsers.JSONParser())
    return t

#write the tweets json
f_original = open('original_tweets.txt', 'w')

#first batch
first_batch = get_tweet("steeler", "")
f_original.write(json.dumps(first_batch)+"\n")

#udpate oldest_id
oldest_id = first_batch['statuses'][-1]['id']

#15 calls per time ->oct 17(id=788085227348299776)---oct 26
for i in range(14):
    ith_batch = get_tweet("steeler", oldest_id-1)
    f_original.write(json.dumps(ith_batch)+"\n")
    oldest_id = ith_batch['statuses'][-1]['id']#udpate oldest_id

f_original.close()

#write out
f = open('user_tweets.txt', 'w')
f.write("user_name"+"\t"+"user_creen_name"+"\t"+"user_location"+"\t"+"user_timezone"+"\t"+"user_description"
        +"\t" + "tweet_created_at"+"\t"+"tweet_text"+"\t"+"tweet_place"+"\t"+"tweet_coordinates"+"\t"
        +"tweet_geo"+"\n")

def clean_tweet(original_tweets):
    tweets = original_tweets['statuses']
    for i in range(len(tweets)):
        user_name = tweets['statuses'][i]['user']['name']
        user_screen_name = tweets['statuses'][i]['user']['screen_name']
        user_location = tweets['statuses'][i]['user']['location']
        user_timezone = tweets['statuses'][i]['user']['time_zone']
        user_description = tweets['statuses'][i]['user']['description']
        tweet_created_at = tweets['statuses'][i]['created_at']
        tweet_text = tweets['statuses'][i]['text']
        tweet_place = tweets['statuses'][i]['place']
        tweet_coordinates = tweets['statuses'][i]['coordinates']
        tweet_geo = tweets['statuses'][i]['geo']
        f.write(user_name+"\t"+user_screen_name+"\t"+user_location+"\t"+user_timezone+"\t"+user_description
                +"\t"+tweet_created_at+"\t"+tweet_text+"\t"+tweet_place+"\t"+tweet_coordinates+"\t"
                +tweet_geo+"\n")


f.close()    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
