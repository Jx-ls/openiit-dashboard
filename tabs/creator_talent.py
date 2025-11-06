from dash import html, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import dash_cytoscape as cyto


# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------
df = pd.read_csv('./data/netflix_titles.csv')
df.fillna('', inplace=True)
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df['listed_in'] = df['listed_in'].astype(str)

# --- Helper splitters ---
def split_people(s):
    return [x.strip() for x in s.split(',') if x.strip()] if isinstance(s, str) and s.strip() else []

def parse_year_added(s):
    try:
        return pd.to_datetime(s).year
    except Exception:
        return np.nan

df['year_added'] = df['date_added'].apply(parse_year_added)

# --- Prepare lists ---
dir_rows, act_rows = [], []

for _, row in df.iterrows():
    base = {
        'title': row.get('title', ''),
        'type': row.get('type', ''),
        'release_year': row.get('release_year', np.nan),
        'genres': [g.strip() for g in row.get('listed_in', '').split(',') if g.strip()],
        'country': row.get('country', ''),
        'rating': row.get('rating', ''),
        'duration': row.get('duration', ''),
        'year_added': row.get('year_added', np.nan),
        'description': row.get('description', ''),
    }

    # Director entry
    if isinstance(row['director'], str) and row['director'].strip():
        dir_rows.append({
            **base,
            'name': row['director'].strip(),
            'role': 'Director'
        })

    # Actor entries
    for actor in split_people(row['cast']):
        act_rows.append({
            **base,
            'name': actor,
            'role': 'Actor'
        })

# --- Combine ---
creators_df = pd.DataFrame(dir_rows + act_rows)
creator_names = sorted(creators_df['name'].dropna().unique().tolist())

# ---------- Rising Stars Computation ----------
# ---------- Improved Rising Stars Computation ----------
RECENT_YEARS = 5
max_year_added = int(pd.Series(df['year_added']).dropna().max()) if pd.Series(df['year_added']).notna().any() else None

if max_year_added:
    recent_cut = max_year_added - RECENT_YEARS + 1

    # Group by creator
    grp = creators_df.dropna(subset=['year_added']).groupby(['name'])

    # Count recent and old works
    stats_recent = grp.apply(lambda g: (g['year_added'] >= recent_cut).sum()).rename('recent_count')
    stats_old = grp.apply(lambda g: (g['year_added'] < recent_cut).sum()).rename('old_count')
    stats_total = grp.size().rename('total_count')

    rising = pd.concat([stats_recent, stats_old, stats_total], axis=1).fillna(0)

    # Rising score: high recent count, low old count
    rising['rising_score'] = (rising['recent_count'] / rising['total_count']) * (1 / (1 + rising['old_count']))

    # Filter for meaningful candidates
    rising = rising[
        (rising['recent_count'] >= 2) &            # at least 2 recent works
        (rising['total_count'] >= 2) &             # at least 2 total works
        (rising['old_count'] == 0)                 # true newcomers: no old works
    ]

    # Rank and take top 10
    rising_top10 = rising.sort_values(['rising_score', 'recent_count'], ascending=[False, False]).head(10).reset_index()

else:
    rising_top10 = pd.DataFrame(columns=['name', 'recent_count', 'old_count', 'total_count', 'rising_score'])



