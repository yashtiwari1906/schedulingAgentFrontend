import logging
import streamlit as st
import requests
import json

from constants import CLOUD_RUN_URL, AGENT_SERVER_URL

def prepare_email_content(hr_email_content):
    if "scheduling_link" not in hr_email_content:
        hr_email_content += "\n here's the link which you can use for scheduling the interview: {}" 
    else:
        hr_email_content = hr_email_content.replace("scheduling_link", "{}")

    email_content = """Hi {},
    """+ hr_email_content+"""
    """ 

    return email_content

def userRegistrationWithAgent(
    client_name,
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
    role,
    department,
    experience_level,
    employee_emails,
):

    url = f"{AGENT_SERVER_URL}/api/external-communications/interview-pool-creation/"
    print(f"fuck yeah")
    payload = json.dumps(
        {
            "client_name": client_name,
            "client_email_extension": client_email_extension,
            "pool_creator": {
                "name": pool_creator_name,
                "email": pool_creator_email,
                "contact": pool_creator_contact,
                "department": pool_creator_department,
            },
            "job_meta_data": {
                "email_summary": email_summary,
                "job_description": job_description,
                "email_heading": email_heading,
                "email_content": email_content,
                "meeting_heading": meeting_heading,
                "meeting_content": meeting_content,
            },
            "role": role,
            "experience_level": experience_level,
            "department": department,
            "employee_emails": employee_emails,
        }
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def interviewPoolCreationPage():
    st.header("Create New Job")

    # Example form inputs

    client_name = st.text_input("client name for eg. meta, google, etc")
    client_email_extension = st.text_input(
        "company's email extension for eg. meta.com, google.com, etc"
    )
    st.write("Information related to you who is creating this job")
    pool_creator_name = st.text_input("creator name")
    pool_creator_email = st.text_input("creator email")
    pool_creator_contact = st.text_input("creator contact")
    pool_creator_department = st.text_input("creator department")
    # st.write("Some meta data information")
    email_summary = "no use"  # st.text_input("email summary")
    job_description = "no use"  # st.text_input("job description")
    email_heading = st.text_input("email heading")
    st.write("Make sure to have a placeholder scheduling_link somewhere where you want to embed the dynamic scheduling link for the user")
    hr_email_content = st.text_area("first of congratulations!!! ... ", height = 400)
    email_content = prepare_email_content(hr_email_content)
    meeting_heading = st.text_area("meeting heading", height = 100)
    meeting_content = st.text_area("meeting content", height=300)
    st.write("information related to the job")
    role = st.text_input("role for which this interview pool is getting created")
    department = st.text_input(
        "department for which this interview pool is getting created"
    )
    experience_level = st.text_input(
        "experience level for eg. junior, senior , lead, etc"
    )
    employee_emails = st.text_input(
        "comma separated emails for eg. mark@meta.com, yann@meta.com"
    )

    if st.button("Submit"):
        response = userRegistrationWithAgent(
            client_name,
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
            role,
            department,
            experience_level,
            employee_emails,
        )
        if response.status_code == 200:
            logging.info(
                f"response from the createJob API hit for the pool_creator_email: {pool_creator_email}"
            )
            st.write(
                f"Thanks for submitting we are creating interviw pool for , role: {role}, pool creator email: {pool_creator_email}"
            )
        elif response.status_code == 400:
            logging.info(
                f"some error happened but problem was at the user side for pool_creator_email: {pool_creator_email}"
            )
            response_dict = response.json()
            print(response_dict)
            st.write(
                f"we faced some problem in processing your request read this message if you can do something: {response_dict}"
            )
        else:
            logging.info(
                f"some internal error occured for the pool_creator_email: {pool_creator_email}"
            )
            st.write(
                f"we faced some problem in processing your request if possible please mail us at yashtiwari.engineer@gmail.com"
            )
