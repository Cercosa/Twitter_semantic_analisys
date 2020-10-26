from flask import Flask, render_template, request
from form import RequestForm

import sys
import os

if sys.platform.lower() == 'win32':  # to display correctly in the console
    os.system('color')

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def main_page():
    user_request = RequestForm()
    return render_template('start_page.html', form=user_request)

@app.route('/result', methods=['POST'])
def result_page():
    result = request.form
    key_word = result['company']
    return render_template('result_page.html', key_word=key_word)


if __name__ == "__main__":
    app.run(debug=True)
