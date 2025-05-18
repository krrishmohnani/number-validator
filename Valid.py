import streamlit as st
import requests
import time

# Function to validate WhatsApp numbers
def validate_whatsapp_numbers(numbers, api_token):
    url = "https://whatsapp-number-validator3.p.rapidapi.com/WhatsappNumberHasItBulkWithToken"
    headers = {
        "x-rapidapi-host": "whatsapp-number-validator3.p.rapidapi.com",
        "x-rapidapi-key": api_token,
        "content-type": "application/json"
    }
    
    payload = {"numbers": numbers}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:
            st.warning("Too many requests. Please try again later.")
            time.sleep(10)  # Wait for 10 seconds before retrying
            return validate_whatsapp_numbers(numbers, api_token)  # Retry
        else:
            st.error(f"An error occurred: {err}")
            return None

# Streamlit app layout
st.title("WhatsApp Number Validator")
api_token = st.text_input("Enter your API Token", type="password")

if st.button("Validate Numbers"):
    numbers = st.text_area("Enter numbers (comma separated)")
    if numbers and api_token:
        numbers_list = [number.strip() for number in numbers.split(",")]
        results = validate_whatsapp_numbers(numbers_list, api_token)
        if results:
            st.json(results)
    else:
        st.warning("Please provide a list of numbers and your API token.")
