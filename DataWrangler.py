import pandas as pd
import re
import google.generativeai as genai
import os

class DataWrangler:
    def __init__(self, gemini_api_key):
        self.data_frames = {
            'clinic_location': pd.read_csv('newData/clinic_location_table_DP (1).csv'),
            'clinic_profitability': pd.read_csv('newData/clinic_profitability_table_DP (1).csv'),
            'medical_dispensation': pd.read_csv('newData/medical_dispensation_table_DP (1).csv'),
            'medical_history': pd.read_csv('newData/medical_history_table_DP (2).csv'),
            'patient_appointment': pd.read_csv('newData/patient_appointment_table_DP (1).csv'),
            'patient': pd.read_csv('newData/patient_table_DP (1).csv'),
            'patient_treatment': pd.read_csv('newData/patient_treatment_table_DP (1).csv'),
            'physician': pd.read_csv('newData/physician_table_DP (1).csv'),
            'treatments_costs': pd.read_csv('/Users/danielazafrani/Documents/GitHub/hw1-DanielAzafrani/AskData/newData/treatments_costs table_DP.csv'),
            'billing_and_insurance': pd.read_csv('newData/billing_and_insurance_table_DP (1).csv'),
            'clinic_expense': pd.read_csv('newData/clinic_expense_table_DP (1).csv'),
            'clinic_inventory': pd.read_csv('newData/clinic_inventory_table_DP (1).csv')
        }

        self.metadata = {df_name: {
            'columns': df.columns.tolist(),
            'example_data': df.iloc[0].to_dict() if not df.empty else {},
            'description': self.generate_description(df_name)
        } for df_name, df in self.data_frames.items()}

        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_description(self, df_name):
        descriptions = {
            'clinic_inventory': "This data frame contains information about the clinic's inventory, including supplies, stock, materials, and equipment.",
            'clinic_location': "This data frame contains detailed information about the physical locations of the clinics within the system, including addresses, geographic coordinates, and contact details.",
            'clinic_profitability': "This data frame contains financial information about the clinic's profitability, including revenue, expenses, and financial metrics.",
            'medical_dispensation': "This data frame contains information about medical dispensations, including medication, dosage, prescription details, and patient information.",
            'medical_history': "This data frame contains the medical history of patients, including diagnoses, treatments received, health outcomes, and medical records.",
            'patient_appointment': "This data frame contains information about patient appointments, including visit details, consultation schedules, and appointment times.",
            'patient': """
IMPORTANT: THIS DATAFRAME HAS NOTHING TO DO WITH TREATMENTS. IGNORE THIS DF IF SEE TREATMENT IN USER QUERY.
This data frame contains demographic and personal information about patients, including contact information and identity details.
""",
            'patient_treatment': "This data frame contains information about patient treatments, including medical procedures, healthcare costs, therapy sessions, and treatment plans.",
            'physician': "This data frame contains information about physicians, including their qualifications, specializations, contact details, and roles within the clinic.",
            'treatments_costs': "This data frame contains information about the costs of treatments, including prices, fees, and billing details."
        }
        return descriptions.get(df_name, "No description available.")

    def choose_dataframe(self, query):
        # Prioritize the patient_treatment table for queries involving "treatment"
        if 'treatment' in query.lower():
            return 'patient_treatment'
        
        prompt = """
You are an AI model tasked with selecting the appropriate data frame based on the following query:
"{query}"

Here are the available data frames and their details:

{dataframes}

Please choose the most relevant data frame.
""".format(
            query=query,
            dataframes=''.join(
                [
                    f"{df_name}: {meta['description']} Columns: {', '.join(meta['columns'])}. Example data: {meta['example_data']}\n"
                    for df_name, meta in self.metadata.items()
                ]
            ),
        )

        response = self.model.generate_content(prompt)
        return self.extract_dataframe_name(response.text)

    def extract_dataframe_name(self, response_text):
        # Extract the data frame name from the response text
        for df_name in self.data_frames.keys():
            if df_name in response_text:
                return df_name
        return None

    def read_and_match_dataframe(self, query):
        # Scan contents of each data frame and make an informed decision
        for df_name, df in self.data_frames.items():
            for column in df.columns:
                if column in query:
                    return df_name
            for row in df.values:
                if any(query.lower() in str(item).lower() for item in row):
                    return df_name
        return None

    def generate_sql_query(self, table_name, conditions=None):
        if conditions:
            return f"SELECT * FROM {table_name} WHERE {conditions};"
        else:
            return f"SELECT * FROM {table_name};"

    def generate_response(self, query):
        # First, try to use the Gemini model to choose the data frame
        table_name = self.choose_dataframe(query)
        
        # If Gemini model doesn't provide a clear answer, fall back to content-based method
        if not table_name:
            table_name = self.read_and_match_dataframe(query)
        
        if not table_name:
            return "No relevant data found."
        
        columns, example = self.metadata[table_name]['columns'], self.metadata[table_name]['example_data']
        if 'sql' in query:
            # Extract conditions for the SQL query if any
            match = re.search(r'where (.+)', query, re.IGNORECASE)
            conditions = match.group(1) if match else None
            sql_query = self.generate_sql_query(table_name, conditions)
            return f"Generated SQL Query:\n{sql_query}"
        else:
            return f"The {table_name} table contains the following columns: {', '.join(columns)}. An example data point: {example}"

# Usage Example
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    dw = DataWrangler(GEMINI_API_KEY)
    print(dw.generate_response('Write an SQL query to count the number of clinics in each state'))
    print(dw.generate_response('What information is available in the clinic location table?'))
    print(dw.generate_response('Write an SQL query to find patients where age > 30'))
    print(dw.generate_response('Write an SQL query to find patients who received a specific treatment'))
