import tweepy
import settings
from sentiment_analysis import get_model_tokenizer, get_sequences
from model import db, Tweets_sentiment
auth = tweepy.OAuthHandler(settings.API_key, settings.API_secret_key)


def text_comments_mining(hashtag):
    api = tweepy.API(auth)
    model, tokenizer = get_model_tokenizer()
    for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100).items():
        result = model.predict(get_sequences(tokenizer, [tweet.text]))
        print(f"Tweet: {tweet.text}.\nResult of analysis: {result}.")
        new_tweet = Tweets_sentiment(hashtag=hashtag, tweet_id=int(tweet.id), tweet_date=tweet.created_at, sentiment=float(result))
        db.session.add(new_tweet)
    db.session.commit()


if __name__ == "__main__":
    hashtag = input('Input your hashtag starting with "#"', )
    tweets = text_comments_mining(hashtag)
