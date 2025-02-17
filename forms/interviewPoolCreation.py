import logging
import streamlit as st
import requests
import json

from constants import CLOUD_RUN_URL, LOCAL_URL


def userRegistrationWithAgent(client_name, 
                              client_email_extension, 
                              pool_creator_name, 
                              pool_creator_email, 
                              pool_creator_contact, 
                              pool_creator_department,
                              email_summary, 
                              job_description,
                              email_heading, 
                              email_content, 
                              meeting_heading, 
                              meeting_content,
                              role, department, experience_level, employee_emails):

    url = "{LOCAL_URL}/api/external-communications/interview-pool-creation/"

    payload = json.dumps({
    "client_name": client_name,
    "client_email_extension": client_email_extension,
    "pool_creator": {
        "name": pool_creator_name,
        "email": pool_creator_email,
        "contact": pool_creator_contact,
        "department": pool_creator_department
    },
    "job_meta_data": {
        "email_summary": email_summary,
        "job_description": job_description,
        "email_heading": email_heading,
        "email_content": email_content,
        "meeting_heading": meeting_heading,
        "meeting_content": meeting_content
    },
    "role": role,
    "experience_level": experience_level,
    "department": department,
    "employee_emails": employee_emails
    })
    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def interviewPoolCreation():
    st.header("Interview Pool Creation")

    # Example form inputs

    client_name = st.text_input("client name for eg. meta, google, etc")
    client_email_extension = st.text_input("company's email extension for eg. meta.com, google.com, etc")
    st.write("Information related to you who is creating this job")
    pool_creator_name = st.text_input("creator name")
    pool_creator_email = st.text_input("creator email")
    pool_creator_contact = st.text_input("creator contact")
    pool_creator_department = st.text_input("creator department")
    st.write("Some meta data information")
    email_summary = st.text_input("email summary")
    job_description = st.text_input("job description")
    email_heading = st.text_input("email heading")
    email_content = st.text_input("email content")
    meeting_heading = st.text_input("meeting heading")
    meeting_content = st.text_input("meeting content")
    st.write("information related to the job")
    role = st.text_input("role for which this interview pool is getting created")
    department = st.text_input("department for which this interview pool is getting created")
    experience_level = st.text_input("experience level for eg. junior, senior , lead, etc")
    employee_emails = st.text_input("comma separated emails for eg. mark@meta.com, yann@meta.com")

    
    
    
    if st.button("Submit"):
        response = userRegistrationWithAgent(client_name, 
                              client_email_extension, 
                              pool_creator_name, 
                              pool_creator_email, 
                              pool_creator_contact, 
                              pool_creator_department,
                              email_summary, 
                              job_description,
                              email_heading, 
                              email_content, 
                              meeting_heading, 
                              meeting_content,
                              role, department, experience_level, employee_emails)
        if response.status_code == 200:
            logging.info(f"response from the createJob API hit for the pool_creator_email: {pool_creator_email}")
            st.write(f"Thanks for submitting we are creating interviw pool for , role: {role}, pool creator email: {pool_creator_email}")
        elif response.status_code == 400:
            logging.info(f"some error happened but problem was at the user side for pool_creator_email: {pool_creator_email}")
            response_dict = response.json()
            st.write(f"we faced some problem in processing your request read this message if you can do something: {response_dict["message"]}")
        else:
            logging.info(f"some internal error occured for the pool_creator_email: {pool_creator_email}")
