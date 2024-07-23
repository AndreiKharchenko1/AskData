from flask import Flask, render_template, request
import google.generativeai as genai
import os
from ResponseAugmentation import *
from QueryAugmentation import *
from BusinessDomains import *
from DataWrangler import DataWrangler
from databasetest import *

# loading the .env file so that the API_KEY is available
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set. Please set the environment variable.")
    exit()

# the rest:
app = Flask(__name__)
dw = DataWrangler(GEMINI_API_KEY)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

standard_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                   'supporting other data professionals with your experience and knowledge. '
                   'You are trained to help Data Professionals at Ketchup Clinic, an extensive' 
                   ' Clinic System that spans the US, and should help the employees in their everyday data tasks.'
                   'Always consider your Data Management Experience but remember that you are a chatbot.'
                   'This is the task that their question: ')

domain_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                 'supporting other data professionals with your experience and knowledge. '
                 'You are trained to help Data Professionals at Ketchup Clinic, an extensive'
                 ' Clinic System that spans the US, and should help the employees in their everyday data tasks.'
                 'Always consider your Data Management Experience but remember that you are a chatbot.'
                 'Consider that their question is related to the {} department of Ketchup Clinic.'
                 'This is their question: ')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    global domain_prompt, standard_prompt
    # get user input
    user_input = request.form['user_input']

    # perform query augmentation on user input
    user_input_augmented = query_augmentation(user_input)

    if user_input_augmented == 'invalid':
        response = 'Invalid input. Please try again with a question that is related to Data Management.'
    else:
        # check for business domains
        business_domain = get_business_domain(user_input)

        if business_domain == 'no domain':
            # Generate response using Data Wrangler
            data_response = dw.generate_response(user_input)
            response = model.generate_content(standard_prompt + user_input_augmented + '\n' + data_response)
            response = response.text
        else:
            # generate domain-specific response
            domain_prompt = domain_prompt.format(business_domain)
            data_response = dw.generate_response(user_input)
            response = model.generate_content(domain_prompt + user_input_augmented + '\n' + data_response)
            response = response.text


    print("response: ", response)

    extracted_sql = extractSQL(response)
    for sql in extracted_sql:
        formatted_sql_result = testQuery(sql)
        if formatted_sql_result != None: # & len(extracted_sql) == 1:
            response = response + '\n\n' + "For Ketchup Clinic, this SQL returns the following data:" + '\n' + formatted_sql_result

        else:
            response = response + '\n' + sql + '\n\n' + "For Ketchup Clinic, this SQL did not return a valid result, please test it before using it."


    response = response_augmentation(response)
    response = transform_to_html(response)

    return response


if __name__ == '__main__':
    app.run(debug=True)
