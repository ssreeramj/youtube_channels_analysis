import json
import os
import re

import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build

from helper import get_all_videos
from plots import get_likes_fig, get_dislikes_fig, get_yearwise_plot, get_title_wordcloud

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="YT-Analysis",
    page_icon=':fire:',
)


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
                st.image(image_url,  use_column_width=True)
                st.write(channel_desc)

                st.subheader(f'Total Videos: {total_videos}')
                st.subheader(f'Total Views: {total_views}')
                st.subheader(f'Total Subscribers: {total_subs}')

                video_df = get_all_videos(youtube=youtube, upload_id=upload_id)
                # st.write(video_df.astype('object'))

                st.text('Here is a chart where the size of the marker represents LIKE percent in the video')
                likes_fig = get_likes_fig(video_df)
                st.plotly_chart(likes_fig,  use_container_width=True)

                st.text('Here is a chart where the size of the marker represents DISLIKE percent in the video')
                dislikes_fig = get_dislikes_fig(video_df)
                st.plotly_chart(dislikes_fig,  use_container_width=True)

                st.text('This chart shows the yearwise uploads on the channel')
                yearwise_fig = get_yearwise_plot(video_df)
                st.plotly_chart(yearwise_fig, use_container_width=True)

                st.text('This image shows the most frequent words used the title of the video')
                title_wc = get_title_wordcloud(video_df)
                st.pyplot(title_wc)


            except Exception as e:
                st.write(e)
                st.subheader('Channel with this URL does not exist....Please enter a correct URL')

        except Exception:
            st.subheader('Could not get the video id, please paste the correct URL')

    else:
        st.subheader('Please enter a valid youtube channel URL')


