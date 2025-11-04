from dash import html

layout = html.Div([
    html.H1(
        children=[
            html.Span("E", style={'color': 'var(--red)'}),
            "xecutive ",
            html.Span("O", style={'color': 'var(--red)'}),
            "verview"
        ]
    ),
    html.P("This is the Executive Overview tab content.")
])