# ----------------------------------------------------------
# Layout (Netflix-Themed)
# ----------------------------------------------------------
layout = html.Div(
    children=[
        html.H1(
            children=[
                html.Span("C", style={'color': '#E50914'}),
                "reator and ",
                html.Span("T", style={'color': '#E50914'}),
                "alent Overview"
            ],
            style={'padding': 0, 'margin': 0, 'color': 'white'}
        ),
        html.P(
            "Select a creator to see their genre distribution.",
            style={'padding': 0, 'margin': 0, 'color': '#CCCCCC'}
        ),
        dcc.Dropdown(
            id='creator-search',
            options=[{'label': name, 'value': name} for name in creator_names],
            placeholder='Search for a director or actor...',
            style={
                'width': '50%',
                'margin': '20px auto',
                'color': 'black'
            },
            value='Anupam Kher',
            searchable=True,
            clearable=True
        ),
        html.Div(
            [
                # Genre Chart
                html.Div(
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth': '40%'
                    }
                ),
                # Type Pie
                html.Div(
                    dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth': '40%'
                    }
                ),
                # Activity Line
                html.Div(
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
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
                # Collaboration Graph
                html.Div(
                    cyto.Cytoscape(
                        id='collab-graph',
                        layout={'name': 'cose', 'animate': False},
                        stylesheet=[
                            {
                                'selector': 'node',
                                'style': {
                                    'content': 'data(label)',
                                    'font-size': '12px',
                                    'color': '#FFFFFF',
                                    'text-outline-color': '#E50914',
                                    'text-outline-width': 2,
                                    'background-color': '#E50914',
                                    'border-color': '#FFFFFF',
                                    'border-width': 1
                                }
                            },
                            {
                                'selector': '[role = "Director"]',
                                'style': {'background-color': '#B81D24', 'shape': 'triangle'}
                            },
                            {
                                'selector': '[role = "Actor"]',
                                'style': {'background-color': '#E50914', 'shape': 'ellipse'}
                            },
                            {
                                'selector': 'edge',
                                'style': {
                                    'line-color': '#777777',
                                    'width': 1.5,
                                    'target-arrow-color': '#777777',
                                    'target-arrow-shape': 'vee',
                                    'curve-style': 'bezier'
                                }
                            },
                            {
                                'selector': ':selected',
                                'style': {
                                    'border-color': '#FFFFFF',
                                    'border-width': 3,
                                    'background-color': '#FFFFFF',
                                    'color': '#E50914'
                                }
                            }
                        ],
                        style={'width': '100%', 'height': '420px', 'backgroundColor': 'rgba(0,0,0,0)'},
                        elements=[]
                    ),
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
                # Rising Stars
                html.Div(
                    dcc.Graph(id='rising-stars-bar', figure={}, config={'displayModeBar': False}),
                    className='chart-card',
                    style={
                        'flex': '1',
                        'margin': '10px',
                        'background': 'rgba(30,30,30,0.85)',
                        'backdropFilter': 'blur(8px)',
                        'borderRadius': '16px',
                        'padding': '30px',
                        'boxShadow': '0 4px 30px rgba(0, 0, 0, 0.4)',
                        'minWidth': '40%'
                    }
                ),
            ],
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'center',
                'alignItems': 'stretch',
                'margin': 'auto'
            }
        ),
    ],
    className='genre-int',
    style={
        'backgroundColor': '#000000',
        'minHeight': '100vh',
        'minWidth': '90vw',
        'padding': '60px 20px',
        'fontFamily': 'Segoe UI, sans-serif',
        'overflowY': 'scroll',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center'
    }
)


# ----------------------------------------------------------
# Callbacks
# ----------------------------------------------------------
@callback(Output("bar-chart", "figure"), Input('creator-search', "value"))
def generate_genre_bar_graph(selected_name):
    if not selected_name:
        fig = px.bar(pd.DataFrame({'x': [], 'y': []}), x='x', y='y')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    sub_df = creators_df[creators_df['name'] == selected_name]
    all_genres = [g for lst in sub_df['genres'] for g in lst if g]

    if not all_genres:
        fig = px.bar(title=f"No genre data available for {selected_name}")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        return fig

    genre_counts = pd.Series(all_genres).value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    fig = px.bar(genre_counts, x='Genre', y='Count', title=f"Genre Distribution for {selected_name}",
                 text='Count', color_discrete_sequence=['#E50914'])
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title='Genre',
        yaxis_title='Count',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font=dict(size=20, color='white'),
        margin=dict(l=40, r=20, t=60, b=60)
    )
    return fig


@callback(Output("pie-chart", "figure"), Input('creator-search', "value"))
def generate_type_pie_chart(selected_name):
    if not selected_name:
        fig = px.pie(pd.DataFrame({'x': [], 'y': []}), names='x', values='y')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    sub_df = creators_df[creators_df['name'] == selected_name]
    if sub_df.empty:
        fig = px.pie(pd.DataFrame({'x': [], 'y': []}), names='x', values='y')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    type_counts = sub_df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig = px.pie(type_counts, names='Type', values='Count',
                 title=f"Content Type Split for {selected_name}", hole=0.4,
                 color_discrete_sequence=['#E50914', '#B81D24'])
    fig.update_traces(textinfo='label+percent', pull=[0.05]*len(type_counts))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font=dict(size=20, color='white'),
        margin=dict(l=40, r=20, t=60, b=60),
        legend=dict(title='', orientation='h', y=-0.1, font=dict(color='white'))
    )
    return fig


