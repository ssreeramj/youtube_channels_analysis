import plotly.express as px
import texthero as hero
import pandas as pd

pd.options.plotting.backend = "plotly"

LABELS = { 
    'upload_year': 'Year',
    'upload_date': 'Date',
    'upload_day': 'Day',
    'upload_month': 'Month',
    'views': 'Total Views', 
    'vid_dur': 'Video Length (mins)',
    'vid_title': 'Video Title',
    'dislikes_percent': 'Dislike Percentage',
    'likes_percent': 'Like Percentage',
    'vid_id': 'Total Videos',
}

def get_likes_fig(df):
    
    fig = px.scatter(
        data_frame=df,
        x='vid_dur',
        y='views',
        color='upload_year',
        size='likes_percent',
        opacity=0.4,
        hover_data=['vid_title'],
        labels=LABELS,  
        template='plotly_dark',  
    )
    fig.add_hline(y=df['views'].median(), line_dash='dash')

    # fig.show()
    return fig

def get_dislikes_fig(df):
    
    fig = px.scatter(
        data_frame=df,
        x='vid_dur',
        y='views',
        color='upload_year',
        size='dislikes_percent',
        opacity=0.6,
        hover_data=['vid_title'],
        labels=LABELS, 
        template='plotly_dark',  
    )
    fig.add_hline(y=df['views'].median(), line_dash='dash', )

    # fig.show()
    return fig

def get_yearwise_plot(df):

    yearwise = df.groupby('upload_year').count()['vid_id']

    fig = px.line(
        data_frame=yearwise,
        y='vid_id',
        labels=LABELS,
        template='plotly_dark',  
    )

    fig.update_layout(
        xaxis = dict(
            dtick = 1
        )
    )

    # fig.show()
    return fig

def get_monthwise_plot(df):
    df = df.groupby('upload_month').count()['vid_id']

    fig = px.line(
        data_frame=df,
        y='vid_id',
        labels=LABELS,
        template='plotly_dark',
    )

    fig.update_layout(
        xaxis = dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        )
    )
    fig.update_traces(mode='markers+lines')

    # fig.show()
    return fig

def get_daywise_plot(df):
    df = df.groupby('upload_day').count()['vid_id']

    fig = px.line(
        data_frame=df,
        y='vid_id',
        labels=LABELS,
        template='plotly_dark'
    )

    fig.update_layout(
        xaxis = dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        )
    )
    fig.update_traces(mode='markers+lines')
    # fig.show()
    return fig

def get_title_wordcloud(df):
    clean_title = df['vid_title'].pipe(hero.clean)
    
    fig = hero.visualization.wordcloud(clean_title, background_color='#101010', colormap='jet', height=250)

    return fig