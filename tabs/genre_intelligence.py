from dash import html

layout = html.Div(
    children=[
        html.H1(
            children=[
                html.Span("G", style={'color': 'var(--red)'}),
                "enre and ",
                html.Span("C", style={'color': 'var(--red)'}),
                "ategory Intelligence"
            ]
        ),
        html.P("This is the Executive Overview tab content.")
    ],
    className='genre-int'
)