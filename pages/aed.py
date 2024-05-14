import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

dash.register_page(__name__)

df = pd.read_csv("./dataset.csv")
df_genres = pd.read_csv("./genres.csv")

dropdownStyle = {"margin-bottom": "10px"}

buttonStyle = {
    "border-radius": "15px",
    "padding": "10px",
    "background-color": "#119dff",
    "color": "white",
    "font-size": "15px",
    "font-weight": "800",
    "border": "0px"
}

audioData = np.array([
    "popularity", 
    "danceability", 
    "loudness", 
    "acousticness", 
    "valence",
    "duration_ms",
    "energy",
    "key",
    "speechiness",
    "instrumentalness",
    "tempo",
    "time_signature",
    "mode"
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

sectionStyle = {
    "border": "1px solid black",
    "padding": "10px",
    "margin-bottom": "20px"
}


layout = html.Div([

    html.Div([
        # SEÇÃO DE GÊNERO
        flex_row([
            html.Div([
                html.H2("Dados por gênero musical", style={"text-align": "left"}),
            ]),
            html.Div([
                dcc.Dropdown(df.track_genre.unique(), 'acoustic', id="dropdown-selection-track-genre", style=dropdownStyle),
            ])
        ]),
        html.P("Escolha um gênero de música e veja a análise exploratória feita neste bloco"),
        html.Hr(),
        # JUKEBOX
        html.H3("Jukebox"),
        html.P("Selecione e escute qualquer música da amostra do gênero escolhido"),
        html.Div([dcc.Dropdown(id="jukebox-dropdown")],id="dropdown-jukebox", style={"margin-bottom": "10px"}),

        html.Div(id="jukebox"),

        html.Hr(),

        # GRÁFICO DE BARRAS 1
        html.H3("Features Isoladas"),
        flex_row([
            html.Div([
                html.Label("Escolha a característica musical"),
                    dcc.Dropdown(
                        audioData, 
                        'popularity', 
                        id="dropdown-selection-track-feature", 
                        style=dropdownStyle
                    ),
            ]),
            html.Div([
                html.Button("Mostrar Resultado", id="show-1", style=buttonStyle),
            ], style={"text-align": "right"}),
            
        ]),
        html.Div(id='graph-content'),
        
        html.Hr(),

        # BOX PLOT FEATURES
        html.H3("Features do Gênero"),
        html.Div(id="box-plot-features"),
    ], style=sectionStyle),
    

    # SEÇÃO GERAL 
    html.Div([
        # BOX PLOT GERAL
        html.H2("Dados Gerais"),
        html.P("Nesta seção estarão apresentados alguns gráficos sem o recorte de gênero musical."),
        html.Hr(),
        html.H3("Explorando o comportamento de cada gênero musical"),
        flex_row([
            html.Div([
                html.Label("Escolha a característica musical"),
                dcc.Dropdown(
                    audioData, 
                    'popularity', 
                    id="dropdown-selection-track-feature-2", 
                    style=dropdownStyle
                ),
            ]),
            html.Button("Mostrar Resultado", id="show-2", style=buttonStyle),
        ]),
        html.Div(id='graph-box-plot'),
        html.Hr(),
        # CLUSTERIZAÇÃO PARCIAL
        html.H3("Clusterização Parcial"),
        html.P("Escolha alguns gêneros musicais para realizar uma clusterização."),
        dcc.Checklist(options=df_genres["track_genre"], inline=True, id="checklist-track-genre"),
        html.Div(id="partial-clustering")
    ], style=sectionStyle),
    
])

# CLUSTERIZAÇÃO PARCIAL
@callback(
    Output("partial-clustering", "children"),
    Input("checklist-track-genre", "value")
)
def update_cluster(value):

    if(value and len(value) > 0):

        filtered = df[df["track_genre"].isin(value)]

        df_selected = filtered[['popularity', 'danceability', 'loudness', 'acousticness', 'valence', 
                    'duration_ms', 'energy', 'key', 'speechiness', 'instrumentalness', 
                    'tempo', 'time_signature', 'mode']]

        scaler = StandardScaler()
        df_normalized = scaler.fit_transform(df_selected)

        # Aplicando PCA
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(df_normalized)

        df_pca = pd.DataFrame(df_pca, columns=['PC1', 'PC2'])

        df_final = df_pca

        kmeans = KMeans(n_clusters=len(value), random_state=42)
        clusters = kmeans.fit_predict(df_pca)

        # Adicionando os clusters ao dataframe final
        df_final['cluster'] = clusters

        return dcc.Graph(figure=px.scatter(x=df_final["PC1"], y=df_final["PC2"], color=df_final["cluster"], opacity=0.5, hover_name=filtered['track_genre']))

    return html.Div(value)

# BOX PLOT FEATURES
@callback(
    Output("box-plot-features", 'children'),
    Input('dropdown-selection-track-genre', 'value'),
)
def update_boxplot_features(genre):
    if(genre):

        return dcc.Graph(figure=px.box(data_frame=df[df["track_genre"] == genre], y=["acousticness", "valence","danceability", "energy", "speechiness", "instrumentalness"], height=800))
    return html.Div()

# JUKEBOX - Callback de Gênero
@callback(
    Output('dropdown-jukebox', 'children'),
    Input('dropdown-selection-track-genre', 'value'),
)
def update_jukebox_dropdown(genre):

    filtered_df = df.query('track_genre == @genre')

    #result_array = filtered_df.apply(lambda row: f"{row['artists']} - {row['track_name']}", axis=1).tolist()

    result_array = filtered_df.apply(lambda row: f"{row['track_id']}", axis=1).tolist()

    #result_map = {row['track_id']: string for row, string in zip(filtered_df.itertuples(index=False), result_array)}

    

    return dcc.Dropdown(options=result_array, id="jukebox-dropdown")

# JUKEBOX - Callback do Iframe
@callback(
    Output("jukebox", "children"),
    Input("jukebox-dropdown", "value")
)
def update_iframe(track_id):

    if(track_id):
        return html.Iframe(
            id="myIframe",
            src="https://open.spotify.com/embed/track/"+track_id+"?theme=0",
            width="100%",
            height="152px",
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
            style={"border-radius": "12px", "border": "0px"}
        )
    return html.Div()

# BOX PLOT GERAL
@callback(
    Output('graph-box-plot', 'children'),
    Input('dropdown-selection-track-feature-2', 'value'),
    Input('show-2', 'n_clicks')
)
def update_boxplot(feature, show):
    if(show and int(show) % 2 != 0):
        return dcc.Graph(figure=px.box(data_frame=df, points=False, x=feature, y="track_genre", height=10000))
    
    return html.P("")


# GRÁFICO DE BARRAS 1
@callback(
    Output('graph-content', 'children'),
    Input('dropdown-selection-track-genre', 'value'),
    Input('dropdown-selection-track-feature', 'value'),
    Input('show-1', 'n_clicks')
)
def update_graph(genre, feature, show):
    if(show and int(show) % 2 != 0):

        return dcc.Graph(figure=px.histogram(
            data_frame=df.query('track_genre=="' + genre + '"'), 
            title="'"+feature+"' nas músicas do estilo '"+genre+"'",
            labels={"count": "Quantidade de Músicas"},
            x=feature, 
            nbins=100
        ), id='graph-1')

    return html.P("")

# BOTÃO MOSTRAR GRÁFICO
@callback(
    Output('show-1', 'children'),
    Input('show-1', 'n_clicks'),
)
def update_button(show):
    if(show and int(show) % 2 != 0):
        return "Esconder Gráfico"

    return "Mostrar gráfico"