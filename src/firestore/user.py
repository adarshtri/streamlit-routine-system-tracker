from google.cloud.firestore_v1 import DELETE_FIELD
import streamlit as st

from src.firestore.define_you import DefineYouDoc
from src.firestore.helpers import get_current_datetime_utc, create_hash, load_credentials


class UserDoc:

    def __init__(self, username):
        self.username = username
        self.client = load_credentials()
        self.doc_reference = self.client.collection(st.secrets["firestore_collection"]).document(username)
        self.__ensure_document_exists()
        self.__ensure_fields_exists()
        self.define_you = DefineYouDoc(username)

    def __ensure_fields_exists(self):

        doc_data = self.doc_reference.get()

        if "dates" not in doc_data.to_dict():
            self.doc_reference.update({
                "dates": {}
            })

        if "habits" not in doc_data.to_dict():
            self.doc_reference.update({
                "habits": []
            })

        if "jobs" not in doc_data.to_dict():
            self.doc_reference.update({
                "jobs": {}
            })

        if "weight" not in doc_data.to_dict():
            self.doc_reference.update({
                "weight": {}
            })

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

    def get_habit_tracking_for_all_dates(self):
        doc_data = self.doc_reference.get()
        return doc_data.to_dict()["dates"]

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

    def get_user_jobs(self, applied: bool = None):
        doc_data = self.doc_reference.get()
        jobs = doc_data.to_dict().get("jobs", None)

        if jobs is None:
            return []

        if applied is None:
            return [job for job in list(jobs.values())]

        return [job for job in list(jobs.values()) if job["applied"] == applied]


    def applied_to_job(self, job_data):
        self.doc_reference.update({
            f"jobs.{create_hash(job_data['job_url'])}": job_data
        })

    def untrack_job(self, job_data):
        self.doc_reference.update({
            f"jobs.{create_hash(job_data['job_url'])}": DELETE_FIELD
        })

    def track_weight(self, input_date, weight):
        self.doc_reference.update({
            f"weight.{input_date}": weight
        })

    def get_weight_for_date(self, input_date):
        doc_data = self.doc_reference.get()
        weights = doc_data.to_dict().get("weight", None)

        if not weights or input_date not in weights:
            return 0.0

        return weights[input_date]

    def get_all_weight(self):
        doc_data = self.doc_reference.get()

        weights = doc_data.to_dict().get("weight", None)

        if not weights:
            return {}

        return weights
