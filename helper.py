import os
import datetime
import json

import streamlit as st
import numpy as np
import pandas as pd

COLUMNS = [
    'vid_id', 'vid_title', 'vid_description', 'thumbnail_url', 'upload_time', 
    'duration', 'views', 'likes', 'dislikes', 'comment_counts',
]

INT_COLS = ['views', 'likes', 'dislikes', 'comment_counts']
CATEGORY_COLS = ['upload_year', 'upload_month', 'upload_date', 'upload_hour', 'upload_minute', 'upload_second', 'upload_day']

def add_video_data(res):
    data = []

    for items in res['items']:
        video_id = items['snippet']['resourceId']['videoId']
        video_title = items['snippet'].get('title', '')
        video_desc = items['snippet'].get('description', '')
        upload_time = items['snippet'].get('publishedAt', '')
        thumbnail_url = items['snippet']['thumbnails']['high'].get('url', '')

        # print(video_title, upload_time, thumbnail_url)
        temp = [video_id, video_title, video_desc, thumbnail_url, upload_time] + [''] * 5
        data.append(temp)
    
    return data


def get_video_stats(res):
    data = []

    for items in res['items']:
        duration = items['contentDetails'].get('duration', 'PT0S')
        views = items['statistics'].get('viewCount', 0)
        likes = items['statistics'].get('likeCount', 0)
        dislikes = items['statistics'].get('dislikeCount', 0)
        comment_count = items['statistics'].get('commentCount', 0)
        
        temp = [duration, views, likes, dislikes, comment_count]
        data.append(temp)

    return data


def convert_dur(s):
    mapp = { 'H': '*60', 'M': '*1', 'S': '/60' }
    time, val, units, prev_char = 0, [], [], True
    for char in s[2:]:
        if char.isdigit():
            if prev_char:
                val.append(char)
            else:
                val[-1] += char
            prev_char = False
        else:
            units.append(char)
            prev_char = True
           
    for u, v in zip(units, val):
        time += eval(v+mapp[u])
        
    return time


def preprocess_data(raw):
    raw[INT_COLS] = raw[INT_COLS].astype(int)

    raw['upload_date'] = raw['upload_time'].apply(
    lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").day
    )
    raw['upload_month'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").month
    )
    raw['upload_year'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").year
    )
    raw['upload_hour'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").hour
    )
    raw['upload_minute'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").minute
    )
    raw['upload_second'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").second
    )
    raw['upload_day'] = raw['upload_time'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").strftime('%w')
    ) 

    raw[CATEGORY_COLS] = raw[CATEGORY_COLS].astype('category')

    raw['vid_dur'] = raw['duration'].apply(lambda x: convert_dur(x))
    raw['likes_percent'] = raw['likes'] * 100 / (raw['likes'] + raw['dislikes'])
    raw['dislikes_percent'] = raw['dislikes'] * 100 / (raw['likes'] + raw['dislikes'])

    raw['likes_percent'].fillna(0, inplace=True)
    raw['dislikes_percent'].fillna(0, inplace=True)

    return raw

@st.cache()
def get_all_videos(youtube, upload_id):

    all_data = []
    video_stats = []

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=upload_id,
        maxResults=50,
    )
    response = request.execute()

    data = add_video_data(response)
    all_data.extend(data)

    next_page_token = response.get('nextPageToken', 0)

    while next_page_token:
        next_request = youtube.playlistItems().list_next(request, response)
        next_response = next_request.execute()

        data = add_video_data(next_response)
        all_data.extend(data)

        next_page_token = next_response.get('nextPageToken', 0)
        request, response = next_request, next_response
    
    df = pd.DataFrame(all_data, columns=COLUMNS)
    # print(','.join(df['vid_id'].values))
    total_videos = df.shape[0]

    for i in range(0, total_videos, 50):
        request = youtube.videos().list(
            part="statistics, contentDetails",
            id=','.join(df['vid_id'].values[i:i+50]),
        )
        response = request.execute()

        data = get_video_stats(response)
        video_stats.extend(data)
    # print(video_stats)

    df.iloc[:, 5:] = video_stats

    df = preprocess_data(df)

    return df

