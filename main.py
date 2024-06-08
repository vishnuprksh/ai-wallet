import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

import pandas as pd
from io import StringIO

# Load environment variables from .env file
load_dotenv()

client = OpenAI()
def generate_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expense tracker. \
             You take copy text of transactions from pdf bank statements and convert those into csv format. \
             The headers for the csv are Date, Description, Debit, Credit, Balance After and Category. \
             Assign appropriate category for each expenses"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion

# print(completion.choices[0].message.content)

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

    # Provide download option for the CSV
    csv_download = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_download,
        file_name="preview.csv",
        mime="text/csv"
    )
