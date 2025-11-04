from dash import html

layout = html.Div(
    children=[
        html.H1(
            children=[
                html.Span("C", style={'color': 'var(--red)'}),
                "ontent ",
                html.Span("E", style={'color': 'var(--red)'}),
                "xplorer"
            ]
        ),
        html.P("This is the content explorer tab content.")
    ],
    className='content'
)