from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('./data/netflix_titles.csv')

# Process data
# Type data
type_counts = df['type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']

# year data
year_counts = df['release_year'].value_counts().sort_index().reset_index()
year_counts.columns = ['Release Year', 'Count']

# country data
country_list = df["country"].str.split(",").explode().str.strip() #parsing multiple countries and adding them to the count
country_counts = country_list.value_counts().head(20)  #top 20 countries

titles = df['title'].count()

# language data
lang_keywords = {
    'Hindi': ['Bollywood', 'Indian'],
    'Japanese': ['Anime', 'Japanese'],
    'Korean': ['Korean', 'K-drama'],
    'Spanish': ['Spanish', 'Español', 'Mexico', 'Spanish-language'],
    'French': ['French', 'Paris'],
    'English': ['British', 'American', 'English']
}

language_counts = {}

for lang, keywords in lang_keywords.items():
    count = df[df['listed_in'].str.contains('|'.join(keywords), case=False, na=False) |
               df['description'].str.contains('|'.join(keywords), case=False, na=False)].shape[0]
    language_counts[lang] = count

# Convert to DataFrame
lang_df = pd.DataFrame(list(language_counts.items()), columns=['Language', 'Count']).sort_values(by='Count', ascending=False)

# ---- PIE CHART ----
fig_pie = px.pie(
    type_counts,
    names='Type',
    values='Count',
    color='Type',
    color_discrete_sequence=['#E50914', '#B20710'],  # Netflix reds
    hole=0.45,
)
fig_pie.update_layout(
    title=dict(
        text='Movies vs TV Shows',
        font=dict(size=18, color='white'),
        x=0.5,
        xanchor='center'
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    # showlegend=True,
    # legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=-0.2,
    #     xanchor="center",
    #     x=0.5,
    #     font=dict(size=12, color='white')
    # )
)
fig_pie.update_traces(
    textinfo='percent+label',
    textfont_size=14,
    marker=dict(line=dict(color='#121212', width=2)),
    hovertemplate='<b>%{label}</b><br>%{value} Titles<br>%{percent}',
)

# ---- BAR CHART ----
fig_bar = px.bar(
    year_counts.tail(30),  # Show last 15 years for clarity
    x='Release Year',
    y='Count',
    text='Count',
    color='Count',
    color_continuous_scale=['#B20710', '#E50914']
    )
fig_bar.update_layout(
        title=dict(
            text='Content Releases Over the Years',
            font=dict(size=18, color='white'),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        coloraxis_showscale=False,
    )
fig_bar.update_traces(
        textposition='outside',
        marker_line_color='#121212',
        marker_line_width=1.2,
        hovertemplate='<b>%{x}</b><br>%{y} Titles'
    )
# ---- CATEGORY ----
rating_groups = {
    'Kids': ['TV-Y', 'TV-Y7', 'TV-G', 'G', 'TV-Y7-FV'],
    'Teens': ['TV-PG', 'PG', 'PG-13', 'TV-14'],
    'Adults': ['TV-MA', 'R', 'NC-17', 'NR', 'UR']
}
def cat(x):
  for k ,v in rating_groups.items():
    if x['rating'] in v:
      return k
df['category']=df.apply(lambda x : cat(x),axis=1)
fig_hist = px.histogram(
    df,
    x='category',
    color='type',  # same as hue in seaborn
    barmode='group',  # side-by-side grouping
    color_discrete_sequence=['#E50914', "#B0262D"]  # Netflix-style colors
)

fig_hist.update_layout(
    title=dict(
        text='Rates of Category by Type',
        font=dict(size=18, color='white'),
        x=0.5
    ),
    xaxis=dict(
        title='Category',
        tickangle=45,
        tickfont=dict(size=11, color='white')
    ),
    yaxis=dict(
        title='Count',
        tickfont=dict(size=11, color='white')
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    legend=dict(
        title='Type',
    )
)

# ---- Top Countries ----
fig_country_bar = px.bar(
    country_counts,
    x = country_counts.values[::-1],
    y=country_counts.index[::-1],
    color='count',
    color_continuous_scale=['#B20710', '#E50914']
)
fig_country_bar.update_layout(
    title= dict(
        text= 'Top 20 countries ',
        font=dict(size=18, color='white'),
        x=0.5
    ),
    xaxis=dict(
        title='Country',
        tickangle=0,
        tickfont=dict(size=11, color='white'),
        showgrid=False
    ),
    yaxis=dict(
        title='Count',
        tickfont=dict(size=11, color='white'),
        showgrid=False
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
)

# ---- Language Bar Graph ----
fig_lang_bar = px.bar(
    lang_df,
    x=lang_df['Language'],
    y= lang_df['Count'],
)

fig_lang_bar.update_layout(
    title=dict(
        text='Language Based Content Division',
        font=dict(size=18, color='white'),
        x=0.5
    ),
    xaxis=dict(
        title='Language',
        tickangle=0,
        tickfont=dict(size=11, color='white'),
    ),
    yaxis=dict(
        title='Count',
        tickfont=dict(size=11, color='white'),
        showgrid=False
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
)

# ---- LAYOUT ----
layout = html.Div(
    children=[
        html.H1(
            [
                html.Span("E", style={'color': '#E50914'}),
                "xecutive ",
                html.Span("O", style={'color': '#E50914'}),
                "verview"
            ],
            style={
                'textAlign': 'center',
                'fontFamily': 'Segoe UI, sans-serif',
                'color': 'white',
                'fontWeight': '700',
                'fontSize': '2.5rem',
                'marginBottom': '10px'
            }
        ),
        html.P(
            "High-level summary of Netflix content trends and release evolution.",
            style={
                'textAlign': 'center',
                'color': '#ccc',
                'fontSize': '1.1rem',
                'marginBottom': '50px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "KPIs",
                            style={
                                'textAlign': 'center'
                            }
                        ),
                        html.Div(
                            [
                            html.P(
                            'No.of titles',
                            style={
                                'textAlign': 'center'
                            }
                            ),
                            html.P(
                                "Growth Rate",
                                style={
                                    'textAlign': 'center'
                                }
                            ),
                            html.P(
                                "No of countries",
                                style={
                                    'textAlign': 'center'
                                }
                            ),
                            html.P(
                                "No of Genres",
                                style={
                                    'textAlign': 'center'
                                }
                            ),
                            html.P(
                                "Diversity Index",
                                style={
                                    'textAlign': 'center'
                                }
                            ),
                            ],
                            style={
                                'display': 'flex',
                                'justify-content': 'space-between',
                                'gap': '0.1rem',
                                'flex-wrap': 'wrap'
                            }
                        )
                    ]
                )
            ],
            style={
                'width': 'full',
                'display':'flex',
                'flex-direction': 'column',
                'margin': '10px',
                'background': 'rgba(30,30,30,0.85)',
                'backdropFilter': 'blur(8px)',
                'borderRadius': '16px',
                'padding': '30px',
                'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
            }
        ),
        html.Div(
            [
                html.Div(
                    html.P(
                        "High Level Summary Charts",
                        style={
                            'flex': '1',
                            'margin': '10px',
                            'background': 'rgba(30,30,30,0.85)',
                            'backdropFilter': 'blur(8px)',
                            'borderRadius': '16px',
                            'padding': '30px',
                            'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                            'textAlign': 'center'
                        }
        ),
                )
            ],
            style={
                'width': 'full'
            }
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='bar-chart', figure=fig_bar, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth': '50%'
                    }
                ),
                html.Div(
                    dcc.Graph(id='pie-chart', figure=fig_pie, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth': '30%'
                    }
                ),
                html.Div(
                    dcc.Graph(id='histogram', figure=fig_hist, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth':'30%'
                        
                    }
                ),
                html.Div(
                    dcc.Graph(id='bar-chart', figure=fig_country_bar, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth':'50%'
                    }
                ),
                html.Div(
                    dcc.Graph(id='bar-chart', figure=fig_lang_bar, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                    }
                ),
            ],
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'alignItems': 'stretch',
                # 'maxWidth': '1100px',
                'margin': 'auto'
            }
        )
    ],
    className='exec-overview',
    style={
        'backgroundColor': '#121212',
        'minHeight': '100vh',
        'padding': '60px 20px',
        'fontFamily': 'Segoe UI, sans-serif',
        'overflow': 'scroll-y'
    }
)

