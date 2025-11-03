import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=['/assets/style.css'],
                title='Team Sigmoid')

app.layout = dbc.Container([

    html.Div(id='theme-output-link', children=[
        html.Link(rel='stylesheet', href='/assets/dark.css', id='theme-link')
    ], style={'display': 'none'}),

    html.Div(
        children=[        
            html.Div(
                children=[
                    html.Div(style={'height': '1px'}),
                    html.Div(
                        children=[
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab1.svg'), id='tab-icon-1', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab2.svg'), id='tab-icon-2', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab3.svg'), id='tab-icon-3', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab4.svg'), id='tab-icon-4', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab5.svg'), id='tab-icon-5', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab6.svg'), id='tab-icon-6', className='tab-icon')),
                            dbc.NavItem(html.Img(src=app.get_asset_url('Tab/Tab7.svg'), id='tab-icon-7', className='tab-icon')),
                        ],
                        className='tabs'
                    ),
                    dbc.NavItem(html.Img(src=app.get_asset_url('Theme.svg'), id='theme-switcher', className='theme-switcher-icon'))
                ],
                className='nav-icons',
            ),
            html.Div(id='page-content'),
        ],
        className='container'
    ),
    dcc.Store(id='current-theme', data='dark'),
], fluid=True, className="dashboard-container")

tab_icon_outputs = [Output(f'tab-icon-{i}', 'className') for i in range(1, 8)]
tab_icon_inputs = [Input(f'tab-icon-{i}', 'n_clicks') for i in range(1, 8)]

@app.callback(
    tab_icon_outputs,
    tab_icon_inputs,
)
def update_active_tab_style(*args):
    
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id
    
    base_class = 'tab-icon'
    new_class_names = []
    
    for i in range(1, 8):
        icon_id = f'tab-icon-{i}'
        
        if not triggered_id and i == 1:
            new_class_names.append(f'{base_class} active')
        elif triggered_id == icon_id:
            new_class_names.append(f'{base_class} active')
        else:
            new_class_names.append(base_class)
            
    return new_class_names

@app.callback(
    Output('page-content', 'children'),
    [Input('tab-icon-1', 'n_clicks'),
     Input('tab-icon-2', 'n_clicks'),
     Input('tab-icon-3', 'n_clicks'),
     Input('tab-icon-4', 'n_clicks'),
     Input('tab-icon-5', 'n_clicks'),
     Input('tab-icon-6', 'n_clicks'),
     Input('tab-icon-7', 'n_clicks')]
)
def render_page_content(*args):
    ctx = dash.callback_context

    if not ctx.triggered_id:
        tab_id = '1'
    else:
        tab_id = ctx.triggered_id.replace('tab-icon-', '')

    if tab_id == '1':
        return html.Div([
            html.H1(
                children=[
                    html.Span("E", style={'color': 'var(--red)'}),
                    "xecutive ",
                    html.Span("O", style={'color': 'var(--red)'}),
                    "verview"
                ]
            )
        ])
    elif tab_id == '2':
        return html.Div([
            html.H1(
                children=[
                    html.Span("C", style={'color': 'var(--red)'}),
                    "ontent ",
                    html.Span("E", style={'color': 'var(--red)'}),
                    "xplorer"
                ]
            )
        ])
    elif tab_id == '3':
        return html.Div([
            html.H1(
                children=[
                    html.Span("T", style={'color': 'var(--red)'}),
                    "rend ",
                    html.Span("I", style={'color': 'var(--red)'}),
                    "ntelligence"
                ]
            )
        ])
    elif tab_id == '4':
        return html.Div([
            html.H1(
                children=[
                    html.Span("G", style={'color': 'var(--red)'}),
                    "eographic ",
                    html.Span("I", style={'color': 'var(--red)'}),
                    "nsights"
                ]
            )
        ])
    elif tab_id == '5':
        return html.Div([
            html.H1(
                children=[
                    html.Span("G", style={'color': 'var(--red)'}),
                    "enre and ",
                    html.Span("C", style={'color': 'var(--red)'}),
                    "ategory Intelligence"
                ]
            )
        ])
    elif tab_id == '6':
        return html.Div([
            html.H1(
                children=[
                    html.Span("C", style={'color': 'var(--red)'}),
                    "reator and ",
                    html.Span("T", style={'color': 'var(--red)'}),
                    "alent Hub"
                ]
            )
        ])
    elif tab_id == '7':
        return html.Div([
            html.H1(
                children=[
                    html.Span("S", style={'color': 'var(--red)'}),
                    "trategic ",
                    html.Span("R", style={'color': 'var(--red)'}),
                    "ecommendations"
                ]
            )
        ])
    return html.H2("Hello World")

@app.callback(
    Output('current-theme', 'data'),
    Output('theme-link', 'href'),
    Input('theme-switcher', 'n_clicks'),
    State('current-theme', 'data'),
    prevent_initial_call=True
)
def switch_theme(n_clicks, current_theme):
    if current_theme == 'dark':
        new_theme = 'light'
        new_css_href = '/assets/light.css'
    else:
        new_theme = 'dark'
        new_css_href = '/assets/dark.css'
        
    return new_theme, new_css_href


if __name__ == '__main__':
    app.run(debug=True)

server = app.server