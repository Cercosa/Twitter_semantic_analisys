

# sending data to db
# from datetime import datetime
# from model import db
# tweet = Tweets_sentiment(hashtag='декатлон', tweet_id='3333', tweet_date=datetime(2020, 7, 5), sentiment='0.5')
# db.session.add(tweet)
# db.session.commit()

# receiving data from db

from model import Tweets_sentiment


def average_semantic_evaluation(requested_hashtag):
    semantic_evaluations = []
    tweets = Tweets_sentiment.query.filter_by(hashtag=requested_hashtag).all()
    try:
        for tweet in tweets:
            sem_evaluation = tweet.sentiment
            semantic_evaluations.append(sem_evaluation)
            result = sum(semantic_evaluations) / len(semantic_evaluations)
        return result
    except UnboundLocalError:
        print("requested hashtag does not exist")
    

if __name__ == "__main__":
    requested_hashtag = input('Input your hashtag ', )
    print(average_semantic_evaluation(requested_hashtag))