@callback(Output("line-chart", "figure"), Input('creator-search', "value"))
def generate_active_year_line_chart(selected_name):
    if not selected_name:
        fig = px.line(pd.DataFrame({'x': [], 'y': []}), x='x', y='y')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    sub_df = creators_df[creators_df['name'] == selected_name]
    yearly_counts = (
        sub_df.dropna(subset=['release_year'])
              .groupby('release_year').size()
              .reset_index(name='Count')
              .sort_values('release_year')
    )

    if yearly_counts.empty:
        fig = px.line(pd.DataFrame({'x': [], 'y': []}), x='x', y='y')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    fig = px.line(yearly_counts, x='release_year', y='Count',
                  title=f"Yearly Activity of {selected_name}", markers=True)
    fig.update_traces(line=dict(width=3, color='#E50914'), marker=dict(size=8, color='#B81D24'))
    fig.update_layout(
        yaxis_title='Titles',
        xaxis=dict(
            title='Release Year',
            showgrid=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font=dict(size=20, color='white'),
        margin=dict(l=40, r=20, t=60, b=60),
        hovermode='x unified'
    )
    return fig


@callback(Output('rising-stars-bar', 'figure'), Input('creator-search', 'value'))
def rising_stars(_):
    if rising_top10.empty:
        fig = px.bar(title="Rising Stars (Insufficient Data)")
    else:
        plotdf = rising_top10.copy()
        plotdf['Label'] = plotdf['name'] + ' (' + plotdf['recent_count'].astype(int).astype(str) + '/' + plotdf['total_count'].astype(int).astype(str) + ')'
        fig = px.bar(plotdf, x='Label', y='rising_score', text='rising_score',
                     title=f"Rising Stars (Last {RECENT_YEARS} Years)",
                     color_discrete_sequence=['#E50914'])
        fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        fig.update_xaxes(tickangle=45)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(l=40, r=20, t=60, b=120),
        yaxis=dict(tickformat=".0%", gridcolor='#333333'),
        title_font=dict(size=20, color='white')
    )
    return fig


# ----------------------------------------------------------
# Cytoscape Callback
# ----------------------------------------------------------
@callback(Output('collab-graph', 'elements'), Input('creator-search', 'value'))
def build_collab_graph(selected_name):
    if not selected_name:
        return []

    involved_titles = creators_df[creators_df['name'] == selected_name]['title'].unique().tolist()
    sub_df = df[df['title'].isin(involved_titles)]

    nodes, edges = {}, []

    sel_role = creators_df[creators_df['name'] == selected_name]['role'].mode()[0] if not creators_df[creators_df['name'] == selected_name].empty else 'Actor'
    nodes[selected_name] = {'data': {'id': selected_name, 'label': selected_name, 'role': sel_role}}

    for _, row in sub_df.iterrows():
        director = row['director'].strip() if isinstance(row['director'], str) else ''
        cast = split_people(row['cast'])

        if director and director not in nodes:
            nodes[director] = {'data': {'id': director, 'label': director, 'role': 'Director'}}
        for actor in cast:
            if actor not in nodes:
                nodes[actor] = {'data': {'id': actor, 'label': actor, 'role': 'Actor'}}

        if director:
            for actor in cast:
                edges.append({'data': {'source': director, 'target': actor}})
        if selected_name in cast:
            for a in cast:
                if a != selected_name:
                    edges.append({'data': {'source': selected_name, 'target': a}})

    if len(nodes) > 60:
        deg = {}
        for e in edges:
            deg[e['data']['source']] = deg.get(e['data']['source'], 0) + 1
            deg[e['data']['target']] = deg.get(e['data']['target'], 0) + 1
        keep = {selected_name}
        keep |= set(sorted(deg, key=lambda k: -deg[k])[:40])
        nodes = {k:v for k,v in nodes.items() if k in keep}
        edges = [e for e in edges if e['data']['source'] in keep and e['data']['target'] in keep]

    return list(nodes.values()) + edges
