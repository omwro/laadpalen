import streamlit as st
import numpy as np
import pandas as pd
import requests as req
from IPython.display import display
from fuzzywuzzy import fuzz
import plotly.express as px
import geopandas as gpd

def main():
    st.markdown("Dit is Open Charge Map")