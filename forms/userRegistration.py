import logging
import streamlit as st
import requests
import json

from constants import CLOUD_RUN_URL, LOCAL_URL


def userRegistrationWithAgent(name, email, contact, department, client_name):

    url = f"{LOCAL_URL}/api/external-communications/user-registration/"

    payload = json.dumps({
    "name": name,
    "email": email,
    "contact": contact,
    "department": department,
    "client_name": client_name
    })
    headers = {
    'Content-Type': 'application/json',
    'c': ''
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def userRegistration():
    st.header("User Registration")

    # Example form inputs
    name = st.text_input("Employee Name")
    email = st.text_input("Employee email")
    contact = st.text_input("Employee Contact")
    department = st.text_input("Department")
    client_name = st.text_input("Company")

    
    
    
    if st.button("Submit"):
        response = userRegistrationWithAgent(name, email, contact, department, client_name)
        if response.status_code == 200:
            logging.info(f"response from the createJob API hit for the email: {email}")
            st.write(f"Thanks for submitting we are creating user with , Name: {name}, Email: {email}")
        elif response.status_code == 400:
            logging.info(f"some error happened but problem was at the user side for email: {email}")
            response_dict = response.json()
            st.write(f"we faced some problem in processing your request read this message if you can do something: {response_dict["message"]}")
        else:
            logging.info(f"some internal error occured for the email: {email}")
