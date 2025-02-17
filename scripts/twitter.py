import tweepy
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Twitter Bearer Token
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# OAuth1 for replying to tweets (API v1.1)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter using OAuth 2.0 (Bearer Token)
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Post a Tweet
def post_tweet(tweet_text):
    try:
        print(f"Posting tweet: {tweet_text}")
        # client.create_tweet(text=tweet_text)
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

# Fetch Tweets from a User's Timeline 
def fetch_tweet(user_handle):
    """Fetch tweets from a user's timeline and fact-check them."""
    try:
        # Step 1: Convert username to user ID
        user = client.get_user(username=user_handle)  # This returns the user object with ID
        user_id = user.data.id
        print(f"User ID for {user_handle}: {user_id}")

        # Step 2: Fetch tweets using the user ID
        tweets = client.get_users_tweets(user_id, max_results=5, exclude=["replies", "retweets"])
        tweet = tweets.data[0]
        tweet_text = tweet.text
        tweet_id = tweet.id

        print(tweet_id, f"New tweet: {tweet_text}")
        return tweet_text
    
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")

def reply_to_tagged(user_id):
    pass