import json
from google.cloud import firestore
from google.cloud.firestore_v1 import DELETE_FIELD
from google.oauth2 import service_account
import streamlit as st
import hashlib
from datetime import datetime
import pytz


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


class UserDoc:

    def __init__(self, username):
        self.username = username
        self.client = load_credentials()
        self.doc_reference = self.client.collection("routine-system-tracker").document(username)
        self.__ensure_document_exists()

    def __ensure_document_exists(self, initial_data=None):
        """
        Ensures that the document exists in Firestore. If it does not exist, creates it.

        Args:
            initial_data (dict, optional): Initial data to set in the document if it doesn't exist.
                                           Defaults to an empty dictionary.
        """
        initial_data = initial_data or {}

        # Check if the document exists
        doc_snapshot = self.doc_reference.get()
        if not doc_snapshot.exists:
            # Create the document with the initial data
            self.doc_reference.set(initial_data)

    def user_exists(self):
        return self.doc_reference.get().exists

    def has_habits_defined(self):
        doc_data = self.doc_reference.get()
        return 'habits' in doc_data.to_dict() and len(doc_data.to_dict()["habits"]) != 0

    def get_habits(self):
        if self.has_habits_defined():
            doc_data = self.doc_reference.get()
            return doc_data.to_dict()["habits"]
        else:
            return None

    def update_habits(self, habits):
        self.doc_reference.update({
                'habits': habits
        })

    def update_tracking_for_a_date(self, input_date, check_box_dict):
        self.doc_reference.update({
            f"dates.{input_date}": check_box_dict
        })

    def get_tracking_for_a_date(self, input_date):
        doc_data = self.doc_reference.get()
        dates_data = doc_data.to_dict()["dates"]
        if input_date in dates_data:
            return dates_data[input_date]
        return None

    def add_job_tracking(self, job_url, company_name, role_name):
        doc_data = self.doc_reference.get()
        jobs = doc_data.to_dict().get("jobs", None)

        if jobs is None:
            self.doc_reference.update({
                "jobs": {}
            })

        doc_data = self.doc_reference.get()
        jobs = doc_data.to_dict()["jobs"]

        if create_hash(job_url) not in jobs:
            self.doc_reference.update({
                f"jobs.{create_hash(job_url)}": {
                    "job_url": job_url,
                    "company_name": company_name,
                    "creation_time": get_current_datetime_utc(),
                    "applied": False,
                    "role_name": role_name
                }
            })
            return True
        return False

    def get_user_jobs(self, applied: bool):
        doc_data = self.doc_reference.get()
        jobs = doc_data.to_dict().get("jobs", None)

        if jobs is None:
            return []

        job_values = [job for job in list(jobs.values()) if job["applied"] == applied]
        return job_values

    def toggle_apply_job(self, job_data):
        self.doc_reference.update({
            f"jobs.{create_hash(job_data['job_url'])}": job_data
        })

    def untrack_job(self, job_data):
        self.doc_reference.update({
            f"jobs.{create_hash(job_data['job_url'])}": DELETE_FIELD
        })

