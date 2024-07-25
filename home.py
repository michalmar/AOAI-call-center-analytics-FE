import streamlit as st
import os
from dotenv import load_dotenv
import time
from azure.core.exceptions import ResourceExistsError
final_arr=[]
load_dotenv()


if "info" not in st.session_state:
    st.session_state.info = None
#################################################################################
# App elements

st.set_page_config(layout="wide")
st.title("Call Center Analytics")


container_name = "cc-stage0-input"

def upload_file_to_blob(data, container_name, blob_name):
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    # with open(file_path, "rb") as data:
    #     blob_client.upload_blob(data)
    upload_info = blob_client.upload_blob(data)
    return upload_info

file = st.file_uploader("Upload a call recording", type=["wav"])
if file is not None:
    st.session_state.info = file
    try:
        upload_info = upload_file_to_blob(file, container_name, file.name)
        st.success(f"File {file.name} uploaded successfully.")
        st.info(f"The processing of the file just started. It may take a few minutes to complete. Check back in a while.")
        st.write(upload_info) 
    
    except ResourceExistsError:
        st.warning(f"The file {file.name} already exists in the container {container_name}.")
        # Handle the exception as needed, e.g., skip the upload or overwrite the file

    




# text = '''

# Supported scenarios & APIs:
# - :speech_balloon: [Offline Subtitles](./Subtitles) generated offline subtitles
# - :frame_with_picture: [Video Analytics](./Video_Analysis) video analytics dashboard
# '''

# st.markdown(text)