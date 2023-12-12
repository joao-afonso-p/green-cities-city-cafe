import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

#https://www.dn.pt/cidades/so-uma-minoria-usa-transportes-publicos-9542110.html 
#https://www.numbeo.com/traffic/in/Porto

working_days = 260
average_minutes_daily = 24
car_passenger_min_co2_kg = 133/1000
public_passenger_min_co2_kg = 15/1000

total_min_year = average_minutes_daily * working_days

car_avg = 69
public_avg = 11
micro_avg = 19
average_in_porto_year = (total_min_year * (car_avg * car_passenger_min_co2_kg + public_avg * public_passenger_min_co2_kg)) / (car_avg+public_avg+micro_avg)
average_in_porto_day = (average_minutes_daily * (car_avg * car_passenger_min_co2_kg + public_avg * public_passenger_min_co2_kg)) / (car_avg+public_avg+micro_avg)

st.title("City Café Sustentável")

st.image("cover.png")

tab1, tab2 = st.tabs(["Calcular", "Histórico"])

with tab1:

    st.markdown("#### Qual é o nosso principal meio de transporte?")

    c1, c2, c3 = st.columns(3)
    car = c1.number_input("Carro", min_value=None, step=1)
    public = c2.number_input("Transportes públicos", min_value=None, step=1)
    micro = c3.number_input("Pedonal ou micromobilidade", min_value=0, step=1)

    submit = st.button("Calcular")

    if submit:
        total_year_emissions = total_min_year * (car * car_passenger_min_co2_kg + public * public_passenger_min_co2_kg)
        avg_year_emissions = total_year_emissions / (car + public + micro)
        total_day_emissions = average_minutes_daily * (car * car_passenger_min_co2_kg + public * public_passenger_min_co2_kg)
        avg_day_emissions = total_day_emissions / (car + public + micro)

        st.write("")
        st.markdown("##### Emissões médias de CO2 (kg)")
        st.write("")
        st.write("")

        c11, c12 = st.columns(2)

        fig1 = go.Figure(go.Indicator(
            value = avg_day_emissions,
            mode = "gauge+number+delta",
            title = {'text': "Hoje"},
            delta = {'reference': average_in_porto_day,
                    'increasing': {'color': "red"},
                    'decreasing': {'color': "green"}},
            gauge = {'axis': {'range': [0, 5]},
                    'threshold' : {'line': {'color': "grey", 'width': 4}, 'thickness': 0.75, 'value': average_in_porto_day}}))

        fig1.update_layout(height=200, width=450)

        fig2 = go.Figure(go.Indicator(
            value = avg_year_emissions,
            mode = "gauge+number+delta",
            title = {'text': "Anualmente"},
            delta = {'reference': average_in_porto_year,
                    'increasing': {'color': "red"},
                    'decreasing': {'color': "green"}},
            gauge = {'axis': {'range': [0, 1000]},
                    'threshold' : {'line': {'color': "grey", 'width': 4}, 'thickness': 0.75, 'value': average_in_porto_year}}))

        fig2.update_layout(height=200, width=450)

        fig1.update_layout(margin=dict(l=20, r=20, b=40, t=40))
        fig2.update_layout(margin=dict(l=20, r=20, b=40, t=40))

        c11.plotly_chart(fig1)
        c12.plotly_chart(fig2)

with tab2:

    st.markdown("#### Histórico de mobilidade")

    data = pd.read_csv("data.csv", delimiter=";")
    data["car_users"] = data["car_users"]*7
    data["public_users"] = data["public_users"]*7
    data["micro_users"] = data["micro_users"]*7
    data = data.rename(columns={"week": "Semana", "car_users": "Carro", "public_users": "Transportes Públicos", "micro_users": "Pedonal e micromobilidade"})

    data["Emissões (kg CO2)"] = data.apply(lambda row: round((average_minutes_daily * (row["Carro"] * car_passenger_min_co2_kg + row["Transportes Públicos"] * public_passenger_min_co2_kg)), 1), axis=1)

    layout = go.Layout(
        xaxis=go.layout.XAxis(
            title='Semana',
            tickmode='array',
            tickvals=[],  # Empty list to hide tick labels
            showticklabels=False
        ),
        yaxis=go.layout.YAxis(
            title='Nº pessoas'
        )
    )


    fig = px.line(data, x='Semana', y=['Emissões (kg CO2)'], title="Emissões semanais")
    st.plotly_chart(fig)


    fig = px.line(data, x='Semana', y=['Carro', 'Transportes Públicos', 'Pedonal e micromobilidade'], title="Meios de transporte")

    st.plotly_chart(fig)
