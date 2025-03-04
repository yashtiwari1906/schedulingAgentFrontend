import logging
from forms.utils import showJobsOnScreen
import streamlit as st
import requests


# def ingestResumes():
#     st.header("Create Job")

#     # Example form inputs
#     name = st.text_input("Name")
#     email = st.text_input("Email")

#     if st.button("Submit"):
#         st.write(f"Name: {name}, Email: {email}")


import streamlit as st
import io

from constants import CLOUD_RUN_URL, AGENT_SERVER_URL


def candidateSheetIngestionWithAgent(jobId, candidate_sheet):

    url = f"{AGENT_SERVER_URL}/api/external-communications/candidate-sheet-insertion/?jobId={jobId}"

    payload = {}

    files = [("candidate_sheet", (candidate_sheet.name, candidate_sheet, "text/csv"))]

    headers = {"Content-Type": "application/json"}

    # Perform the POST request
    with requests.Session() as session:
        try:
            response = session.post(url, data=payload, files=files)
            return response

        except Exception as e:
            print(f"Error occurred: {e}")

        # Ensure files are closed after the request is sent
        finally:
            # Close the opened files to avoid resource leakage
            for _, file_tuple in files:
                file_tuple[1].close()

    return None


def candidateSheetIngestionPage():
    """Creates the form to upload csv file and enter parameters."""
    st.header("select the job for which you want to upload candidate sheet")

    client_name = st.text_input("client name eg. meta, google, etc")
    jobId = showJobsOnScreen(client_name=client_name)

    st.header("okay now upload your candidate sheet")

    # csv upload
    uploaded_candidate_sheet = st.file_uploader(
        "Upload candidate sheet", type=["csv"], accept_multiple_files=False
    )
    # logging.error(f"type uploaded_pdf {type(uploaded_pdf)}")
    # logging.error(f"uploaded_pdf : {uploaded_pdf}")

    if uploaded_candidate_sheet is not None:

        # Button to submit the form (you could add further logic here, e.g., saving the data or processing it)
        if st.button("Submit"):
            response = candidateSheetIngestionWithAgent(jobId, uploaded_candidate_sheet)

            if response == None:
                logging.info(
                    f"some error occured while uploading the candidate to agent for jobId: {jobId}"
                )
                st.write(
                    "candidate sheet ingestion failed sorry we will reach shortly or if you can you can write us at yashtiwari1906@gmail.com"
                )
                return

            if response.status_code == 400:
                logging.info(
                    f"some error happened but problem was at the user side for jobId: {jobId}"
                )
                response_dict = response.json()
                st.write(
                    f"we faced some problem in processing your request read this message if you can do something: {response_dict}"
                )
                return

            if response.status_code == 500:
                logging.info(f"some internal error occured for the jobId: {jobId}")
                st.write(
                    f"Sorry for the incovenience but some error had occured we will shortly look into it if possible mail us at yashtiwari1906@gmail.com"
                )
                return

            response_dict = response.json()
            data = response_dict["data"]
            st.success("candidate sheet ingested successfully I will start reaching out to the candidates from tomorrow!")

            # Here, you can add logic to handle the form submission, like saving the data to a database or further processing
