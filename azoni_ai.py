import tweepy
import openai
from dotenv import load_dotenv
import os
import time

# Load the .env file
load_dotenv()

# === Step 1: Setup Twitter API ===
# Replace with your Twitter Bearer Token
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# OAuth1 for replying to tweets (API v1.1)
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter using OAuth 2.0 (Bearer Token)
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Replace with your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def fact_check_with_openai(tweet_text):
    """Use OpenAI's GPT model to analyze and fact-check a tweet."""
    prompt = f"""
    You are an AI trained to fact-check statements based on your extensive knowledge base.
    If there is nothing to fact check then make a funny comment based on the content.
    A user tweeted:
    "{tweet_text}"

    1. Analyze the tweet and identify any claims that can be fact-checked.
    2. Fact-check the claims using your knowledge and provide accurate corrections.
    3. Simulate reputable sources or suggest references for further reading.

    Format your response like this:
    Start with a greeting and introduction as an AI based on the content of the twwet then do the following;
    Statement: [The specific claim being fact-checked]

    Response: [The verified information, with corrections if needed]


    Sources: [Provide realistic citations or suggest areas to verify]

    Summary: [A concise Twitter-friendly reply]
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the newer chat-based model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,          # Optional: control response length
        temperature=0.5          # Optional: creativity control
    )
    return response['choices'][0]['message']['content'].strip()  # Return the text of the first choice

# === Step 3: Fetch Tweets from a User's Timeline ===
def fetch_and_fact_check_tweets(user_handle):
    """Fetch tweets from a user's timeline and fact-check them."""
    try:
        # Step 1: Convert username to user ID
        # user = client.get_user(username=user_handle)  # This returns the user object with ID
        user_id = 1442171217859907593 #user.data.id
        print(f"User ID for {user_handle}: {user_id}")

        # Step 2: Fetch tweets using the user ID
        tweets = client.get_users_tweets(user_id, max_results=5, exclude=["replies", "retweets"])
        tweet = tweets.data[0]
        tweet_text = tweet.text
        tweet_id = tweet.id
        # user_handle = tweet.author_id  # Twitter handles are accessed through author_id in API v2
        print(tweet_id, f"New tweet: {tweet_text}")
        # Post the response as a reply
        try:
            response_text = fact_check_with_openai(tweet_text)
            # Post the response as a reply using the correct method
            reply = f"@{user_handle}\n{response_text}"
            print(reply)
            client.create_tweet(text=reply, in_reply_to_tweet_id=tweet_id)
            

        except tweepy.TweepyException as e:
            print(f"Error generating or posting response: {e}")
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {e}")

# === Step 4: Run the Bot ===
if __name__ == "__main__":
    user_handle = "azoniNFT"  # Replace with the handle of the account you want to track
    fetch_and_fact_check_tweets(user_handle)
    #post_tweet("Hello")