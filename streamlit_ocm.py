import streamlit as st
import numpy as np
import pandas as pd
import requests as req
from fuzzywuzzy import fuzz
import plotly.express as px
import geopandas as gpd
import matplotlib as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.markdown("### Introductie")
    st.markdown("Voor het ophalen van de laadpalen data, hebben we gebruik gemaakt van de Open Charge Map "
                "API. De API kan je terug vinden op [OpenChargeMap](https://openchargemap.org/site/develop/api). "
                "Tijdens het ophalen hebben we opgemerkt dat we niet alle data terugkregen, dus hiervoor hebben "
                "gekozen om de maximum resultaat limiet op 100.000 te zetten om het analyse zo goed mogelijk "
                "uit te voeren. Maar dit kon helaas Streamlit niet aan waardoor we het limiet moesten verlagen naar "
                "1.000 regels. De tekstuele analyses zijn nog van de analyse met de limiet van 100.000 regels.")
    # https://openchargemap.org/site/develop/api
    api_key = "bef339a4-319a-4a46-bbbe-a5f13db5bd24"
    ocm_url = f"https://api.openchargemap.io/v3/poi/?output=json&key=${api_key}&countrycode=NL&maxresults=1000"
    req_ocm = req.get(ocm_url)

    st.markdown("Daarnaast hebben we ook een extra dataset gebruikt om alle correcte benamingen van provincies en "
                "gemeenten op te halen zodat we later de data kunnen corrigeren. de data halen we op van "
                "[Geoportaaloverijssel](https://download.geoportaaloverijssel.nl/download/vector/6be88637-f10f-44a4-aa5c-fc8c0f857620).")
    # https://download.geoportaaloverijssel.nl/download/vector/6be88637-f10f-44a4-aa5c-fc8c0f857620
    df_gp = pd.read_csv('Grenzen_van_alle_Nederlandse_gemeenten_en_provincies.csv')
    df_gp = df_gp[['SHAPE', 'PROVINCIENAAM', 'GEMEENTENAAM']]

    st.markdown("### Analyse")
    st.markdown("#### Open Charge Map")
    df_ocm_raw = pd.json_normalize(req_ocm.json())
    st.dataframe(df_ocm_raw)
    df_ocm = df_ocm_raw.copy()
    st.markdown("Tijdens het analyseren van de data, zijn we achter gekomen dat we veel data missen in de dataset. De "
                "dataset heeft **7785** regels aan data. "
                "\n\nVan de **7785** regels de Provincie kolom, zijn maar **296** waarden ingevuld en de overige "
                "**7487** waarden ontbreekt. "
                "\n\nVan de **7785** regels de Gemeente kolom, zijn maar **7766** waarden ingevuld en de overige "
                "**17** waarden ontbreekt.")

    st.markdown("#### Geoportaaloverijssel")
    st.dataframe(df_gp)

    st.markdown("### Cleaning")
    st.markdown("#### Lege string waarden vervangen")
    st.markdown("Wat ons als eerst opviel is dat we veel data missen en in meerdere types, zoals `None`, `NaN` en `''`. "
                "Binnen python zijn `None` en `NaN` makkelijk te herkennen maar lege string niet, dus we hebben ervoor "
                "gekozen om alle lege strings te vervangen met `NaN`.")
    st.code("df_ocm = df_ocm.replace('', np.nan)")
    df_ocm = df_ocm.replace('', np.nan)

    st.markdown("#### Connections kolom overzetten naar een dataframe")
    st.markdown("Vervolgens hebben we gemerkt dat de kolom 'Connections' niet goed is "
                "genormaliseerd naar een dataframe en nog JSON data bevat. Daarom is er gekozen om een **nested "
                "dataframe** te maken waarbij de kolom 'Connections' een dataframe op zichzelf is")
    st.dataframe(df_ocm['Connections'])
    df_ocm['Connections'] = df_ocm.apply(lambda row: pd.json_normalize(row['Connections']), axis=1)
    st.code("df_ocm['Connections'] = df_ocm.apply(lambda row: pd.json_normalize(row['Connections']), axis=1)")
    st.dataframe(df_ocm['Connections'])

    st.markdown("#### Provincie en gemeente namen corrigeren")
    st.markdown("Zoals we hebben gezien in de analyse, ontbreken er veel data en zijn ook verkeerd gespeld. Hiervoor "
                "hebben we gekozen om de __Geoportaaloverijssel__ dataset te gebruiken voor de correcte benamingen en "
                "de __FuzzyWuzzy__ bibliotheek om in te schatten of de gebruiker hetzelfde locatie bedoelde. Een "
                "voorbeeld van hoe we dit voor elkaar hebben gekregen ziet er ongeveer zo uit:")
    st.code("def get_cleaned_province_and_town(row):"
            "\n\tif row['AddressInfo.Town'] is None: return row"
            "\n\tif row['AddressInfo.Town'] is np.nan: return row"
            "\n\n\thighest_score_gp = None"
            "\n\tfor i, gp in df_gp.iterrows():"
            "\n\t\tratio_town = fuzz.WRatio(gp['GEMEENTENAAM'], row['AddressInfo.Town'])"
            "\n\t\tif ratio_town > highest_score_town:"
            "\n\t\t\thighest_score_town = ratio_town"
            "\n\t\thighest_score_gp = gp"
            "\n\n\tif highest_score_town >= 90:"
            "\n\t\trow['cleaned.town'] = highest_score_gp['GEMEENTENAAM']"
            "\n\t\trow['cleaned.province'] = highest_score_gp['PROVINCIENAAM']"
            "\n\treturn row")

    df_ocm['cleaned.town'] = np.nan
    df_ocm['cleaned.province'] = np.nan

    def get_cleaned_province_and_town(row):
        if row['AddressInfo.Town'] is None: return row
        if row['AddressInfo.Town'] is np.nan: return row

        highest_score_town = 0
        highest_score_gp = None
        for i, gp in df_gp.iterrows():
            ratio_town = fuzz.WRatio(gp['GEMEENTENAAM'], row['AddressInfo.Town'])
            if ratio_town > highest_score_town:
                highest_score_town = ratio_town
                highest_score_gp = gp

        if highest_score_town >= 90:
            row['cleaned.town'] = highest_score_gp['GEMEENTENAAM']
            row['cleaned.province'] = highest_score_gp['PROVINCIENAAM']
        return row

    def get_extra_cleaned_province(row):
        if type(row['AddressInfo.StateOrProvince']) == str and type(row['cleaned.province']) == float:
            highest_score_province = 0
            highest_score_province_name = None
            for pro in df_gp['PROVINCIENAAM'].unique():
                ratio_province = fuzz.WRatio(pro, row['AddressInfo.StateOrProvince'])
                if ratio_province > highest_score_province:
                    highest_score_province = ratio_province
                    highest_score_province_name = pro
            if highest_score_province >= 70:
                row['cleaned.province'] = highest_score_province_name
        return row

    df_ocm = df_ocm.apply(lambda row: get_cleaned_province_and_town(row), axis=1)
    df_ocm = df_ocm.apply(lambda row: get_extra_cleaned_province(row), axis=1)

    st.markdown("Nadat we de Gemeente waarden hebben gecorrigeerd, zien we dat **504** waarden verkeerd zijn ingevuld. "
                "De hoofdreden voor deze verkeerde waarden is dat ze stedennamen of dorpsnamen hebben ingevuld die "
                "niet gelijkstaan aan de gemeentenaam. Ook zijn de Provincie kolom aangevuld met de correcte Gemeente "
                "waarden."
                "\n\nTot slot hebben we de Provincie kolom extra gecontroleerd op mogelijke vermiste waarden en "
                "hiermee hebben we maar **444** vermiste waarden in Provincie.")

    labels = ['Ingevuld', 'Niet ingevuld']
    fig1 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig1.add_trace(go.Pie(labels=labels,
                         values=[
                             df_ocm['AddressInfo.StateOrProvince'].notna().sum(),
                             df_ocm['AddressInfo.StateOrProvince'].isna().sum()]
                         ), 1, 1)
    fig1.add_trace(go.Pie(labels=labels,
                         values=[
                             df_ocm['AddressInfo.Town'].notna().sum(),
                             df_ocm['AddressInfo.Town'].isna().sum()]
                         ), 1, 2)
    fig1.update_traces(hole=.6, hoverinfo="percent+value")
    fig1.update_layout(
        title_text="Ratio tussen complete en incomplete data voor de Cleaning",
        annotations=[dict(text='Provincie', x=0.15, y=0.5, font_size=16, showarrow=False),
                     dict(text='Gemeente', x=0.87, y=0.5, font_size=16, showarrow=False)])
    st.plotly_chart(fig1)

    fig2 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig2.add_trace(go.Pie(labels=labels,
                         values=[
                             df_ocm['cleaned.province'].notna().sum(),
                             df_ocm['cleaned.province'].isna().sum()]
                         ), 1, 1)
    fig2.add_trace(go.Pie(labels=labels,
                         values=[
                             df_ocm['cleaned.town'].notna().sum(),
                             df_ocm['cleaned.town'].isna().sum()]
                         ), 1, 2)
    fig2.update_traces(hole=.6, hoverinfo="percent+value")
    fig2.update_layout(
        title_text="Ratio tussen complete en incomplete data na de Cleaning",
        annotations=[dict(text='Provincie', x=0.15, y=0.5, font_size=16, showarrow=False),
                     dict(text='Gemeente', x=0.87, y=0.5, font_size=16, showarrow=False)])
    st.plotly_chart(fig2)


    st.markdown("### Type laadpalen")
    types = []
    for con in df_ocm['Connections']:
        if 'CurrentType.Title' in con.columns:
            for title in con['CurrentType.Title']:
                types.append(title)
        else:
            types.append(np.nan)

    unique, counts = np.unique(types, return_counts=True)

    df_types = pd.DataFrame()
    df_types['type'] = unique
    df_types['count'] = counts
    fig = px.pie(df_types,
                 values='count',
                 names='type',
                 title="Type laadpalen in nederland")
    st.plotly_chart(fig)

    st.markdown("### Tarieven")
    st.markdown("Zijn tarieven transparant?"
                "- De meeste laadpalen zijn vaag met de specifieke tarieven"
                "- De specificeerde tarieven zijn inconsistent met de andere laadpalen")
    st.dataframe(df_ocm['UsageCost'].value_counts())

    st.markdown("### Kaart")
    st.markdown("### Alle laadpunten")
    fig = px.scatter_mapbox(
        df_ocm,
        lon='AddressInfo.Longitude',
        lat='AddressInfo.Latitude',
        hover_name="AddressInfo.Title",
        zoom=7
    )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)

    st.markdown("### Aantal laadpunten per gemeente")
    df_ocm_no_points = df_ocm.groupby('AddressInfo.Town')['NumberOfPoints'].sum()
    st.dataframe(df_ocm_no_points)

    df_gp['NumberOfPoints'] = 0
    for i in df_ocm_no_points.index:
        v = df_ocm_no_points.loc[i]
        index_found = df_gp[df_gp['GEMEENTENAAM'] == i].index
        df_gp.loc[index_found, 'NumberOfPoints'] = v
    df_gp['geometry'] = gpd.GeoSeries.from_wkt(df_gp['SHAPE'])
    gdf_gp = gpd.GeoDataFrame(df_gp, geometry='geometry')
    gdf_gp.plot(column='NumberOfPoints',
                legend=True,
                cmap='Blues',
                edgecolor='black')
    st.pyplot()


