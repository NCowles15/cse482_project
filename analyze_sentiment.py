import sys
import os
import ast
import time
import json
import operator
import datetime
import math
from textblob import TextBlob
import csv
import codecs
import re

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov','dec']

def clean_tweet(tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
  
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    # print("{}: {}\n]".format(analysis,analysis.sentiment.polarity))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity < 0:
        return -1
    else:
        return 0

def clean_date(date_str):
    date_list = date_str.split()
    new_date = date_list[5]+'-'+get_month(date_list[1])+'-'+date_list[2]
    return new_date
 
def get_month(month_str):
    month_int = MONTHS.index(month_str.lower())+1
    return "{:02d}".format(month_int)  

def dates_dict_to_str(dates_dict, dates_list):
    out_str = "Date,SentimentSum\n"
    for key in dates_dict:
        out_str+="{},{}\n".format(key,dates_dict[key])
    return out_str
  
def get_listing_file():
    try:
        fp = open("twitDirFiles.txt")
        listings = [line.strip().split(' ') for line in fp]
        fp.close()
        return listings
    except:
        return []  
  
def array_to_data(file_path):
    with open(file_path, 'r') as read_file:
        data = json.load(read_file)

    # print("data from {}: {}".format(file_path,data))
    return data
  
def process_tweet(tweet, out_str, dates_list, dates_dict, sentiments_list):
    sentiment = get_tweet_sentiment(tweet['text'])
    # print("tweet {}/{}: {}".format(i, len(all_tweets), sentiment))
    new_sentiment = {}

    date_cleaned = clean_date(tweet['created_at'])

    date_real = datetime.datetime.strptime(date_cleaned, "%Y-%m-%d").strftime("%d-%m-%Y")
    if date_cleaned not in dates_dict:
        dates_dict[date_cleaned]=sentiment
    else:
        dates_dict[date_cleaned]+=sentiment
    new_sentiment['id'] = tweet['id']
    new_sentiment['date'] = date_cleaned
    new_sentiment['hashtags'] = tweet['entities']['hashtags']
    new_sentiment['text'] = tweet['text']
    new_sentiment['sentiment'] = sentiment
    
    new_sentiment_list = [str(new_sentiment['id']),new_sentiment['date'],str(new_sentiment['sentiment'])]
    new_sentiment_string = ",".join(new_sentiment_list)

    dates_list.append(date_real)
    sentiments_list.append(new_sentiment)
    return new_sentiment_string+"\n"
  
def main():
    print("loading sentiments")
    start_time = time.time()
    # all_tweets=[]
    sentiments_list = []
    dates_dict = {}
    dates_list = []
    out_str=""
    listings = get_listing_file()
    listings_new = [item[0] for item in listings]
    listings = listings_new
    local_dir = os.getcwd()
    local_twit = os.path.join(local_dir, "Twitter")
    local_twit_json = os.path.join(local_dir, "../TwitterJSON")
    for i, file in enumerate(listings):
        if i<len(listings):
            filename = file
            print("[{}] Reading file {}/{}: {}".format(datetime.datetime.now().time(), i, len(listings), filename+".json"))
            local_path = os.path.join(local_twit, filename)
            save_path = os.path.join(local_twit_json, filename+".json")
            new_data = array_to_data(save_path)
            for tweet in new_data:
                out_str += process_tweet(tweet, out_str, dates_list, dates_dict, sentiments_list)
            # all_tweets += new_data

    print("loaded sentiments after {}".format(time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))))


        
        
    with open("TweetSentiments.json", 'w+') as sentiments_file:
        json.dump(sentiments_list, sentiments_file)
        
    with open("TweetSentimentsData.csv", 'w+') as sentiments_data_file:
        sentiments_data_file.write(out_str)
    
    dates_list.sort()
    with open("TweetDates.json", 'w+') as dates_file:
        json.dump(dates_list, dates_file)
    
    with open("SentimentDates.csv", 'w+') as sentiment_dates_file:
        sentiment_dates_file.write(dates_dict_to_str(dates_dict, dates_list))

if __name__ == "__main__":
    main()