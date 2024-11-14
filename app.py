# load all the environment variables
from dotenv import load_dotenv
load_dotenv() 

# Import necessary library
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


# Function to load model
# It will be responsible for giving the query as response
def get_gemini_response(question,prompt):
    model = genai.GenerativeModel(model_name='gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


# Function to retrive query(records) from the data base

def read_sql_query(sql,db):
    conn=sqlite3.connect(db) # create connection with db
    cur=conn.cursor() # Cursor:- this will help in executing our query
    cur.execute(sql) # Run the sql query
    rows=cur.fetchall() # Fetch all the records
    conn.commit() # Commit
    conn.close()  # Close the connection after fetching the data
    # print the rows
    for row in rows:
        print(row)
    return rows
    


# Define Prompt
# Multiple prompt in form of list
prompt=[
    # Prompt 1
    """
    "You are an expert in translating English requirements into accurate and efficient SQL queries. 
    For each request, generate a precise SQL query that meets the user’s needs without errors. 
    The SQL database includes a STUDENT table with columns: Name, Class, and Section. 
    Ensure the SQL code doesn’t contain ''' quotes at the beginning or end, nor the word 'SQL' in the output.
    For example, if the user asks, 'How many records are present?', the query should look like: SELECT COUNT(*) FROM STUDENT;
    """
    # Prompt 2
    # """
    #     you are an expert in converting english to SQL query!
    #     Execute the sql query according to the need that the user want  without any error
    #     The Sql Database has the same STUDENT and has the following columns -Name,Class
    #     Section \n\n For example:- How many entities of records are present?,
    #     the SQL Command will be something like SELECT COUNT(*) FROM STUDENT;
    #     also the sql code should not have ''' in the beginning or end and sql word in output
    # """

]

# Set up the Streamlit app
st.set_page_config(page_title="Retrieve SQL data with Gemini")
st.header("Gemini to Retrieve SQL Data")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the Question")


# If submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)



