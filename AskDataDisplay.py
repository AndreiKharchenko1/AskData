from flask import Flask, render_template, request
import google.generativeai as genai
import os

# loading the .env file so that the API_KEY is available
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set. Please set the environment variable.")
    exit()

# the rest:
app = Flask(__name__)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

standard_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                   'supporting other data professionals with your experience and knowledge. '
                   'Always consider your Data Management Experience but remember that you are a chatbot.'
                   'This is the task that they need help with: ')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']

    # Generate response
    response = model.generate_content(standard_prompt + user_input)
    return response.text


if __name__ == '__main__':
    app.run(debug=True)
