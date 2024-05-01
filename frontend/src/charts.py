import plotly.express as px

def chart_daily_stock(df):
    df = df.sort_values('date')
    fig = px.line(
        data_frame=df,
        x='date',
        y='stock',
        title='Daily stock',
    )
    # fig.update_xaxes(tickmode='linear')
    fig.update_yaxes(rangemode='tozero')
    return fig