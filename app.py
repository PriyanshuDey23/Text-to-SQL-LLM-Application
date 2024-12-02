# Load all the environment variables
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
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        response = model.generate_content([prompt[0], question])
        # Extracting the first candidate's text content
        sql_query = response.candidates[0].content.parts[0].text.strip()
        return sql_query
    except Exception as e:
        st.error(f"Error fetching response from Gemini: {e}")
        return None


# Function to retrieve query(records) from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)  # Create connection with the database
        cur = conn.cursor()         # Cursor to execute SQL queries
        cur.execute(sql)            # Run the SQL query
        rows = cur.fetchall()       # Fetch all records
        conn.close()                # Close the connection
        return rows
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []


# Define Prompt
prompt = [
    """
    "You are an expert in translating English requirements into accurate and efficient SQL queries. 
    For each request, generate a precise SQL query that meets the user’s needs without errors. 
    The SQL database includes a STUDENT table with columns: Name, Class, and Section. 
    Ensure the SQL code doesn’t contain ''' quotes at the beginning or end, nor the word 'SQL' in the output.
    For example, if the user asks, 'How many records are present?', the query should look like: SELECT COUNT(*) FROM STUDENT;
    """
]

# Set up the Streamlit app
st.set_page_config(page_title="Retrieve SQL Data with Gemini")
st.header("Gemini to Retrieve SQL Data")

# User input and button
question = st.text_input("Input your question:", key="input")
submit = st.button("Ask the Question")

# If submit is clicked
if submit:
    try:
        # Step 1: Get SQL Query
        response = get_gemini_response(question, prompt)
        if response:
            st.write("Generated SQL Query:", response)

            # Step 2: Retrieve data from database
            data = read_sql_query(response, "student.db")

            # Step 3: Display results
            st.subheader("Database Response:")
            if data:
                for row in data:
                    st.write(row)
            else:
                st.write("No data returned from the query.")
        else:
            st.write("No response generated by Gemini.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
