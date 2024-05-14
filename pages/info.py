import dash
from dash import html, dcc, callback, Input, Output, get_asset_url
import plotly.express as px
import pandas as pd
import numpy as np

dash.register_page(__name__)

cellStyle = {
    "border": "1px solid black",
    "padding": "10px"
}

tableStyle = {
    "width": "100%",
    "border": "1px solid black"
}

imageStyle = {
    "text-align": "center"
}


layout = html.Div([
    html.H2(children="Informações sobre o Dataset"),
    html.P([
        "Este ", 
        html.I(["dataset"]), 
        " é um conjunto de dados de músicas coletados na plataforma ",
        html.I(["Spotify. "]),
        "Nele, temos 114 gêneros de música, com 1000 músicas cada. Você pode acessar o dataset ",
        html.A("aqui.", href="https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset?rvi=1", target="blank")
    ]),
    html.Hr(),
    html.H2("Colunas"),
    html.P(["As colunas deste ", html.I("dataset"), " são:"]),
    html.Table([
        html.Thead([
            html.Tr([
                html.Th("Index", style=cellStyle),
                html.Th("Coluna", style=cellStyle),
                html.Th("Descrição", style=cellStyle),
            ]),
        ]),
        html.Tr([
            html.Td("1", style=cellStyle),
            html.Td("track_id", style=cellStyle),
            html.Td("Identificador da música.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("2", style=cellStyle),
            html.Td("artists", style=cellStyle),
            html.Td("Artistas proprietários da música.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("3", style=cellStyle),
            html.Td("album_name", style=cellStyle),
            html.Td("Nome do àlbum da música.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("4", style=cellStyle),
            html.Td("track_name", style=cellStyle),
            html.Td("Título da música.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("5", style=cellStyle),
            html.Td("popularity", style=cellStyle),
            html.Td("Valor que varia de 0 a 100 que indica a popularidade da música. Quando mais próximo de 100, mais popular.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("6", style=cellStyle),
            html.Td("duration_ms", style=cellStyle),
            html.Td("Duração da música em milissegundos.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("7", style=cellStyle),
            html.Td("explicit", style=cellStyle),
            html.Td("True se a música possui linguagem explícita, False em caso contrário.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("8", style=cellStyle),
            html.Td("danceability", style=cellStyle),
            html.Td("Chamaremos esse dado de 'dançabilidade'. Ele indica o quanto a musica é adequada para danças baseado na combinação de alguns elementos musicais como andamento, estabilidade de ritmo, força das batidas e regularidade musical como um todo. O valor 0 (zero) corresponte a uma canção nada 'dançável' e 1 uma canção 'dançável' ao máximo.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("9", style=cellStyle),
            html.Td("energy", style=cellStyle),
            html.Td("Chamaremos esse dado de 'energia'. Ele indica uma medida entre 0 e 1 que representa a intensidade e atividade de uma música. Geralmente, músicas mais enérgicas possui maior dinâmica, volume e timbres com mais destaque. ", style=cellStyle),
        ]),
        html.Tr([
            html.Td("10", style=cellStyle),
            html.Td("key", style=cellStyle),
            html.Td("Tom da música. Medido em uma escala de cifras, onde Dó = 0, Dó sustenido = 1, Ré = 2, e assim por diante... até Si = 11.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("11", style=cellStyle),
            html.Td("loudness", style=cellStyle),
            html.Td("Volume médio da mixagem da música em decibeis. Varia de -60 a 0", style=cellStyle),
        ]),
        html.Tr([
            html.Td("12", style=cellStyle),
            html.Td("mode", style=cellStyle),
            html.Td("Indica se a música encontra-se numa escala maior ou menor de notas musicais. (maior = 1, menor = 0).", style=cellStyle),
        ]),
        html.Tr([
            html.Td("13", style=cellStyle),
            html.Td("speechiness", style=cellStyle),
            html.Td("Esse índice indica a detecção de palavras pronunciadas na música. Esse valor, quanto mais próximo de 1 maiores são os trechos que contém palavras pronunciadas, e quanto mais próximo de 0 menores são os trechos com palavras pronunciadas", style=cellStyle),
        ]),
        html.Tr([
            html.Td("14", style=cellStyle),
            html.Td("acousticness", style=cellStyle),
            html.Td("Representa a chance de uma música ser acústica. Quanto mais próximo de 1, maiores as chances de ser uma música acústica. Quanto mais próximo de 0, menor a chance de ser uma música acústica.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("15", style=cellStyle),
            html.Td("instrumentalness", style=cellStyle),
            html.Td("Indica se uma música contém ou não vocais humanos com letra. Vocalizações como 'Ooh', 'Aah' são consideradas como percussão ou elemento instrumental. Valores entre 0 (musicas com letra) e 1 (musicas instrumentais).", style=cellStyle),
        ]),
        html.Tr([
            html.Td("16", style=cellStyle),
            html.Td("liveness", style=cellStyle),
            html.Td("Valor entre 0 e 1 que indica se uma música é uma versão ao vivo ou não. Quanto mais próximo de 1, maior a chance dela ser ao vivo.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("17", style=cellStyle),
            html.Td("valence", style=cellStyle),
            html.Td("Valor entre 0 e 1 que indica a positividade da música, valores próximos a 0 geralmente indicam músicas tristes, melancólicas, ou que expressam raiva ou revolta. Valores próximos a 1 são músicas mais positivas, felizes que indicam alegria ou euforia.", style=cellStyle),
        ]),
        html.Tr([
            html.Td("18", style=cellStyle),
            html.Td("tempo", style=cellStyle),
            html.Td("Andamento da música medido em BPM (batidas por minuto)", style=cellStyle),
        ]),
        html.Tr([
            html.Td("19", style=cellStyle),
            html.Td("time_signature", style=cellStyle),
            html.Td("Valor entre 3 e 7 que indica quantas batidas tem por compasso (teoria musical).", style=cellStyle),
        ]),
        html.Tr([
            html.Td("20", style=cellStyle),
            html.Td("track_genre", style=cellStyle),
            html.Td("Gênero da música.", style=cellStyle),
        ]),
    ], style=tableStyle),
    html.Hr(),
    html.H2("Metodologia"),
    html.P([
        "Este dataset foi coletado diretamente da API disponibilizada pelo Spotify, segundo o proprietário deste dataset. Na página deste dataset no Kaggle, especificamente na aba 'discussion' há uma pergunta interessante que deve ser mencionada aqui na metodologia. O usuário pergunta: "
    ]),
    html.Div([
        html.Img(src=get_asset_url('comment.png')),
    ], style=imageStyle),
    
    html.P([
        "Em seguida, o dono do dataset responde: "
    ]),
    html.Div([
        html.Img(src=get_asset_url('answer.png')),
    ], style=imageStyle),
    html.P([
        "Em suma, o dono do dataset fez o seguinte processo:  "
    ]),
    html.Ol([
        html.Li([
            "Obteve os gêneros de música ", html.A("neste", href="https://developer.spotify.com/documentation/web-api/reference/get-recommendation-genres", target="blank"), " endpoint."
        ]),
        html.Li([
            "Recuperou músicas, gênero a gênero, ", html.A("neste", href="https://developer.spotify.com/documentation/web-api/reference/search", target="blank"), " endpoint. Separando as 1000 primeiras da busca."
        ]),
        html.Li("Compilou tudo em um arquivo csv.")
    ]),
    html.Hr(),
])