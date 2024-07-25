import streamlit as st
import os
from dotenv import load_dotenv
import time


# final_arr=[]
load_dotenv()


if "info" not in st.session_state:
    st.session_state.info = None
if "recordings" not in st.session_state:
    st.session_state.recordings = None
if "recording" not in st.session_state:
    st.session_state.recording = None
if "selected_recording" not in st.session_state:
    st.session_state.selected_recording = None

container_name = "cc-stage2-transcript-analysis"
# load the processed recordings from the Azure Blob Storage
def load_recordings_from_blob(container_name):
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    recordings = [blob.name for blob in blob_list]
    # recordings = blob_list
    # st.session_state.recordings = recordings
    return recordings


def get_blob_by_name(container_name, blob_name):
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client

def download_blob(blob_client):
    # import io
    stream = blob_client.download_blob()
    binary_content = stream.readall()
    text_content = binary_content.decode('utf-8')
    return text_content

def invoke_function(recording_name):
    # Define the function to be invoked when the button is clicked
    # st.write(f"Function invoked with recording: {recording_name}")
    st.session_state.selected_recording = recording_name
    blob_stream = download_blob(get_blob_by_name(container_name, recording_name))
    st.session_state.recording = blob_stream


def display_recordings(recordings):
    for recording_name in recordings:
        col2, col3 = st.columns([5, 2])
        with col2:
            st.write(recording_name)
        with col3:
            if st.button(f"show details"):
                invoke_function(recording_name)

if st.session_state.recordings is None:
    st.session_state.recordings = load_recordings_from_blob(container_name)
else:
    st.info(f"Recordings already loaded.")

display_recordings(st.session_state.recordings)


if st.session_state.recording is not None:
    with st.container(border=True):
        st.write(st.session_state.recording)
