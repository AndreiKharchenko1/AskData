import sqlite3
import re


def extractSQL(response):
    # Use regular expression to find text within triple backticks
    sql_statements = re.findall(r'```sql(.*?)```', response, re.DOTALL)
    return sql_statements


# Function to connect to the database
def connect_to_database(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print("Successfully connected to the database")
        return connection
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None


# Function to execute a query and return the result along with column names
def execute_query(query, params=None):
    connection = connect_to_database('askdatanew.db')  # Replace 'askdata.db' with your actual .db file name
    if connection is None:
        return None, None
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return result, column_names
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None, None
    finally:
        if connection:
            connection.close()


def testQuery(query):
    result, column_names = execute_query(query)

    if result and column_names:
        formatted_sql_result = format_query_results(column_names, result)
        return formatted_sql_result
    else:
        print("For Ketchup Clinic, this SQL did not return a valid result, please test it before using it.")
        return "For Ketchup Clinic, this SQL did not return a valid result, please test it before using it."


def format_query_results(column_names, rows):
    formatted_string = "<table border='1'><tr><th>" + "</th><th>".join(column_names) + "</th></tr>"
    for row in rows:
        formatted_string += "<tr><td>" + "</td><td>".join(map(str, row)) + "</td></tr>"
    formatted_string += "</table>"
    return formatted_string
