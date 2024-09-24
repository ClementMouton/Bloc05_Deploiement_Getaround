import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import io

### Config
st.set_page_config(
    page_title="GetAround",
    page_icon=":blue_car:",
    layout="wide"
)

## IMPORT DATASET
@st.cache_data
def load_data():
    data = pd.read_excel("get_around_delay_analysis.xlsx")
    data_file_delay = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
    data_file_pricing = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv'
    data_delay = pd.read_excel(data_file_delay)
    data_pricing = pd.read_csv(data_file_pricing)
    return data, data_delay, data_pricing

data_load_state = st.text('Loading data...')
data, df_delay, df_pricing = load_data()
data_load_state.text("")

# ----------------------------------

# Finding number of unique cars
number_of_cars = len(data['car_id'].unique())

# Finding number of rentals
number_of_rentals = data.shape[0]

# Add one feature that shows there is a delay or not
data['delay'] = data['delay_at_checkout_in_minutes'].apply(lambda x: 'Late' if x > 0 else 'On-time')

# Define a dataframe that shows for each car, the previous car had delay or not
data['previous_delay'] = 'None'
df = data[data['previous_ended_rental_id'].notnull()]
df = df.dropna(axis=0).reset_index(drop=True)

data2 = data[data['state'] == 'canceled']
df2 = data2[data2['previous_ended_rental_id'].notnull()]

y = []
delta = [*range(0, 750, 30)]
for x in delta:
    y.append(100 - 100 * len(df2[df2['time_delta_with_previous_rental_in_minutes'] > x]) / len(df2))

for i in range(len(df)):
    previous_id_index = data.index[data['rental_id'] == df.loc[i, 'previous_ended_rental_id']].tolist()
    df['previous_delay'].iloc[i] = data.loc[previous_id_index[0], 'delay']

# Removing NaN values about late checkout from the dataset
data_without_nan = data[data["delay_at_checkout_in_minutes"].notna()]
st.write(f"There are {data_without_nan.shape[0]} rentals in the dataset 'data_delay_without_nan'.")

# Main function for routing pages
def main():

    pages = {
        'A propos du projet': project,
        'Analyse exploratoire des données': analysis,
    }

    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            'page': 'Projet'
        })

    with st.sidebar:
        page = st.selectbox("Menu", tuple(pages.keys()))
    pages[page]()

def project():
    ### TITLE AND TEXT
    st.title("Tableau GetAround")
    st.write('\n')
    st.write('Fait par Clément Mouton')
    st.write('\n')
    st.title("Contexte:")
    "GetAround est l'Airbnb des voitures. Vous pouvez louer des voitures à n’importe qui pour quelques heures à quelques jours ! Fondée en 2009, cette entreprise a connu une croissance rapide. En 2019, ils comptent plus de 5 millions d'utilisateurs et environ 20 000 voitures disponibles dans le monde."
    "Nous avons donc un dataset de 16 346 entrées."

    st.write('\n')
    st.write('\n')

    st.title("Projet 🚧:")
    "Pour cette étude de cas, nous vous proposons de vous mettre à notre place et de réaliser une analyse que nous avons réalisée en 2017 🔮 🪄"
    "Lorsqu'ils utilisent Getaround, les conducteurs réservent des voitures pour une période spécifique, allant d'une heure à quelques jours. Ils sont censés ramener la voiture à temps, mais il arrive de temps en temps que les chauffeurs soient en retard au passage en caisse."
    "Les retours tardifs à la caisse peuvent générer de fortes frictions pour le conducteur suivant si la voiture était censée être louée à nouveau le même jour : le service client signale souvent des utilisateurs insatisfaits car ils ont dû attendre que la voiture revienne de la location précédente ou des utilisateurs qui ils ont même dû annuler leur location car la voiture n'était pas restituée à temps."

    st.title("Objectifs 🎯:")
    "Afin d'atténuer ces problèmes, nous avons décidé de mettre en place un délai minimum entre deux locations. Une voiture ne sera pas affichée dans les résultats de recherche si les heures d'arrivée ou de départ demandées sont trop proches d'une location déjà réservée."
    "Cela résout le problème des départs tardifs, mais peut également nuire aux revenus de Getaround et des propriétaires : nous devons trouver le bon compromis."

    st.write('\n')
    st.write('\n')

    st.subheader("Dataset")
    nrows_data = st.slider('Sélectionner le nombre de lignes à afficher', min_value=10, max_value=200)
    data_rows = data.head(nrows_data)
    st.dataframe(data_rows)

    st.write(f"Il y a {number_of_cars} différentes voitures dans le dataset.")
    
    st.subheader("Types de data et valeurs manquantes")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

