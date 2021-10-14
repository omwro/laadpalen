import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import fuzzywuzzy
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff



def main():
    st.title("Laadpaal Data")
    st.header("###Importeren en opschonen van data")
    paalData = pd.read_csv('laadpaaldata.csv')
    paalData.head()
    st.code("paalData = pd.read_csv('laadpaaldata.csv')
    "\npaalData.head()")
    plt.figure()
    sns.scatterplot(x='ChargeTime', y='ConnectedTime', data=paalData)
    st.plotly_chart(fig)




