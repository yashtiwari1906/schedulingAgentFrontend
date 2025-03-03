import logging
import streamlit as st
import requests
import json

from constants import CLOUD_RUN_URL, LOCAL_URL


def select_slot(month_week, day, slot):
    """Sets the global selected slot in session state."""
    st.session_state.selected_slot = {
        "month_week": month_week,
        "day": day,
        "time_slot": slot,
    }


def saveCandidateSlotPreferenceWithAgent(
    jobId,
    candidate_email,
    candidate_name,
    candidate_contact,
    empId,
    month_week,
    day,
    time_slot,
):

    url = f"{LOCAL_URL}/api/external-communications/save-candidate-slot-preference/?jobId={jobId}"

    payload = json.dumps(
        {
            "candidate_email": candidate_email,
            "candidate_name": candidate_name,
            "candidate_contact": candidate_contact,
            "empId": empId,
            "reschedule": False,
            # "interviewId": "67991f7b7907a162cd1a0dcd",
            "selected_slot": {
                "month_week": month_week,
                "day": day,
                "time_slot": time_slot,
            },
        }
    )
    # print("="*20)
    # print({
    # "candidate_email": candidate_email,
    # "candidate_name": candidate_name,
    # "candidate_contact": candidate_contact,
    # "empId": empId,
    # "reschedule": False,
    # # "interviewId": "67991f7b7907a162cd1a0dcd",
    # "selected_slot": {
    #     "month_week": month_week,
    #     "day": day,
    #     "time_slot": time_slot
    # }
    # })
    # print("="*20)

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def getCandidateSlotOptionsFromAgent(jobId):

    url = f"{LOCAL_URL}/api/external-communications/get-candidate-slot-options/?jobId={jobId}"

    payload = {}
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()["data"][0]
    return data


def showCandidateSlotOptions(jobId):
    api_data = getCandidateSlotOptionsFromAgent(jobId)
    # Initialize session state for the API data (so that modifications persist)
    if "data" not in st.session_state:
        st.session_state["data"] = api_data

    # Initialize session state for the currently selected slot
    if "selected_slot" not in st.session_state:
        st.session_state["selected_slot"] = None

    st.write("## Available Slot Options")

    # Loop through each week and day to display options.
    # Each day is shown as an expander; inside, time slots are shown as buttons.
    print(f"st.session_state.data: {st.session_state.data}")
    for month_week, days in st.session_state.data.items():
        st.write(f"### {month_week}")
        for day, slots in days.items():
            # TODO: collapsing logic  if no slot is available
            with st.expander(day.capitalize()):
                # List available time slots for that day.
                for slot in list(slots.keys()):
                    if len(slots[slot]) == 0:
                        continue
                    # Mark the button label to indicate if it is selected.
                    label = slot
                    current_selection = st.session_state.selected_slot
                    if (
                        current_selection is not None
                        and current_selection.get("month_week") == month_week
                        and current_selection.get("day") == day
                        and current_selection.get("time_slot") == slot
                    ):
                        label = f"{slot} (selected)"
                    # When a slot button is clicked, update the selected slot globally.
                    if st.button(label, key=f"{month_week}_{day}_{slot}"):
                        select_slot(month_week, day, slot)

    # Display the currently selected slot.
    if st.session_state.selected_slot:
        st.write("### Currently Selected Slot:")
        st.write(st.session_state.selected_slot)
    else:
        st.write("No slot selected.")


def saveCandidateSlotPreferencePage():
    st.header("slot preference form")
    query_params = st.query_params
    jobId = query_params.get("jobId", None)
    candidate_name = query_params.get("candidate_name", None)
    candidate_email = query_params.get("candidate_email", None)
    candidate_contact = query_params.get("candidate_contact", None)

    if jobId is None:
        st.toast(
            "Please click on the link again or contact HR.", icon="⚠️"
        )  # Popup notification
        st.error("🚨 Access Denied: Please click on the link again or contact HR.")
        st.stop()  # Stops the script execution, preventing the rest of the page from loading

    # Example form inputs
    # candidate_name = st.text_input("candidate Name")
    # candidate_email = st.text_input("candidate email")
    # candidate_contact = st.text_input("candidate Contact")
    st.write(f"candidate name: {candidate_name}")
    st.write(f"candidate email: {candidate_email}")
    st.write(f"candidate contact: {candidate_contact}")

    showCandidateSlotOptions(jobId)
    if st.session_state.selected_slot is not None:
        user_selected_slot = st.session_state.selected_slot
        month_week, day, time_slot = (
            user_selected_slot["month_week"],
            user_selected_slot["day"],
            user_selected_slot["time_slot"],
        )

    if st.button("Submit"):
        try:
            empId = st.session_state.data[month_week][day][time_slot].pop()
        except Exception as e:
            logging.error(
                f"candidate with candidate email: {candidate_email} in the jobId: {jobId} error happened detailed error: {e}"
            )
            st.toast(
                "Please fill the details, select the slot then only hit the submit.",
                icon="⚠️",
            )  # Popup notification
            st.error(
                "🚨 Access Denied: Please click on the link again, fill the details and select a slot then also it doesn't resolve then contact HR."
            )
            st.stop()  # Stops the script execution, preventing the rest of the page from loading

        response = saveCandidateSlotPreferenceWithAgent(
            jobId,
            candidate_email,
            candidate_name,
            candidate_contact,
            empId,
            month_week,
            day,
            time_slot,
        )
        if response.status_code == 200:
            logging.info(
                f"response from the saveCandidateSlotPreferenceWithAgent API hit for the candidate_email: {candidate_email} and jobId : {jobId}"
            )
            st.write(
                f"Thanks for submitting we are creating your interview you will recieve a mail don't forget to tap yes on it"
            )
        elif response.status_code == 400:
            logging.info(
                f"some error happened but problem was at the user side for candidate_email: {candidate_email} and jobId: {jobId}"
            )
            response_dict = response.json()
            st.write(
                f"we faced some problem in processing your request read this message if you can do something: {response_dict}"
            )
        else:
            logging.info(
                f"some internal error occured for the candidate_email: {candidate_email} and jobId : {jobId}"
            )
            st.write(
                f"we faced some problem in processing your request if possible please mail us at yashtiwari.engineer@gmail.com"
            )
