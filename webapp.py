from flask import Flask, render_template, request
from form import RequestForm
from averege_sentiment import average_semantic_evaluation
from db import db
from API_hashtags_mining_1 import text_comments_mining
import sys
import os


if sys.platform.lower() == 'win32':  # to display correctly in the console
    os.system('color')


app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


@app.route('/')
def main_page():
    user_request = RequestForm()
    return render_template('start_page.html', form=user_request)


@app.route('/result', methods=['POST'])
def result_page():
    result = request.form
    key_word = result['company']
    text_comments_mining(key_word)
    analysis = average_semantic_evaluation(key_word)
    return render_template('result_page.html', key_word=key_word, sentiment_result=analysis)


if __name__ == "__main__":
    app.run(debug=True)
