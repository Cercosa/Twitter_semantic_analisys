from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'tweets.db')
db = SQLAlchemy(app)


class Tweets_sentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String, nullable=False)
    tweet_id = db.Column(db.Integer, unique=True, nullable=False)
    tweet_date = db.Column(db.DateTime, nullable=False)
    sentiment = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        return '<Analysis {} {}>'.format(self.tweet_id, self.sentiment)
