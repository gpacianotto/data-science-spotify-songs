from dash import Dash, html, dcc, callback, Output, Input, page_container, page_registry

app = Dash(__name__, use_pages=True)

documentStyle = {
    "font-family": "Helvetica",
}

topBarStyle = {
    'display': 'flex',
    'flex-direction': "row",
    "border-bottom": "2px solid black",
    "margin-bottom": "15px"

}
itemStyle = {
    "flex": 1,
    "text-align": "center",
    "border-left": "1px solid white",
    "padding": "20px 0px",
    "font-weight": "800",
    "background-color": "black"
}

linkStyle = {
    "color": "white",
}

app.layout = html.Div([
    html.Div([
        html.Div([
                dcc.Link(f"Info", href="/info", style=linkStyle)
            ],
            style=itemStyle
        ),
        html.Div([
                dcc.Link(f"AED", href="/aed", style=linkStyle),
            ],
            style=itemStyle
        ),
        html.Div([
                dcc.Link(f"Relatório", href="/relatorio", style=linkStyle)
            ],
            style=itemStyle
        ),
        
    ], style=topBarStyle),
    page_container
], style=documentStyle)


if __name__ == '__main__':
    app.run(debug=True)