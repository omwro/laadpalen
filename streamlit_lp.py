import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff



def main():
    st.title("Laadpaal Data")
    st.header("Importeren en opschonen van data")
    paalData = pd.read_csv('laadpaaldata.csv')
    paalData.head()
    st.code("paalData = pd.read_csv('laadpaaldata.csv')"
    "\npaalData.head()")
    fig = px.scatter(x=paalData['ChargeTime'],y=paalData['ConnectedTime'],labels={'x':'Laadtijd','y':'Aansluit tijd'})
    st.plotly_chart(fig)
    st.caption("Er is hier te zien dat er duidelijke outliers zijn in de laadtijd, deze worden gefilterd door middel van:")
    st.code("paalData = paalData[paalData['ChargeTime'] > 0]"
            "\npaalData = paalData[paalData['ChargeTime'] < 7]")

    st.caption("We houden nu het volgende DataFrame over:")
    st.dataframe(paalData)

    with st.echo():
        st.write("Laat de gemiddelden van de kolommen zien:")
        st.write(paalData.mean())






