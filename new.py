import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
import sqlite3

# Load environment variables from .secrets file
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_response(prompt):
    content = "You are an expense tracker. \
            Take text form of bank statements and convert those into sql format. \
            The headers for the csv after conversion should be Date, Description, Debit, Credit, Balance After and Category. \
            Assign appropriate category for each expense. \
            Format for date is yyyy-mm-dd. \
            Should simplify the description for readability."

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": prompt}
        ]
    )
    return completion

def create_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS balance_sheet (
            Date TEXT,
            Description TEXT,
            Debit REAL,
            Credit REAL,
            Balance_After REAL,
            Category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(df):
    conn = sqlite3.connect('expenses.db')
    df.to_sql('balance_sheet', conn, if_exists='append', index=False)
    conn.close()

# Set the title of the web app
st.title('AI Wallet')

# Create a text input widget for the prompt
prompt = st.text_area('Enter your prompt:')

# Create a button widget to submit the prompt
if st.button('Submit'):
    # Generate response using GPT-3
    response = generate_response(prompt)
    
    # Display the response
    csv_content = response.choices[0].message.content
    data = StringIO(csv_content)
    df = pd.read_csv(data, encoding="utf-8")
    st.table(df.head())

    # Add button to insert data into the SQL database
    if st.button('Add to Record'):
        # Create the database and table if it doesn't exist
        create_database()
        
        # Insert the new data
        insert_data(df)
        st.success('Record added to the SQL database')
