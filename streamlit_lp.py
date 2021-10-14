import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import fuzzywuzzy
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff



def main():
    st.title("Laadpaal Data")
    st.header("###Importeren en opschonen van data")
    paalData = pd.read_csv('laadpaaldata.csv')
    paalData.head()
    st.code("paalData = pd.read_csv('laadpaaldata.csv')"
    "\npaalData.head()")
    fig = px.scatter(x=paalData['ChargeTime'],y=paalData['ConnectedTime'])
    st.plotly_chart(fig)




