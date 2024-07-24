import sqlite3
import re

response = """Certainly! An SQL statement for the `clinic_profitability` table might look like this:```sql SELECT * FROM clinic_inventory;``` This statement will select all rows from the `clinic_profitability` table. Here is an example of a more specific SQL statement that will select the `clinic_name`, `total_revenue`, and `total_expenses` columns for all rows in the `clinic_profitability` table where the `profit` is greater than $100,000: ```SELECT clinic_name, total_revenue, total_expenses FROM clinic_profitability WHERE profit > 100000;```"""

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
        print(column_names)
        for row in result:
            print(row)
        formatted_sql_result = format_query_results(column_names, result)
        return formatted_sql_result
    else:
        print("No results or error in query execution")
        return "No results or error in query execution"

'''
def format_query_results(column_names, rows):
    formatted_string = "\t".join(column_names) + "\n"
    for row in rows:
        formatted_string += "\t".join(map(str, row)) + "\n"
    print("formatted_string", formatted_string)
    return formatted_string
'''
def format_query_results(column_names, rows):
    formatted_string = "<table border='1'><tr><th>" + "</th><th>".join(column_names) + "</th></tr>"
    for row in rows:
        formatted_string += "<tr><td>" + "</td><td>".join(map(str, row)) + "</td></tr>"
    formatted_string += "</table>"
    return formatted_string


# Test
extracted_sql = extractSQL(response)
for sql in extracted_sql:
    print("sql:", sql)
    #print("testquery result: ")
    testQuery(sql)



