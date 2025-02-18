import hashlib
import json
from datetime import datetime
import pytz
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account


def get_current_datetime_utc():
    # Get the current UTC time
    utc_now = datetime.now(pytz.utc)
    # Format as string
    return utc_now.strftime("%Y-%m-%d %H:%M:%S")


def create_hash(input_string):
    # Convert the input string to bytes
    input_bytes = input_string.encode('utf-8')
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(input_bytes)
    # Return the hexadecimal representation of the hash
    return hash_object.hexdigest()


@st.cache_resource
def load_credentials():
    # Authenticate to Firestore with the JSON account key.
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    fire_store_client = firestore.Client(credentials=creds)
    return fire_store_client
