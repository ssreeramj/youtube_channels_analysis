import os
import streamlit as st

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

if __name__ == '__main__':
    st.title('Youtube Channel Analysis:rocket:')

    
