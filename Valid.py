import streamlit as st
import requests
import json

# Streamlit UI
st.title("📱 WhatsApp Number Validator")
st.write("Enter international phone numbers (with country code) separated by commas.")

# Input field
phone_input = st.text_area("Phone Numbers", placeholder="Example: 447748188019, 447999999999")

# Submit button
if st.button("Check Numbers"):
    if phone_input.strip():
        # Clean and format input numbers
        phone_numbers = [num.strip() for num in phone_input.split(",") if num.strip().isdigit()]
        
        if not phone_numbers:
            st.warning("Please enter valid phone numbers.")
        else:
            # API request
            url = "https://whatsapp-number-validator3.p.rapidapi.com/WhatsappNumberHasItBulkWithToken"
            payload = {"phone_numbers": phone_numbers}
            headers = {
                "x-rapidapi-key": "c0a6f42258mshcceedc1d343e8c8p161593jsnb5ed74fe152f",  # Consider storing this securely
                "x-rapidapi-host": "whatsapp-number-validator3.p.rapidapi.com",
                "Content-Type": "application/json"
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                result = response.json()

                # Display results
                st.subheader("Validation Results")
                for item in result:
                    status = "✅ Valid" if item["status"] == "valid" else "❌ Invalid"
                    st.write(f"**{item['phone_number']}** → {status}")
            except Exception as e:
                st.error(f"API request failed: {e}")
    else:
        st.warning("Enter at least one phone number.")

# Optional footer
st.markdown("---")
st.caption("Powered by RapidAPI • Built with ❤️ using Streamlit")
