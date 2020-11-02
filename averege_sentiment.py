from model import Tweets_sentiment

# sending data to db
# from datetime import datetime
# from model import db
# tweet = Tweets_sentiment(hashtag='декатлон', tweet_id='3333', tweet_date=datetime(2020, 7, 5), sentiment='0.5')
# db.session.add(tweet)
# db.session.commit()

# receiving data from db


def average_semantic_evaluation():
    semantic_evaluations = []
    tweets = Tweets_sentiment.query.all()
    for tweet in tweets:
        sem_evaluation = tweet.sentiment
        semantic_evaluations.append(sem_evaluation)
    return(sum(semantic_evaluations) / len(semantic_evaluations))


if __name__ == "__main__":
    print(average_semantic_evaluation())
