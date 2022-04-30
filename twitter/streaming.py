import json
import tweepy
import boto3
import random
from secret import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

client = boto3.client('firehose', region_name = 'us-east-1', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

twitter_api_key =TWITTER_API_KEY
twitter_api_secret_key =  TWITTER_API_SECRET_KEY
twitter_access_token = TWITTER_ACCESS_TOKEN
twitter_access_token_secret =  TWITTER_ACCESS_TOKEN_SECRET


class SimpleStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id)
        tweet = json.dumps({'id': status.id, 'created_at': status.created_at, 'text': status.text}, default=str)

        try:
            response = client.put_record(Record={'Data': f'{tweet}\n'}, DeliveryStreamName='PUT-RED-TWEET')
        
        except Exception as ex:
            print(ex)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

stream_listener = SimpleStreamListener()

auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

twitterStream = tweepy.Stream(auth, stream_listener)
twitterStream.filter(track=['Bitcoin',])