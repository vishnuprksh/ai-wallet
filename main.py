import streamlit as st
from openai import OpenAI
import os
import pandas as pd
from io import StringIO

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_response(prompt):
    content = "You are an expense tracker. \
            Take text form of bank statements and convert those into sql format. \
            The headers for the csv after convertion should be Date, Description, Debit, Credit, Balance After and Category. \
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

    # Add button to append to balance_sheet.csv
    if st.button('Add to Record'):
        # Check if balance_sheet.csv exists
        if os.path.exists('balance_sheet.csv'):
            existing_df = pd.read_csv('balance_sheet.csv')
            updated_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            updated_df = df

        # Save the updated DataFrame back to balance_sheet.csv
        updated_df.to_csv('balance_sheet.csv', index=False)
        st.success('Record added to balance_sheet.csv')

