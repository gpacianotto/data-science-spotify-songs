import dash
from dash import html, dcc, callback, Input, Output, get_asset_url

dash.register_page(__name__)

imageStyle = {
    "text-align": "center"
}

layout = html.Div([
    html.H2(children="O que foi descoberto?"),
    html.P(["Nesta seção será discutido as descobertas após uma análise exploratória dos dados do dataset."]),
    html.Hr(),
    html.H3("Diferenciação por gênero"),
    html.P("Com uma breve análise dos dados, é possível concluir que há a possibilidade de diferenciação de gêneros musicais  com base nas características musicais de cada música. Isso porque muitos dos gêneros de música analizados possuem peculiaridades em certas características que podem ser cruciais para sua identificação. A clusterização parcial também ajudou a demonstrar isso"),
    html.H3("Anomalias"),
    html.P("Conforme a análise exploratória foi sendo feita, foram encontradas algumas anomalias nos dados, em destaque, quando se diz respeito aos gêneros musicais. Em certos gêneros, utilizando a jukebox, foi verificado exemplares não condizentes com o gênero musical. Por exemplo, ao selecionar o gênero 'pagode' pode-se verificar algumas músicas da artista Anitta que não possuem relação com o gênero."),
    html.Div([
        html.Img(src=get_asset_url('anomalia.png'), style={"width": "80%"}),
    ], style=imageStyle),
    html.P("A causa desta anomalia reside na metodologia utilizada na coleta dos dados mencionada na aba Info. O problema, especificamente, encontra-se no item 2 da sua metodologia, pois não há nada que garanta que, em uma busca com a palavra-chave do gênero, o gênero será contemplado por 1000 músicas."),
])