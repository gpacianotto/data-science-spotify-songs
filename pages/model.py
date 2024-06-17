import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
from utils.modelCore import classify

dash.register_page(__name__)

genres = pd.read_csv("./genres.csv")

inputStyle = {
    "width": "100%",
    "border-radius": "20px",
    "font-size": "20px",
    "padding": "0px 5px"
}

buttonStyle = {
    "border-radius": "15px",
    "padding": "10px",
    "background-color": "#119dff",
    "color": "white",
    "font-size": "15px",
    "font-weight": "800",
    "border": "0px"
}


def generateRows(gen):
    rows = []
    for index, genre in enumerate(gen["track_genre"]):
        rows.append(
            html.Tr([
                html.Td(str(index + 1)),
                html.Td(genre)
            ])
        )
    
    return rows

def genreTable(gen):
    return html.Div([
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("índice"),
                    html.Th("Gênero")
                ]),
            ]),
            html.Tbody(
                generateRows(gen)
            )
        ])
    ])

def item_row(child):
    style = {"flex": 1, "padding": "0px 10px", "align-self": "center", "text-align": "left"}
    return html.Div([child], style=style)

def flex_row(child):
    style = {
        "flex-direction": "row",
        "display": "flex"
    }
    return html.Div(list(map(item_row, child)), style=style)

def extractIdFromURL(url:str):
    id = url.split("/")
    return id[-1], len(id)

def renderClassification(url):
    try:
        id, length = extractIdFromURL(url)
        if(length == 5 and id):
            classification = classify(id)

            print(classification)

            return html.Div([
                html.H2("Jukebox"),
                html.Div(id="jukebox"),
                html.Iframe(
                    id="myIframe",
                    src="https://open.spotify.com/embed/track/"+id+"?theme=0",
                    width="100%",
                    height="152px",
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
                    style={"border-radius": "12px", "border": "0px"}
                ),
                html.H3("Predição"),
                html.P("Esta predição aponta para:" + classification["predicted_genre"].values[0]),
                renderRowFeatures(classification)
            ])

        return html.P("link inválido!")
    except Exception as e:
        
        print(f"An error occurred: {e}")

        return html.Div([
            html.P("oops alguma coisa deu errado!")
        ])

def renderRowFeatures(classification):
    genresInner = genres["track_genre"].unique()

    classificationValues = classification[genresInner].values

    print("renderingRowFeatures")

    print(genresInner)

    print(classificationValues)

    rows = []

    for i in range(0, len(genresInner), 4):
        if(i != 112):
            rows.append(
                flex_row([
                    html.Div([
                        html.H4(genresInner[i]),
                        html.P(round(classificationValues[0][i], 5))
                    ]),
                    html.Div([
                        html.H4(genresInner[i + 1]),
                        html.P(round(classificationValues[0][i + 1], 5))
                    ]),
                    html.Div([
                        html.H4(genresInner[i + 2]),
                        html.P(round(classificationValues[0][i + 2], 5))
                    ]),
                    html.Div([
                        html.H4(genresInner[i + 3]),
                        html.P(round(classificationValues[0][i + 3], 5))
                    ]),
                ])
            )
        if (i == 112):
            rows.append(
                flex_row([
                    html.Div([
                        html.H4(genresInner[i]),
                        html.P(classificationValues[0][i])
                    ]),
                    html.Div([
                        html.H4(genresInner[i + 1]),
                        html.P(classificationValues[0][i + 1])
                    ])
                ])
            )
    return html.Div(rows)

layout = html.Div([
    html.H1("Modelo de Classificação"),
    html.P("Este modelo foi construido para que a partir de um link de uma música do Spotify o usuário consiga classificar a música entre os gêneros presentes nos dados de treinamento deste modelo."),
    html.H2("Gêneros de Treinamento (classes)"),
    html.P("Os gêneros de música utilizados no treinamento deste modelo foram:"),
    genreTable(gen=genres),
    html.H2("Classificação"),
    html.P("Insira abaixo o link da música que você deseja que o modelo classifique:"),
    flex_row([
        dcc.Input(id="song-url", style=inputStyle),
        html.Button("Classificar", id="classify-button", style=buttonStyle)
    ]),
    html.Div([],id="classification-container"),
    
    
    
])

@callback(
    Output('classification-container', 'children'),
    Input('classify-button', 'n_clicks'),
    Input('song-url', 'value'),
    prevent_initial_call=True,
    running=[(Output("classify-button", "disabled"), True, False)]
)
def update_button(show, url):
    if(show and (int(show) % 2 != 0)):
        return renderClassification(url)

    return html.Div([])