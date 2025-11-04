from dash import html

layout = html.Div(
    children=[
        html.H1(
            children=[
                html.Span("G", style={'color': 'var(--red)'}),
                "eographic ",
                html.Span("I", style={'color': 'var(--red)'}),
                "nsights"
            ]
        ),
        html.P("This is the Executive Overview tab content.")
    ],
    className='geo-insights'
)