#!/usr/bin/python

# General:
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

# We import our access keys:
from credentials import *    # This will allow us to use the keys as variables

# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def extract_maxtweets(extractor):

    # 200 tweets are extracted in a request
    # Hence repeat request until max tweets are extracted which is 3231
    # Looks for ways to go beyond extraction 3231 tweets
    # check - http://tomkdickinson.co.uk/2015/05/extracting-a-users-twitter-timeline-above-the-3-2k-limit/

    # We create a tweet list as follows:
    #tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)
    new_tweets = extractor.user_timeline(screen_name="srisri", count=200)
    print("Number of tweets extracted: {}.\n".format(len(new_tweets)))

    #save most recent tweets
    alltweets = []
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # print len(alltweets)
        # print "getting tweets before %s" % (oldest)
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = extractor.user_timeline(screen_name="srisri",count=200,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    return alltweets


# We create an extractor object:
extractor = twitter_setup()

tweets = extract_maxtweets(extractor)
print len(tweets)


#We print the most recent 5 tweets:
# print("5 recent tweets:\n")
# for tweet in tweets[:5]:
#     print(tweet.text.encode("utf-8"))
#     print()

# We create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text.encode("utf-8") for tweet in tweets], columns=['Tweets'])

# We display the first 10 elements of the dataframe:
#display(data.head(10))

# Internal methods of a single tweet object:
# print(dir(tweets[0]))

# We print info from the first tweet:
# print(tweets[0].id)
# print(tweets[0].created_at)
# print(tweets[0].source)
# print(tweets[0].favorite_count)
# print(tweets[0].retweet_count)
# print(tweets[0].geo)
# print(tweets[0].coordinates)
# print(tweets[0].entities)

# We add relevant data:
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])

# Display of first 10 elements from dataframe:
# display(data.head(10))
#print tweets[15].text.encode("utf-8")

# We extract the mean of lenghts:
mean_len = np.mean(data['len'])
mean_Likes = np.mean(data['Likes'])
mean_RTs = np.mean(data['RTs'])
# print("The lenght's average in tweets: {}".format(mean))
print("The average Likes in tweets: {}".format(mean_Likes))
print("The average retweet count of a tweet: {}".format(mean_RTs))

# We extract the tweet with more FAVs and more RTs:

fav_max = np.max(data['Likes'])
rt_max  = np.max(data['RTs'])

print mean_Likes,fav_max

for x in data.Likes:
    # if (x > 2 * mean_Likes): print x, data['Tweets'][data.Likes == x]
    if (x > 8 * mean_Likes): print x,tweets[data[data.Likes == x].index[0]].text.encode("utf-8")
exit (1)


fav = data[data.Likes == fav_max].index[0]
rt  = data[data.RTs == rt_max].index[0]

print fav_max, rt_max
print fav, rt

# Max FAVs:
print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))

# Max RTs:
print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))
