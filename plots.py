import plotly.express as px

LABELS = { 
    'upload_year': 'Year', 
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
    )
    fig.add_hline(y=df['views'].median(), line_dash='dash', )

    # fig.show()
    return fig

def get_yearwise_plot(df):

    yearwise = df.groupby('upload_year').count()['vid_id']

    fig = px.line(
        data_frame=yearwise,
        y='vid_id',
        labels=LABELS
    )

    fig.update_layout(
        xaxis = dict(
            dtick = 1
        )
    )

    # fig.show()
    return fig