import sqlite3

def initialize_db():
    """Create a SQLite database to store tweets by user."""
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_handle TEXT NOT NULL,
            tweet_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def recreate_db():
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tweets")
    cursor.execute("""
        CREATE TABLE tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_handle TEXT NOT NULL,
            tweet_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_tweet_to_db(user_handle, tweet_text):
    """Save a tweet and its user handle to the SQLite database."""
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tweets (user_handle, tweet_text) VALUES (?, ?)", (user_handle, tweet_text))
    conn.commit()
    conn.close()


def get_past_tweets_by_user(user_handle, limit=10):
    """Retrieve past tweets from the database for a specific user."""
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tweet_text FROM tweets 
        WHERE user_handle = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (user_handle, limit))
    past_tweets = [row[0] for row in cursor.fetchall()]
    conn.close()
    return past_tweets

def clear_user_data(user_handle):
    """Delete all tweets for a specific user from the database."""
    conn = sqlite3.connect("tweets.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tweets WHERE user_handle = ?", (user_handle,))
    conn.commit()
    conn.close()
    print(f"All data for user '{user_handle}' has been deleted.")