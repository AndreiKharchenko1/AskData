from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from DataWrangler import DataWrangler

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set. Please set the environment variable.")
    exit()

# File paths for the CSV files
file_paths = {
    'clinic_location_table': '/Users/danielazafrani/AskData/data/clinic_location_table_DP.csv',
    'clinic_profitability_table': '/Users/danielazafrani/AskData/data/clinic_profitability_table_DP.csv',
    'employee_table': '/Users/danielazafrani/AskData/data/employee_table_DP.csv',
    'patient_appointment_table': '/Users/danielazafrani/AskData/data/patient_appointment_table_DP.csv',
    'patient_table': '/Users/danielazafrani/AskData/data/patient_table_DP.csv',
    'physician_table': '/Users/danielazafrani/AskData/data/physician_table_DP.csv',
    'treatments_costs_table': '/Users/danielazafrani/AskData/data/treatments_costs table_DP.csv'
}

# Initialize DataWrangler
data_wrangler = DataWrangler(file_paths)

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

standard_prompt = ('You are an experienced Data Professional in Enterprise Data Management '
                   'supporting other data professionals with your experience and knowledge. '
                   'You are trained to help Data Professionals at Ketchup Clinic, an extensive'
                   ' Clinic System that spans the US, and should help the employees in their everyday data tasks.'
                   'Always consider your Data Management Experience but remember that you are a chatbot.'
                   'Generate a SQL query to address the following task: ')

@app.before_request
def initialize():
    if data_wrangler.conn is None:
        data_wrangler.initialize_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    response = ""

    try:
        if user_input.lower().startswith("list columns in"):
            table_name = user_input.split()[-1]
            response = data_wrangler.list_columns(table_name)
        elif user_input.lower().startswith("list tables"):
            response = data_wrangler.get_table_names()
        else:
            user_input_augmented = user_input  # Placeholder for actual query augmentation
            prompt = standard_prompt + user_input_augmented
            generated_sql = model.generate_content(prompt).text
            print("Generated SQL:", generated_sql)
            clean_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
            if not clean_sql.lower().startswith('select'):
                raise ValueError("Generated SQL is not a SELECT statement.")
            response = data_wrangler.execute_sql_query(clean_sql)

        response = response_augmentation(response)

    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return jsonify(response)

def response_augmentation(response):
    return response

if __name__ == '__main__':
    app.run(debug=True)
