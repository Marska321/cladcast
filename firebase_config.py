# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore, storage
import streamlit as st
import json

def init_firebase():
    if not firebase_admin._apps:
        creds_json = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
        creds = credentials.Certificate(creds_json)
        storage_bucket_url = st.secrets["FIREBASE_STORAGE_BUCKET"]
        
        firebase_admin.initialize_app(creds, {'storageBucket': storage_bucket_url})
    
    return firestore.client(), storage.bucket()