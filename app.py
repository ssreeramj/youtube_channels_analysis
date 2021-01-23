import json
import os
import re

import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build

from helper import get_all_videos
from plots import get_likes_fig, get_dislikes_fig, get_yearwise_plot, get_title_wordcloud, get_monthwise_plot, get_daywise_plot

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

    st.image('images/user_url.png', use_column_width=True)
    st.image('images/id_url.png', use_column_width=True, caption='Examples of valid URLs')

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

                col1, col2, col3 = st.beta_columns(3)
                col2.subheader(channel_title)
                st.image(image_url,  use_column_width=True)
                with st.beta_expander(label='Channel Description'):
                    st.write(channel_desc)

                with st.beta_expander(label='Channel Statistics',):
                    st.write(f'Total Videos: {total_videos}')
                    st.write(f'Total Views: {total_views}')
                    st.write(f'Total Subscribers: {total_subs}')

                video_df = get_all_videos(youtube=youtube, upload_id=upload_id)
                # st.write(video_df.astype('object'))

                st.header('Charts')
                st.markdown('##### (The dashed line in the below plots tells the median views of all videos)')

                st.markdown('### This chart tells gives us the information about **LIKE** percentage in a video. The bigger the marker, greater the :+1: %.')
                likes_fig = get_likes_fig(video_df)
                st.plotly_chart(likes_fig,  use_container_width=True)

                st.markdown('### This chart tells gives us the information about **DISLIKE** percentage in a video. The bigger the marker, greater the :-1: %.')
                dislikes_fig = get_dislikes_fig(video_df)
                st.plotly_chart(dislikes_fig,  use_container_width=True)

                st.markdown('### Here is the yearly video uploads on this channel')
                yearwise_fig = get_yearwise_plot(video_df)
                st.plotly_chart(yearwise_fig, use_container_width=True)

                st.markdown('### Here is the monthly video uploads on this channel')
                monthwise_fig = get_monthwise_plot(video_df)
                st.plotly_chart(monthwise_fig, use_container_width=True)

                st.markdown('### Here is the daywise video uploads on this channel')
                daywise_fig = get_daywise_plot(video_df)
                st.plotly_chart(daywise_fig, use_container_width=True)


                st.markdown('### Most often used words in the video title')
                title_wc = get_title_wordcloud(video_df)
                st.pyplot(title_wc)


            except Exception as e:
                st.write(e)
                st.subheader('Channel with this URL does not exist....Please enter a correct URL')

        except Exception as e:
            # st.write(e)
            st.subheader('Could not get the video id, please paste the correct URL')

    else:
        st.subheader('Please enter a valid youtube channel URL')


