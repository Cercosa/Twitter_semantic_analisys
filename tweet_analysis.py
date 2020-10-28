from sentiment_analysis import sentiment_analysis
from API_hashtags_mining_1 import text_comments_mining
from model import db, Tweets_sentiment


def main():
    hashtag = input('Input your hashtag starting with "#"', )
    tweets = text_comments_mining(hashtag)
    for tweet in tweets:
        result = sentiment_analysis(tweet.text)
        print(f"Tweet: {tweet.text}.\nResult of analysis: {result}.")
        new_tweet = Tweets_sentiment(hashtag=hashtag, tweet_id=int(tweet.id), tweet_date=tweet.created_at, sentiment=float(result))
        db.session.add(new_tweet)
        db.session.commit()


if __name__ == "__main__":
    main()
