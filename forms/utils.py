from constants import LOCAL_URL
import requests
import streamlit as st


def showJobsOnScreen(client_name):
    GET_API_URL = f"{LOCAL_URL}/api/external-communications/get-active-jobs/?client_name={client_name}"
    response = requests.get(GET_API_URL)
    if response.status_code == 200:
        response_dict = (
            response.json()
        )  # Assuming data is a dictionary with three elements
        active_job_list = response_dict["data"]
    else:
        st.error("Failed to fetch data from API")
        st.stop()

    # Display options to the user
    st.write("Select one of the following options:")
    showcase_template = "{} created by {}"
    selected_option = st.radio(
        label="Choose one",
        options=[
            (active_job["role"], active_job["hr_name"], active_job["jobId"])
            for active_job in active_job_list
        ],  # Assuming each value has an '_id'
        format_func=lambda x: showcase_template.format(
            x[0], x[1]
        ),  # Show only key names in UI
    )
    print(selected_option)
    jobId = selected_option if selected_option is None else selected_option[-1]
    return jobId
