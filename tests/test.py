import tweepy
from dotenv import load_dotenv
import os
import re
from datetime import datetime, timedelta

load_dotenv()

# Set up your credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate using the Bearer Token
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_all_tweets(query, min_followers, max_results=500):
    """
    Fetch all recent tweets matching the given query.
    Excludes retweets and replies.
    """
    results = []
    next_token = None
    total_fetched = 0

    now = datetime.utcnow()
    one_minute_ago = now - timedelta(seconds=30)

    start_time = one_minute_ago.isoformat("T") + "Z"  # ISO 8601 format for 1 minute ago
    end_time = (now - timedelta(seconds=10)).isoformat("T") + "Z"  # Ensure 10 seconds earlier than current time


    while total_fetched < max_results:
        # Ensure max_results_per_request is between 10 and 100
        max_results_per_request = min(100, max(10, max_results - total_fetched))

        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "public_metrics"],
            user_fields=["username", "public_metrics"],
            expansions="author_id",
            max_results=max_results_per_request,
            start_time=start_time,
            end_time=end_time,
            next_token=next_token
        )

        if not response.data:
            break

        users = {user.id: user for user in response.includes["users"]}
        for tweet in response.data:
            author = users.get(tweet.author_id)
            if author and author.public_metrics["followers_count"] >= min_followers:
                if re.search(regex_pattern, tweet.text):
                    results.append({
                        "username": author.username,
                        "followers": author.public_metrics["followers_count"],
                        "text": tweet.text,
                        "created_at": tweet.created_at,
                        "tweet_url": f"https://twitter.com/{author.username}/status/{tweet.id}"
                    })

        total_fetched += len(response.data)
        next_token = response.meta.get("next_token")
        if not next_token:
            break
    print(total_fetched)
    return results

# Example usage
query_for_all = "*pump -is:retweet -is:reply"
regex_pattern = r"[A-Za-z0-9]+pump"  # Regex to match any characters before "pump"
min_followers_count = 100000  # Adjust as needed
max_results_to_fetch = 500  # Adjust as needed

results = fetch_all_tweets(query_for_all, min_followers_count, max_results_to_fetch)

if results:
    for result in results:
        print(f"User: @{result['username']} ({result['followers']} followers)")
        print(f"Tweet: {result['text']}")
        print(f"Posted: {result['created_at']}")
        print(f"Link: {result['tweet_url']}\n")
else:
    print("No tweets found.")