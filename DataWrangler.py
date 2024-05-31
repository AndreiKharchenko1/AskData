import pandas as pd

class DataWrangler:
    def __init__(self):
        self.data_frames = {
            'clinic_location': pd.read_csv('data/clinic_location_table_DP.csv'),
            'clinic_profitability': pd.read_csv('data/clinic_profitability_table_DP.csv'),
            'employee': pd.read_csv('data/employee_table_DP.csv'),
            'patient_appointment': pd.read_csv('data/patient_appointment_table_DP.csv'),
            'patient': pd.read_csv('data/patient_appointment_table_DP.csv'),
            'physician': pd.read_csv('data/physician_table_DP.csv'),
            'treatments_costs': pd.read_csv('data/treatments_costs table_DP.csv')
        }


    def get_column_info(self, df_name):
        df = self.data_frames.get(df_name)
        if df is not None:
            columns = df.columns.tolist()
            example_data = df.iloc[0].to_dict()
            return columns, example_data
        return None, None

    def generate_response(self, keyword):
        if any(k in keyword for k in ['finance', 'profitability', 'revenue', 'expenses']):
            columns, example = self.get_column_info('clinic_profitability')
            return f"The finance table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['employee', 'staff', 'personnel', 'role']):
            columns, example = self.get_column_info('employee')
            return f"The employee table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['patient appointment', 'appointment', 'visit', 'consultation']):
            columns, example = self.get_column_info('patient_appointment')
            return f"The patient appointment table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['patient', 'patient information', 'demographics', 'medical history']):
            columns, example = self.get_column_info('patient')
            return f"The patient table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['physician', 'doctor', 'healthcare provider', 'qualifications']):
            columns, example = self.get_column_info('physician')
            return f"The physician table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['treatment', 'cost', 'medical procedure', 'healthcare cost']):
            columns, example = self.get_column_info('treatments_costs')
            return f"The treatments costs table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        elif any(k in keyword for k in ['location', 'clinic location', 'address']):
            columns, example = self.get_column_info('clinic_location')
            return f"The clinic location table contains the following columns: {', '.join(columns)}. An example data point: {example}"
        else:
            return "No relevant data found."

# Usage Example
# dw = DataWrangler()
# print(dw.generate_response('finance'))

