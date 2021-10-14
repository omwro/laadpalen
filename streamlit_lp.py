import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff




def main():
    st.title("Laadpaal Data")
    st.header("Importeren, opschonen en filteren van data")
    paalData = pd.read_csv('laadpaaldata.csv')
    paalData.head()
    st.code("paalData = pd.read_csv('laadpaaldata.csv')"
    "\npaalData.head()")
    fig = px.scatter(x=paalData['ChargeTime'],y=paalData['ConnectedTime'],labels={'x':'Laadtijd','y':'Aansluit tijd'})
    st.plotly_chart(fig)
    st.caption("Er is hier te zien dat er duidelijke outliers zijn in de laadtijd, deze worden gefilterd door middel van:")
    st.code("paalData = paalData[paalData['ChargeTime'] > 0]"
            "\npaalData = paalData[paalData['ChargeTime'] < 7]")
    paalData = paalData[paalData['ChargeTime'] > 0]
    paalData = paalData[paalData['ChargeTime'] < 7]

    st.caption("We houden nu het volgende DataFrame over:")
    st.dataframe(paalData)

    with st.echo():
        st.write(type(paalData.loc[0]['Started']))

    st.caption("Het type data in de Started en Ended kolommen zijn nu nog String. Dit is te fixen door pd.to_datetime te gebruiken:")
    st.code("paalData = paalData.assign(Started = lambda x: pd.to_datetime(x['Started'],errors='coerce'))"
            "\npaalData = paalData.assign(Ended = lambda x: pd.to_datetime(x['Ended'],errors='coerce'))")
    paalData = paalData.assign(Started=lambda x: pd.to_datetime(x['Started'], errors='coerce'))
    paalData = paalData.assign(Ended=lambda x: pd.to_datetime(x['Ended'], errors='coerce'))
    paalData = paalData[paalData['Started'] >= "2017-01-01 08:45:26"]
    paalData = paalData[paalData['Ended'] >= "2017-01-01 08:45:26"]

    st.caption("Nu kan deze functie gebruikt worden om te checken of er geen ")
    with st.echo():
        st.write(paalData.isna().sum())

    winter = paalData[paalData['Started'] <= "2018-03-21 23:59:59"]
    lente = paalData[paalData['Started'] <= "2018-06-21 23:59:59"]
    lente = lente[lente['Started'] > "2018-03-21 23:59:59"]
    zomer = paalData[paalData['Started'] > "2018-06-21 23:59:59"]
    zomer = zomer[zomer['Started'] <= "2018-09-21 23:59:59"]
    herfst = paalData[paalData['Started'] > "2018-09-21 23:59:59"]
    herfst = herfst[herfst['Started'] <= "2018-12-21 23:59:59"]

    st.caption("Nu de kolommen de juiste datatypes hebben, kan het dataframe per seizoen gefilterd worden:")
    st.code("winter = paalData[paalData['Started'] <= '2018-03-21 23:59:59']"
            "\n"
            "\nlente = paalData[paalData['Started'] <= '2018-06-21 23:59:59']"
            "\nlente = lente[lente['Started'] > '2018-03-21 23:59:59']")

    st.header("Laadtijd plots")

    st.caption('Als eerste is een histogram gemaakt met de verdeling van laadtijden in 2018, die te filteren is op seizoen. Het gemiddelde en de mediaan zijn weergegeven met pijlen in elke plot.')

    fig = go.Figure()

    # Add traces of charge time for the different seasons
    fig.add_trace(go.Histogram(x=paalData['ChargeTime'], name='2018 totaal', nbinsx=10, ))
    fig.add_trace(go.Histogram(x=winter['ChargeTime'], name='winter', nbinsx=10))
    fig.add_trace(go.Histogram(x=lente['ChargeTime'], name='lente', nbinsx=10))
    fig.add_trace(go.Histogram(x=zomer['ChargeTime'], name='zomer', nbinsx=10))
    fig.add_trace(go.Histogram(x=herfst['ChargeTime'], name='herfst', nbinsx=10))

    # Add annotation for the mean
    laadMean = str(paalData['ChargeTime'].mean())[:3]
    laadMedian = str(paalData['ChargeTime'].median())[:3]
    annotationMean = {'x': paalData['ChargeTime'].mean(),
                      'y': 400,
                      'showarrow': True,
                      'arrowhead': 4,
                      'font': {'size': 15, 'color': 'red'},
                      'text': 'Gemiddelde laadtijd = ' + laadMean + " uur"}
    annotationMedian = {'x': paalData['ChargeTime'].median(),
                        'y': 800,
                        'showarrow': True,
                        'arrowhead': 2,
                        'font': {'size': 15, 'color': 'green'},
                        'text': 'Mediaan van laadtijd = ' + laadMedian + " uur"}
    fig.update_layout({'annotations': [annotationMean, annotationMedian]})

    my_legend = {'x': 1, 'y': 0, 'bgcolor': 'rgb(0, 0, 0)', 'borderwidth': 5}
    fig.update_layout({'showlegend': True, 'legend': my_legend},
                      title="Verdeling van laadtijden in 2018",
                      xaxis_title_text='Laad tijd (uur)',
                      yaxis_title_text='Aantal waarnemingen', )

    sliders = [
        {'steps': [
            {'method': 'update', 'label': '2018 totaal', 'args': [{'visible': [True, False, False, False, False]}]},
            {'method': 'update', 'label': 'winter', 'args': [{'visible': [False, True, False, False, False]}]},
            {'method': 'update', 'label': 'lente', 'args': [{'visible': [False, False, True, False, False]}]},
            {'method': 'update', 'label': 'zomer', 'args': [{'visible': [False, False, False, True, False]}]},
            {'method': 'update', 'label': 'herfst', 'args': [{'visible': [False, False, False, False, True]}]}]}]

    fig.update_layout({'sliders': sliders})

    st.plotly_chart(fig)
    st.caption("Zoals te zien is is de gemiddelde laadtijd 2.3 uur, en is de mediaan 2.2 uur. Ook is te zien dat de laadtijden niet veranderen per seizoen.")
    st.caption("")
    st.caption("De volgende plot geeft de kansdichtheidsfunctie weer van de laadtijden in 2018. Er is een piek te zien bij het gemiddelde van 2.3 uur.")
    # Add histogram data
    x1 = paalData['ChargeTime']

    # Group data together
    hist_data = [x1]

    group_labels = ["2018 laadtijd kansdichtheidsfunctie"]

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
    st.plotly_chart(fig)











