from forms.saveEmployeeAvailabilitySlots import saveEmployeeAvailabilitySlotsPage
from forms.saveCandidateSlotPreference import saveCandidateSlotPreferencePage

from pages.home import home_page
import streamlit as st

# This function will handle page navigation
def main():
    page = st.sidebar.radio("Select Page", ["Home", "employee availability slots", "candidate slot selection"])
    
    if page == "Home":
        home_page()
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
