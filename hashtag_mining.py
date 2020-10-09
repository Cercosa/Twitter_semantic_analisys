import tweepy
import settings 
auth = tweepy.OAuthHandler(settings.API_key, settings.API_secret_key)

def text_comments_mining(hashtag):
    
    api = tweepy.API(auth)
    
    for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100).items(5):
        print(tweet.text)
        pass
    return hashtag

if __name__=="__main__":
    hashtag = input('Input your hashtag starting with "#"' , )
    text_comments_mining(hashtag)