def calculate_proportions(df, checkin_type=None):
    if checkin_type:
        df = df[df['checkin_type'] == checkin_type]
    f_retards = len(df[df['delay_at_checkout_in_minutes'] > 0])
    f_non_retards = len(df[df['delay_at_checkout_in_minutes'] <= 0])
    return [f_non_retards, f_retards]

def analysis():
    st.markdown("<h1 style='text-align: center;'>EDA et Data visualisation</h1>", unsafe_allow_html=True)

    def calculate_proportions2(df):
        thresholds_in_minutes = [0, 50, 100, 150, 200, 250, 300, 350, 400]
        mask = (df['delay_at_checkout_in_minutes'].notnull())
        mask_connect = (df['checkin_type'] == 'connect')
        mask_mobile = (df['checkin_type'] == 'mobile')
        proportions = pd.DataFrame({
            'thresholds': thresholds_in_minutes,
            'prop_retards': [df.loc[mask, 'delay_at_checkout_in_minutes'].
                            gt(threshold).mean() for threshold in thresholds_in_minutes],
            'prop_retards_connect': [df.loc[mask & mask_connect, 'delay_at_checkout_in_minutes'].
                                    gt(threshold).mean() for threshold in thresholds_in_minutes],
            'prop_retards_mobile': [df.loc[mask & mask_mobile, 'delay_at_checkout_in_minutes'].
                                gt(threshold).mean() for threshold in thresholds_in_minutes]
        })
        return proportions

    st.subheader('Comparaison des prix de location')
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Scatter Plot: Prix de location par rapport au kilométrage",
                                                        "Scatter Plot: Prix de location par rapport au kilométrage pour les moteurs de puissance 100"))

    # Première figure : scatter plot pour 'mileage' vs 'rental_price_per_day'
    fig1 = px.scatter(df_pricing, x='mileage', y='rental_price_per_day', trendline='ols')
    fig.add_trace(fig1.data[0], row=1, col=1)  # Ajouter le premier scatter plot
    fig.add_trace(fig1.data[1], row=1, col=1)  # Ajouter la ligne de tendance pour le premier plot

    # Deuxième figure : scatter plot pour un 'engine_power' spécifique
    power = 100
    fig2 = px.scatter(df_pricing[df_pricing['engine_power'] == power],
                      x='mileage',
                      y='rental_price_per_day',
                      trendline='ols',
                      title=f'Rental price par mileage pour un engine power de {power}')
    fig.add_trace(fig2.data[0], row=1, col=2)  # Ajouter le deuxième scatter plot
    fig.add_trace(fig2.data[1], row=1, col=2)  # Ajouter la ligne de tendance pour le deuxième plot

    # Mettre à jour la mise en page
    fig.update_layout(title_text="Comparaison des prix de location en fonction du mileage et de la puissance",
                      showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)

    # Analyse des Retards
    st.subheader('Analyse des Retards')
    
    # Création du scatter plot avec l'échelle y ajustée
    fig1 = px.scatter(df_delay,
                      x='time_delta_with_previous_rental_in_minutes',
                      y='delay_at_checkout_in_minutes',
                      color='checkin_type')

    # Diagramme à secteurs pour la proportion des retards
    total = len(df_delay)
    f_retards = len(df_delay[df_delay['delay_at_checkout_in_minutes'] > 0])
    f_non_retards = len(df_delay[df_delay['delay_at_checkout_in_minutes'] <= 0])
    
    df_delay_pie = pd.DataFrame({
        'Type': ['Retards', 'À l\'heure'],
        'Proportion': [f_retards / total, f_non_retards / total]
    })

    fig2 = px.pie(df_delay_pie, values='Proportion', names='Type')

    # Créer une figure avec des sous-graphiques
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=("Scatter Plot: Time Delta vs Retards", 
                                        "Proportion des Retards"),
                        specs=[[{'type': 'xy'}, {'type': 'domain'}]])

    # Ajouter les graphiques à la figure principale
    fig.add_trace(fig1.data[0], row=1, col=1)  # Ajouter le scatter plot
    for trace in fig1.data[1:]:
        fig.add_trace(trace, row=1, col=1)

    # Ajouter le pie chart dans la deuxième colonne
    fig.add_trace(fig2.data[0], row=1, col=2)

    # Ajuster manuellement l'échelle de l'axe y pour le scatter plot
    fig.update_yaxes(range=[-4000, 11000], row=1, col=1)

    # Mettre à jour la mise en page
    fig.update_layout(title_text="Analyse des Retards et Proportions selon la méthode de réservation",
                      showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

    # Graphique des proportions des retards
    st.subheader('Proportions des retards par type de checkin')

    import plotly.graph_objs as go

    def calculate_proportions(df, checkin_type=None):
        if checkin_type:
            df = df[df['checkin_type'] == checkin_type]
        f_retards = len(df[df['delay_at_checkout_in_minutes'] > 0])
        f_non_retards = len(df[df['delay_at_checkout_in_minutes'] <= 0])
        return [f_non_retards, f_retards]

    proportions_tout = calculate_proportions(df_delay)
    proportions_mobile = calculate_proportions(df_delay, 'mobile')
    proportions_connect = calculate_proportions(df_delay, 'connect')

    fig3 = go.Figure()
    fig3.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_tout, name="Mobile & Connect", sort=False))
    fig3.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_mobile, name="Mobile", visible=False, sort=False))
    fig3.add_trace(go.Pie(labels=['À l\'heure', 'Retards'], values=proportions_connect, name="Connect", visible=False, sort=False))

    # Mise à jour des tracés pour chaque bouton
    fig3.update_traces(hole=.4, hoverinfo="label+percent+name")

    # Ajout des boutons pour changer le diagramme
    fig3.update_layout(
        title_text="Proportion de retards",
        updatemenus=[{
            "buttons": [
                {
                    "label": "Mobile & Connect",
                    "method": "update",
                    "args": [{"visible": [True, False, False]}]
                },
                {
                    "label": "Mobile",
                    "method": "update",
                    "args": [{"visible": [False, True, False]}]
                },
                {
                    "label": "Connect",
                    "method": "update",
                    "args": [{"visible": [False, False, True]}]
                }
            ],
            "direction": "down",
            "showactive": True,
        }]
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader('Répartition des longueurs de retards par type de checkin')
    delay_by_checkin_type = px.box(df_delay, y='delay_at_checkout_in_minutes', color='checkin_type', range_y=[-25000, 72000])
    st.plotly_chart(delay_by_checkin_type, use_container_width=True)

    # Proportions de retards par seuil
    proportions_de_retards = calculate_proportions2(df_delay)
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=proportions_de_retards["thresholds"], y=proportions_de_retards["prop_retards"], name="Proportion de retards"))
    fig5.add_trace(go.Bar(x=proportions_de_retards["thresholds"], y=proportions_de_retards["prop_retards_mobile"], name="Proportion de retards (only mobile)"))
    fig5.add_trace(go.Bar(x=proportions_de_retards["thresholds"], y=proportions_de_retards["prop_retards_connect"], name="Proportion de retards (only connect)"))
    
    fig5.update_layout(title='Proportion de retards selon le mode de réservation vs global', xaxis_title='Seuil', yaxis_title='Proportion de retards', bargap=0.2)
    st.plotly_chart(fig5, use_container_width=True)

    st.write("- Quelle part du revenu du propriétaire est potentiellement affectée par la fonctionnalité ?")
    "Il est difficile de répondre à cette question avec les données actuelles. L'accès à des informations supplémentaires pourrait permettre une meilleure estimation des gains."
    st.write('\n')
    st.write("- Combien de locations sont concernées par la fonctionnalité selon le champ d'application et le seuil ?")
    "Le premier graphique indique que les retards sont moins importants dans le cadre du champ 'connect' par rapport au champ 'mobile'. Le quatrième graphique montre qu'en augmentant le seuil, le nombre de locations avec des retards diminue, ce qui pourrait affecter environ la moitié des locations."
    st.write('\n')
    st.write("- À quelle fréquence les conducteurs sont-ils en retard pour le prochain check-in ? Quel impact cela a-t-il sur le conducteur suivant ?")
    "Selon le deuxième graphique, 57,5 % des retards sont observés. Le troisième graphique révèle que, pour le type 'mobile', un nombre significatif de retards dépasse 720 minutes (12 heures), alors que seulement 13 retards sont enregistrés pour le type 'connect'. L'illustration montre que le retard impactera le client suivant si celui-ci dépasse le délai autorisé. Le premier graphique indique également que plus de locations sont affectées lorsque le délai est court (0 à 200 minutes), justifiant ainsi l'introduction d'un seuil."
    st.write('\n')
    st.write("- Combien de cas problématiques pourraient être résolus selon le seuil et le champ d'application choisis ?")
    "Les cas problématiques sont illustrés dans le schéma. Le quatrième graphique montre qu'en passant au type 'connect', le taux de retards pourrait passer de 61 % à 43 %. En appliquant un seuil de 100 minutes, le nombre de retards pourrait être divisé par trois ou quatre. À mesure que le nombre de retards diminue, le nombre de cas problématiques diminue également (en se référant toujours à l'illustration)."


if __name__ == "__main__":
    main()
