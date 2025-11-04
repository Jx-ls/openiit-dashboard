from dash import html

layout = html.Div(
    children=[
        html.H1(
            children=[
                html.Span("T", style={'color': 'var(--red)'}),
                "rend ",
                html.Span("I", style={'color': 'var(--red)'}),
                "ntelligence"
            ]
        ),
        html.P("This is the Executive Overview tab content.")
    ],
    className='trend'
)