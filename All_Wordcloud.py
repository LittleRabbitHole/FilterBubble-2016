#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:08:04 2016
this is to plot the hashtag world cloud
@author: angli
"""

import os
#import codecs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread

#hillary side mentioned hillary
hillary_alltweets=pd.read_csv("hillary_alltweets.csv")
hillary_alltweets.columns.values
hillary_harshtags = hillary_alltweets[['tweet_hashtags1', 'tweet_hashtags2','mention_hillary', 'mention_Trump']]
#hillary_harshtags = hillary_harshtags.query('mention_hillary == True or mention_Trump == True ')
hillary_harshtags = hillary_harshtags.query('mention_hillary == True')
hillary_harshtags1 = list(hillary_harshtags.query('tweet_hashtags1 != "Unknown" ')['tweet_hashtags1'])
hillary_harshtags2 = list(hillary_harshtags.query('tweet_hashtags2 != "Unknown" ')['tweet_hashtags2'])
all_hillary_harshtags = hillary_harshtags1 + hillary_harshtags2
all_hillary_harshtags=" ".join(all_hillary_harshtags)



twitter_mask = imread('./twitter_mask.png', flatten=True)

wordcloud = WordCloud(
                      font_path='~/cabin-sketch-v1.02/CabinSketch-Bold.ttf',
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=twitter_mask
            ).generate(all_hillary_harshtags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./all_hillary_harshtags_wordcloud.png', dpi=300)
plt.show()

#hillary side mentioned Trump
hillary_harshtags = hillary_alltweets[['tweet_hashtags1', 'tweet_hashtags2','mention_hillary', 'mention_Trump']]
#hillary_harshtags = hillary_harshtags.query('mention_hillary == True or mention_Trump == True ')
hillary_harshtags = hillary_harshtags.query('mention_Trump == True')
hillary_harshtags1 = list(hillary_harshtags.query('tweet_hashtags1 != "Unknown" ')['tweet_hashtags1'])
hillary_harshtags2 = list(hillary_harshtags.query('tweet_hashtags2 != "Unknown" ')['tweet_hashtags2'])
all_hillary_harshtags = hillary_harshtags1 + hillary_harshtags2
all_hillary_harshtags=" ".join(all_hillary_harshtags)


twitter_mask = imread('./twitter_mask.png', flatten=True)

wordcloud = WordCloud(
                      font_path='~/cabin-sketch-v1.02/CabinSketch-Bold.ttf',
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=twitter_mask
            ).generate(all_hillary_harshtags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./all_hillary_harshtags_wordcloud_Trump.png', dpi=300)
plt.show()



