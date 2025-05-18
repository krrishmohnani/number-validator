import streamlit as st
import requests
import pandas as pd

# --------------------------
# 🌐 Country code mapping
# --------------------------
country_map = {
    "+91": "India 🇮🇳",
    "+44": "United Kingdom 🇬🇧",
    "+1": "United States 🇺🇸 / Canada 🇨🇦",
    "+61": "Australia 🇦🇺",
    "+81": "Japan 🇯🇵",
    "+49": "Germany 🇩🇪",
    "+33": "France 🇫🇷",
    "+971": "United Arab Emirates 🇦🇪",
    # Add more as needed
}

# --------------------------
# 🔍 Detect country from number
# --------------------------
def detect_country(number):
    for code, country in country_map.items():
        if number.startswith(code):
            return country
    return "Unknown 🌍"

# --------------------------
# 🚀 Streamlit UI Setup
# --------------------------
st.set_page_config(page_title="Valid Phone Number Checker", page_icon="📱", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#00a884;'>📱 Valid Phone Number Checker</h1>
    <p style='text-align:center;'>Check if a number is <b>valid on WhatsApp</b> and from which <b>country</b>.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# 📥 Input
phone_number = st.text_input("Enter phone number (e.g., +919876543210)", max_chars=15)

# --------------------------
# 🌐 WhatsApp API Call
# --------------------------
def validate_whatsapp_number(number: str):
    api_url = "https://whatsapp-number-validator3.p.rapidapi.com/WhatsappNumberHasItBulkWithToken"

    headers = {
        "x-rapidapi-key": "c0a6f42258mshcceedc1d343e8c8p161593jsnb5ed74fe152f",  # 🔐 Replace with your real key
        "x-rapidapi-host": "whatsapp-number-validator3.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    payload = {"phone_numbers": [number.replace("+", "")]}  # remove '+' for API

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise if HTTP error
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API request failed: {e}")
        return None

# --------------------------
# ✅ Trigger on Button Click
# --------------------------
if st.button("✅ Validate Number"):
    if phone_number:
        country = detect_country(phone_number)
        st.info(f"🌍 Detected Country: **{country}**")

        result = validate_whatsapp_number(phone_number)

        if result and "data" in result and isinstance(result["data"], list) and result["data"]:
            data = result["data"][0]
            status = data.get("status", "unknown").upper()

            st.success(f"📲 The number **{phone_number}** is **{status}** on WhatsApp.")

            st.markdown("### 🔍 Detailed API Response")
            df = pd.DataFrame([data])
            st.dataframe(df)
        else:
            st.error("⚠️ Invalid or unexpected API response. Please check the number or try again.")
    else:
        st.warning("⚠️ Please enter a phone number.")

st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io/) and [RapidAPI](https://rapidapi.com/).")
