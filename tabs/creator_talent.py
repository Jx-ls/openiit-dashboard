from dash import html

layout = html.Div([
    html.H1(
        children=[
            html.Span("C", style={'color': 'var(--red)'}),
            "reator and ",
            html.Span("T", style={'color': 'var(--red)'}),
            "alent Hub"
        ]
    ),
    html.P("This is the Executive Overview tab content.")
])