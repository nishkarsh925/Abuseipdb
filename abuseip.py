import streamlit as st
import requests

# Set the title of the app
st.title("AbuseIPDB IP Address Checker")

# Enter your AbuseIPDB API key here
API_KEY = '43a12597815bc0ffff77dbf9a093ab68a465b733941071fc98c0e8daa098ed595e5d6ac0cc626286'

# Function to get abuse information from AbuseIPDB
def get_abuse_info(ip_address):
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }
    params = {
        'ipAddress': ip_address
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code} {response.text}")
        return None

# Input field for the IP address
ip_address = st.text_input("Enter the IP Address:", "")

if st.button("Check IP"):
    if ip_address:
        abuse_info = get_abuse_info(ip_address)

        if abuse_info and 'data' in abuse_info:
            # Display abuse information
            st.subheader("Abuse Information")
            st.write(f"IP Address: {abuse_info['data']['ipAddress']}")
            st.write(f"Abuse Confidence Score: {abuse_info['data']['abuseConfidenceScore']}")
            st.write(f"Total Reports: {abuse_info['data']['totalReports']}")
            
            # Check if reports exist
            if 'reports' in abuse_info['data'] and abuse_info['data']['reports']:
                st.write("Abuse Reports:")
                for report in abuse_info['data']['reports']:
                    st.write(f"- {report['comment']} (Reported on: {report['dateReported']})")
            else:
                st.write("No abuse reports found for this IP address.")
        else:
            st.warning("No abuse information found.")
    else:
        st.warning("Please enter a valid IP address.")
