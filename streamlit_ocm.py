import streamlit as st
import numpy as np
import pandas as pd
import requests as req
from IPython.display import display
from fuzzywuzzy import fuzz
import plotly.express as px
import geopandas as gpd

def main():

    st.markdown("### Introductie")
    st.markdown("Voor het ophalen van de laadpalen data, hebben we gebruik gemaakt van de Open Charge Map "
                "API. De API kan je terug vinden op [OpenChargeMap](https://openchargemap.org/site/develop/api). "
                "Tijdens het ophalen hebben we opgemerkt dat we niet alle data terugkregen, dus hiervoor hebben "
                "gekozen om de maximum resultaat limiet op 100.000 te zetten om het analyse zo goed mogelijk "
                "uit te voeren.")
    # https://openchargemap.org/site/develop/api
    api_key = "bef339a4-319a-4a46-bbbe-a5f13db5bd24"
    ocm_url = f"https://api.openchargemap.io/v3/poi/?output=json&key=${api_key}&countrycode=NL&maxresults=100000"
    req_ocm = req.get(ocm_url)

    st.markdown("### Analyse")

    df_ocm_raw = pd.json_normalize(req_ocm.json())
    st.dataframe(df_ocm_raw.head())

    st.markdown("### Cleaning")
    df_ocm = df_ocm_raw.copy()
    df_ocm = df_ocm.replace('', np.nan)
    st.markdown("Nadat de request json was opgezet, hebben we gemerkt dat de kolom 'Connections' niet goed is "
                "genormaliseerd naar een dataframe en nog JSON data bevat. Daarom is er gekozen om een **nested "
                "dataframe** te maken waarbij de kolom 'Connections' een dataframe op zichzelf is")
    st.dataframe(df_ocm['Connections'].head())
    df_ocm['Connections'] = df_ocm.apply(lambda row: pd.json_normalize(row['Connections']), axis=1)
    st.markdown("\n```\ndf_ocm['Connections'] = df_ocm.apply(lambda row: pd.json_normalize(row['Connections']), axis=1)")
    st.dataframe(df_ocm['Connections'].head())

    st.markdown("### Plots")

