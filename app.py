from forms.candidateSheetIngestion import candidateSheetIngestionPage
from forms.interviewPoolCreation import interviewPoolCreationPage
from forms.saveEmployeeAvailabilitySlots import saveEmployeeAvailabilitySlotsPage
from forms.saveCandidateSlotPreference import saveCandidateSlotPreferencePage

from forms.userRegistration import userRegistrationPage
from pages.home import home_page
import streamlit as st


# This function will handle page navigation
def main():
    page = st.sidebar.radio(
        "Select Page",
        [
            "Home",
            "User Registration",
            "Create New Job",
            "Insert Candidate Sheet",
            "employee availability slots",
            "candidate slot selection",
        ],
    )

    if page == "Home":
        home_page()
    elif page == "User Registration":
        userRegistrationPage()
    elif page == "Create New Job":
        interviewPoolCreationPage()
    elif page == "Insert Candidate Sheet":
        candidateSheetIngestionPage()
    elif page == "employee availability slots":
        saveEmployeeAvailabilitySlotsPage()
    elif page == "candidate slot selection":
        saveCandidateSlotPreferencePage()
    # elif page == "Ingest Resumes":
    #     ingestResumes()
    # elif page == "Download Report":
    #     downloadReport()
    # elif page == "Settings":
    #     st.title("Settings Page")


if __name__ == "__main__":
    main()
