from model import Tweets_sentiment


def average_semantic_evaluation(requested_hashtag):
    semantic_evaluations = []
    tweets = Tweets_sentiment.query.filter_by(hashtag=requested_hashtag).all()
    if len(tweets) == 0:
        return "no result"
    for tweet in tweets:
        sem_evaluation = tweet.sentiment
        semantic_evaluations.append(sem_evaluation)
        result = sum(semantic_evaluations) / len(semantic_evaluations)
    return result
    

if __name__ == "__main__":
    requested_hashtag = input('Input your hashtag ', )
    print(average_semantic_evaluation(requested_hashtag))
