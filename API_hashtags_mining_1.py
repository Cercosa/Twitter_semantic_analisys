import tweepy
import settings
auth = tweepy.OAuthHandler(settings.API_key, settings.API_secret_key)


def text_comments_mining(hashtag):
    api = tweepy.API(auth)
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100).items(5):
        all_tweets.append(tweet.text)
    return all_tweets


if __name__ == "__main__":
    hashtag = input('Input your hashtag starting with "#"', )
    tweets = text_comments_mining(hashtag)
    print(len(tweets))
