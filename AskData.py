import google.generativeai as genai
from dotenv import load_dotenv
import os
from ResponseAugmentation import *
from QueryAugmentation import *
from BusinessDomains import *

# this is to test it in the console...

# GOOGLE'S GEMINI API

# loading the .env file so that the API_KEY is available
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set. Please set the environment variable.")
    exit()

# configuring the model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# defining a standard prompt that is submitted with every user input
standard_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                   'supporting other data professionals with your experience and knowledge. '
                   'Always consider your Data Management Experience but remember that you are a chatbot.'
                   'This is the data task that they need help with: ')

domain_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                 'supporting other data professionals with your experience and knowledge. '
                 'You are trained to help Data Professionals at Ketchup Clinic, an extensive'
                 ' Clinic System that spans the US, and should help the employees in their everyday data tasks.'
                 'Always consider your Data Management Experience but remember that you are a chatbot.'
                 'Consider that their question is related to the {} department of Ketchup Clinic.'
                 'This is their question: ')


# get user input and model's response
while True:
    user_input = input("Chat with AskData... (enter 'stop' to exit): ")

    # get user input
    if user_input.lower() == 'stop':
        print("Thank you for chatting with AskData.")
        break

    # perform query augmentation on user input
    user_input_augmented = query_augmentation(user_input)

    print("user input after validation", user_input_augmented)

    if user_input_augmented == 'invalid':
        response = 'Invalid input. Please try again with a question that is related to Data Management.'
    else:
        # check for business domains
        business_domain = get_business_domain(user_input)

        if business_domain == 'no domain':
            # Generate response
            print("model receives: ", standard_prompt + user_input_augmented)
            response = model.generate_content(standard_prompt + user_input_augmented)
            response = response.text
        else:
            domain_prompt = domain_prompt.format(business_domain)
            print("model receives: ", domain_prompt + user_input_augmented)
            response = model.generate_content(domain_prompt + user_input_augmented)
            response = response.text

    # perform response augmentation
    response = response_augmentation(response)

    # print final response to user
    print(response)
