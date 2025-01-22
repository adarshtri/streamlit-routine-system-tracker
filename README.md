# Routine System Tracker

This is a streamlit app. 
* This app was originally designed to created a personal tracker using mindfulness.
* The user wanting to track certain aspects of their life need to log data related to it. 
* The logged data is represented with various visual representation.

---

**Data never lies!**

-------

## Setup local secrets

On Mac/Linux based systems -

```
mkdir .streamlit
cd .streamlit
vi secrets.toml
# paste below content and save the file. Don't forget to replace sample values with values you want.
```

Follow Part 2 of [this blog](https://blog.streamlit.io/streamlit-firestore/) to get your firestore setup and service account json ready. 
The service account json is used to run this app with your own firestore setup. Read more about firestore [here](https://firebase.google.com/docs/firestore).

```
textkey = "firestore-service-account-json-escaped"
security_key = "sample_security_key"
supported_users = "{\n \"user1\": \"password1\", \n\"user2\": \"password2\"\n}"
firestore_collection = "routine-system-tracker"
```

## How to run the app?

On Mac/Linux based systems - 

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
streamlit run app.py
```