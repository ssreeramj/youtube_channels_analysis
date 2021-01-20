import json
import os
import re

import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build

from helper import get_all_videos
from plots import get_likes_fig

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

if __name__ == '__main__':
    st.title('Youtube Channel Analysis:rocket:')

    url = st.text_input(label='Enter the url of a youtube channel.')
    pattern = re.compile('^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+')

    if re.match(pattern, url):
        try:
            url = url.split('/')

            if url[-2] == 'channel':
                channel_id = url[-1]
                request_for_upload_id = youtube.channels().list(
                        part="snippet,statistics,contentDetails",
                        id=channel_id,
                    )
                upload_id_response = request_for_upload_id.execute()

            else:
                user_id = url[-1]
                request_for_upload_id = youtube.channels().list(
                        part="snippet,statistics,contentDetails",
                        forUsername=user_id,
                    )
                upload_id_response = request_for_upload_id.execute()

            try:
                channel_title = upload_id_response['items'][0]['snippet']['title']
                channel_desc = upload_id_response['items'][0]['snippet']['description']
                image_url = upload_id_response['items'][0]['snippet']['thumbnails']['high']['url']

                upload_id = upload_id_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

                total_views = upload_id_response['items'][0]['statistics']['viewCount'] 
                total_subs = upload_id_response['items'][0]['statistics']['subscriberCount'] 
                total_videos = upload_id_response['items'][0]['statistics']['videoCount'] 

                st.subheader(channel_title)
                st.image(image_url)
                st.write(channel_desc)

                st.write(f'Total Subscribers: {total_subs}')
                st.write(f'Total Views: {total_views}')
                st.write(f'Total Videos: {total_videos}')

                video_df = get_all_videos(youtube=youtube, upload_id=upload_id)
                st.write('hi')
                st.write(video_df.astype('object'))
                st.write('hi')

                likes_fig = get_likes_fig(video_df)
                st.plotly_chart(likes_fig)

            except Exception as e:
                st.write(e)
                st.subheader('Channel with this URL does not exist....Please enter a correct URL')

        except Exception:
            st.subheader('Could not get the video id, please paste the correct URL')

    else:
        st.subheader('Please enter a valid youtube channel URL')


