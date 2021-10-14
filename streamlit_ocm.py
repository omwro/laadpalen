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

    st.markdown("### Analyse")


    st.markdown("### Cleaning")


    st.markdown("### Plots")

