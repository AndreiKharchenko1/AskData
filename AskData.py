import google.generativeai as genai
from dotenv import load_dotenv
import os

#this is to test in the console...

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

# defining a standard prompt that is submitted with every user input.
standard_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                   'supporting other data professionals with your experience and knowledge. '
                   'Always consider your Data Management Experience but remember that you are a chatbot.'
                   'This is the task that they need help with: ')

research_prompt_genetics = ('You are an experienced Geneticist well versed in bioinformatics '
                   'This is the genetics related question you have been asked to help with: ')


research_prompt_socmed = ('You are an experienced Social Media Analyst who knows a lot about the current topics of interest among users '
                   'This is the social media related question you have been asked to help with: ')
# get user input and model's response
while True:
    user_input = input("Chat with AskData... (enter 'stop' to exit): ")

    # get user input
    if user_input.lower() == 'stop':
        print("Thank you for chatting with AskData.")
        break

   # Generate & print model response
    if 'social' in user_input.lower() or 'media' in user_input.lower():
        response = model.generate_content(research_prompt_socmed + user_input)
    elif any(keyword in user_input.lower() for keyword in ['genetics', 'bio', 'dna', 'allele', 'snp', 'chromos']):
        response = model.generate_content(research_prompt_genetics + user_input)
    else:
        response = model.generate_content(standard_prompt + user_input)
    print(response.text)
