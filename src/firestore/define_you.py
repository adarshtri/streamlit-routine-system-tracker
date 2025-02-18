import streamlit as st
from firebase_admin.db import reference

from src.firestore.helpers import get_current_datetime_utc, load_credentials
from google.cloud import firestore


class DefineYouDoc:

    def __init__(self, username):
        self.username = username
        self.client = load_credentials()
        self.doc_reference = self.client.collection(st.secrets["firestore_define_you_collection"]).document(username)
        self.__ensure_document_exists()
        self.__ensure_fields_exists()

    def __ensure_fields_exists(self):

        doc_data = self.doc_reference.get()

        if "your_definition" not in doc_data.to_dict():
            self.doc_reference.update({
                "your_definition": {}
            })

        if "your_definition_tracking" not in doc_data.to_dict():
            self.doc_reference.update({
                "your_definition_tracking": {}
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

    def __has_define_you_definitions(self):
        doc_data = self.doc_reference.get()
        return 'your_definition' in doc_data.to_dict() and len(doc_data.to_dict()["your_definition"]) != 0

    def __get_user_define_you_definitions(self):
        if self.__has_define_you_definitions():
            doc_data = self.doc_reference.get()
            return doc_data.to_dict()["your_definition"]
        else:
            return {}

    def get_tracked_define_you_definitions(self):
        all_definitions = self.__get_user_define_you_definitions()
        to_remove = []

        for definition in all_definitions:
            if not all_definitions[definition]["tracked"]:
                to_remove.append(definition)

        for definition in to_remove:
            del all_definitions[definition]

        return all_definitions

    def get_historical_define_you_definitions(self):
        all_definitions = self.__get_user_define_you_definitions()
        to_remove = []

        for definition in all_definitions:
            if all_definitions[definition]["tracked"]:
                to_remove.append(definition)

        for definition in to_remove:
            del all_definitions[definition]

        return all_definitions

    def add_definition(self, definition):

        call_time = get_current_datetime_utc()

        current_definition = self.__get_user_define_you_definitions()

        if definition not in current_definition:
            self.doc_reference.update({
                f"your_definition.{self.client.field_path(definition)}": {
                    "tracked": True,
                    "created_at": call_time,
                    "updated_at": call_time,
                    "updates": {
                        str(call_time): {
                            "tracked": True
                        }
                    }
                }
            })
        else:
            if "tracked" in current_definition[definition] and current_definition[definition]["tracked"] == True:
                st.warning(f"Definition \"{definition}\" is already tracked.")
            else:
                updates = current_definition[definition]["updates"]
                updates[str(call_time)] = True
                self.doc_reference.update({
                    f"your_definition.{self.client.field_path(definition)}": {
                        "tracked": True,
                        "updated_at": call_time,
                        "updates": updates
                    }
                })

    def remove_definition(self, definition):

        call_time = get_current_datetime_utc()

        current_definition = self.__get_user_define_you_definitions()

        if definition not in current_definition:
            st.warning(f"Definition \"{definition}\" is not tracked. Can't be removed.")
        else:
            if "tracked" in current_definition and current_definition[definition]["tracked"] == False:
                st.warning(f"Definition \"{definition}\" is already not being tracked.")
            else:
                updates = current_definition[definition]["updates"]
                updates[str(call_time)] = False
                self.doc_reference.update({
                    f"your_definition.{self.client.field_path(definition)}": {
                        "tracked": False,
                        "updated_at": call_time,
                        "updates": updates
                    }
                })

    def celebrate(self, definition):
        celebrate_doc = self.doc_reference.collection("celebrations").document(definition)
        celebrate_doc.set({
            "celebrations": firestore.ArrayUnion([{
                "created_at": get_current_datetime_utc()
            }])
        }, merge=True)

    def get_celebration_data(self, definition):
        definition_celebration_reference = self.doc_reference.collection("celebrations").document(definition)
        reference_doc = definition_celebration_reference.get()

        if reference_doc.exists:
            celebrations = reference_doc.to_dict().get("celebrations")
            return  celebrations
        return []