import tweepy
import settings


hashtag = input('Input your hashtag starting with "#"', )

auth = tweepy.OAuthHandler(settings.API_key, settings.API_secret_key)

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100).items():
    print(tweet.text)
    pass



