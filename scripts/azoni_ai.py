import prompts, open_ai, twitter, database, time
from collections import Counter
from textblob import TextBlob  # Simple sentiment analysis

def analyze_personality(user_handle):
    """Analyze past tweets and build a personality profile."""
    past_tweets = database.get_past_tweets_by_user(user_handle, limit=50)
    print(past_tweets)
    if not past_tweets:
        return {"topics": [], "tone": "neutral", "sentiment": "neutral"}
    
    # Analyze topics using simple keyword frequency
    all_text = " ".join(past_tweets).lower()
    keywords = ["crypto", "gaming", "ai", "nft", "humor", "tech", "finance"]
    topic_counts = Counter(word for word in all_text.split() if word in keywords)
    
    # Analyze tone and sentiment
    sentiments = [TextBlob(tweet).sentiment.polarity for tweet in past_tweets]
    avg_sentiment = sum(sentiments) / len(sentiments)
    
    # Determine tone
    if avg_sentiment > 0.2:
        tone = "positive"
    elif avg_sentiment < -0.2:
        tone = "negative"
    else:
        tone = "neutral"
    
    personality = {
        "topics": topic_counts.most_common(3),  # Top 3 topics
        "tone": tone,
        "sentiment": "positive" if avg_sentiment > 0 else "negative" if avg_sentiment < 0 else "neutral"
    }
    print(personality)
    return personality

def fact_check_with_openai(tweet_text):
    prompt = prompts.fact_check(tweet_text)
    response = open_ai.get_open_ai_response(prompt)
    return response

def fetch_and_fact_check_tweets(user_handle):
    tweet = twitter.fetch_tweet(user_handle)
    response = fact_check_with_openai(tweet)
    twitter.post_tweet(response)

def generate_fact_check_tweet(user):
    """Generate a humorous tweet using OpenAI."""
    past_tweets = database.get_past_tweets_by_user(user)
    
    print(past_tweets)
    text = ""
    prompt = prompts.funny(text, past_tweets)
    response = response = open_ai.get_open_ai_response(prompt)
    
    return response

def generate_personality_based_tweet(user_handle):
    """Generate a tweet that aligns with the user's personality."""
    personality = analyze_personality(user_handle)
    
    topics = ", ".join(topic for topic, _ in personality["topics"])
    tone = personality["tone"]
    
    prompt = f"""
    You are an AI bot with a unique personality. 
    Your personality is based on these traits:
    - Favorite topics: {topics or "random funny topics"}
    - Tone: {tone} and {personality['sentiment']} sentiment
    
    Generate a tweet that aligns with this personality. It should feel consistent with past tweets.
    Keep it under 280 characters.
    """
    
    response = response = open_ai.get_open_ai_response(prompt)
    
    return response

def post_tweet(user_handle):
    # tweet_text = generate_fact_check_tweet(user)
    tweet_text = generate_personality_based_tweet(user_handle)
    twitter.post_tweet(tweet_text)
    database.save_tweet_to_db(user_handle, tweet_text)

def reply_to_tagged(user_id):
    past_tweets = database.get_past_tweets()

    twitter.reply_to_tagged(user_id, past_tweets)

def post_reminder():
    #Opensea bot, AI improvements, buy more dogeai, improve website (add project details)
    pass

# === Step 4: Run the Bot ===
if __name__ == "__main__":
    database.initialize_db()
    #database.recreate_db()
    #database.clear_user_data("AzoniAI")
    user_handle = "azoniNFT"  # Replace with the handle of the account you want to track
    # fetch_and_fact_check_tweets(user_handle)
    post_tweet("AzoniAI")
    # while True:
    #     post_tweet()  # Post a tweet
    #     time.sleep(3600)  # Sleep for 1 hour (3600 seconds)