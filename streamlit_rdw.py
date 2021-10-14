import streamlit as st
import numpy as np
import pandas as pd
import requests as req
from IPython.display import display
from datetime import datetime
import plotly.express as px

def main():
    st.markdown("Dit is RDW Data voor het ophalen van de RDW data hebben gebruik gemaakt van verschillende datasets"
                "\nhttps://opendata.rdw.nl/resource/m9d7-ebf2.json" "https://opendata.rdw.nl/resource/8ys7-d773.json" "https://opendata.rdw.nl/resource/w4rt-e856.json"
               "\nDe RDW datasets bevatten geregistreerde autos in Nederland, de RDW heeft veel verschillende datasets met betrekking tot de autos in Nederland"
               "\nWe hebben voor de datasets gekozen waarbij de datums zijn geregistreerd en waarbij de elektrische autos en de verschillende types brandstof staan geregistreerd.")
    st.markdown('### Analyse')

    with st.echo():
        rdw_url_gv = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
        req_rdw_gv = req.get(rdw_url_gv)
        pd_rdw_gv = pd.json_normalize(req_rdw_gv.json())
        display(pd_rdw_gv)
        
        rdw_url_gvb = "https://opendata.rdw.nl/resource/8ys7-d773.json"
        req_rdw_gvb = req.get(rdw_url_gvb)
        pd_rdw_gvb = pd.json_normalize(req_rdw_gvb.json())
        display(pd_rdw_gv)
        
        rdw_url_ev = "https://opendata.rdw.nl/resource/w4rt-e856.json"
        req_rdw_ev = req.get(rdw_url_ev)
        pd_rdw_ev = pd.json_normalize(req_rdw_ev.json())
        display(pd_rdw_gv)
        
        
    st.markdown('### Cleaning Data')
    st.markdown("Wat opviel was dat er per ingeladen dataset zo'n 1000 rijen waren met 15+ kolommen. Veel cellen waren leeg,"
             "\ndeze cellen hebben we ook gewijzigd in Nan waardes." "Ook hebben we de volledige tabbellen zichtbaar gemaakt om te checken of er nog waardes stonden die niet klopten"
             "\nDit hebben wij gedaan door een door de set option functie toe te passen op max_rows en max_columns en de grens op None te zetten."
             "\nD.M.V. het gebruiken van de isna.any.sum functie hebben we gecheckt of er nog eventuele null waardes in de dataset zaten."
             "\nOok hebben we de datums aangepast in een juiste Time Format, d.m.v. het gebruiken van een nieuwe column met de juiste vorm datum d.m.v. strf.time functie"
             "\nZo hebben we de datums gezet in Year-Month. dit was makkelijker aangezien we de lijn diagram per jaar per maand moesten maken.")
             
    st.markdown('### Plots')

    pd_rdw_gv['cleaned.datum_tenaamstelling'] = None
    pd_rdw_gv['cleaned.datum_tenaamstelling'] = pd_rdw_gv.apply(lambda row: datetime.strptime(row["datum_tenaamstelling"], '%Y%m%d').strftime("%Y/%m"), axis=1)
     
    sorted_pd_rdw_gv = pd_rdw_gv['cleaned.datum_tenaamstelling'].value_counts().sort_index()     
     
    fig = px.line(sorted_pd_rdw_gv)

    fig.update_traces(line_color='lawngreen', showlegend=False)
    fig.update_layout(title_text='Lijndiagram van het aantal voertuigen per maand')
    fig.update_xaxes(title_text='Datums')
    fig.update_yaxes(title_text='Aantal voertuigen') 

    st.plotly_chart(fig)

    merk_gv = pd_rdw_gv['merk'].value_counts()     
    merk_gv = merk_gv[merk_gv.values>10]    
     
    fig = px.histogram(merk_gv, x=merk_gv.index, y=merk_gv.values, color=merk_gv.index)

    fig.update_layout(height=500, width=1000, showlegend=False, xaxis_title='Merk', yaxis_title='Aantal voertuigen', 
                  title_text='Histogram aantal voertuigen per merk')

    st.plotly_chart(fig)     
