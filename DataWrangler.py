import pandas as pd
import sqlite3

class DataWrangler:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.conn = None

    def initialize_db(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        cursor = self.conn.cursor()

        for name, path in self.file_paths.items():
            try:
                df = pd.read_csv(path)
                df.columns = [col.strip() for col in df.columns]
                df.to_sql(name, self.conn, index=False, if_exists='replace')
                print(f"Loaded {name} with columns: {df.columns.tolist()}")
            except Exception as e:
                print(f"Error loading {name} from {path}: {e}")

    def list_columns(self, table_name):
        try:
            query = f"PRAGMA table_info({table_name})"
            result = pd.read_sql_query(query, self.conn)
            columns = result['name'].tolist()
            return columns
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def execute_sql_query(self, query):
        try:
            result = pd.read_sql_query(query, self.conn)
            return result.to_dict(orient='records')
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_table_names(self):
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            result = pd.read_sql_query(query, self.conn)
            tables = result['name'].tolist()
            return tables
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    file_paths = {
        'clinic_location_table': '/Users/danielazafrani/AskData/data/clinic_location_table_DP.csv',
        'clinic_profitability_table': '/Users/danielazafrani/AskData/data/clinic_profitability_table_DP.csv',
        'employee_table': '/Users/danielazafrani/AskData/data/employee_table_DP.csv',
        'patient_appointment_table': '/Users/danielazafrani/AskData/data/patient_appointment_table_DP.csv',
        'patient_table': '/Users/danielazafrani/AskData/data/patient_table_DP.csv',
        'physician_table': '/Users/danielazafrani/AskData/data/physician_table_DP.csv',
        'treatments_costs_table': '/Users/danielazafrani/AskData/data/treatments_costs table_DP.csv'
    }
    dw = DataWrangler(file_paths)
    dw.initialize_db()
    print(dw.list_columns("clinic_location_table"))
    print(dw.get_table_names())
