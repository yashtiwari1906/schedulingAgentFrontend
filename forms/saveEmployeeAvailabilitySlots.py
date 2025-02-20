import logging
from forms.utils import showJobsOnScreen
import streamlit as st
import requests
import json

from constants import CLOUD_RUN_URL, LOCAL_URL


def showSlotSelectOptions():
    GET_API_URL = f"{LOCAL_URL}/api/external-communications/get-availability-slots/"
    response = requests.get(GET_API_URL)
    if response.status_code == 200:
        response_dict = (
            response.json()
        )  # Assuming data is a dictionary with three elements
        data = response_dict["data"]
    else:
        st.error("Failed to fetch data from API")
        st.stop()

    st.write("Click on each day to see available time slots and select one or more:")
    # selected_week = "month2_week4"
    month_week1, month_week2 = data.keys()

    selected_slots = {month_week1: {}, month_week2: {}}  # To hold the user's selections

    # first week
    for day, slots in data[month_week1].items():
        # Use an expander for each day so that when clicked, it shows available slots
        with st.expander(day.capitalize()):
            # The key parameter ensures the widget state is preserved per day
            selected = st.multiselect(
                f"Select time slots for {day.capitalize()}", options=slots, key=day
            )
            if selected:
                selected_slots[month_week1][day] = selected

    # second week
    for day, slots in data[month_week2].items():
        # Use an expander for each day so that when clicked, it shows available slots
        with st.expander(day.capitalize()):
            # The key parameter ensures the widget state is preserved per day
            selected = st.multiselect(
                f"Select time slots for {day.capitalize()}", options=slots, key=day
            )
            if selected:
                selected_slots[month_week2][day] = selected

    return selected_slots


def saveEmployeeAvailabilitySlotsWithAgent(jobId, employee_email, selected_slots):

    url = f"{LOCAL_URL}/api/external-communications/save-employee-availability-slots/?jobId={jobId}"

    payload = json.dumps(
        {"email": employee_email, "reschedule": False, "slots": selected_slots}
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def saveEmployeeAvailabilitySlotsPage():
    query_params = st.query_params
    client_name, jobId = query_params.get("client_name", None), query_params.get(
        "jobId", None
    )
    st.header("slot preference form")

    # Example form inputs
    employee_email = st.text_input("Employee email")
    if client_name is None or jobId is None:
        client_name = st.text_input("enter client name for eg. meta, google, etc")
        jobId = showJobsOnScreen(client_name=client_name)
    print(jobId)
    selected_slots = showSlotSelectOptions()

    if st.button("Submit"):
        response = saveEmployeeAvailabilitySlotsWithAgent(
            jobId, employee_email, selected_slots
        )
        if response.status_code == 200:
            logging.info(
                f"response from the createJob API hit for jobId: {jobId} the employee_email: {employee_email}"
            )
            st.write(f"Thanks for submitting")
        elif response.status_code == 400:
            logging.info(
                f"some error happened but problem was at the user side for jobId: {jobId} the employee_email: {employee_email}"
            )
            response_dict = response.json()
            st.write(
                f"we faced some problem in processing your request read this message if you can do something: {response_dict["message"]}"
            )
        else:
            logging.info(
                f"some internal error occured for the jobId: {jobId} the employee_email: {employee_email}"
            )
            st.write(
                f"we faced some problem in processing your request if possible please mail us at yashtiwari.engineer@gmail.com"
            )
