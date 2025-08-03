import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import numpy as np 

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard de Dados em Tempo Real 📊")
st.write("Criado por Luana Serrão")

st.sidebar.title("Configurações")
st.sidebar.write("Dashboard atualizado em:", datetime.now().strftime("%H:%M:%S"))

st.header("Status: Funcionando.")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Criptomoedas", "Em breve", "📈")

with col2:
    st.metric("Clima", "Em breve", "🌤️")

with col3:
    st.metric("Ações", "Em breve", "📊")

st.success("App funcionando! Agora vamos adicionar os dados reais.")

@st.cache_data(ttl=300)
def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url)
        return response.json()
    except:
        return None
    
st.header("Criptomoedas")
crypto_data = get_crypto_data()

if crypto_data:
    col1, col2 = st.columns(2)

    with col1:
        btc_price = crypto_data['bitcoin']['usd']
        btc_change = crypto_data['bitcoin']['usd_24h_change']
        st.metric("Bitcoin (BTC)", f'${btc_price:,.0f}', f"{btc_change:.1f}%")

    with col2:
        eth_price = crypto_data['ethereum']['usd']
        eth_change = crypto_data['ethereum']['usd_24h_change']
        st.metric("Ethereum (ETH)", f"${eth_price:,.0f}", f"{eth_change:.1f}%")

else:
    st.error("Erro ao carregar dados das criptomoedas.")

import os
from dotenv import load_dotenv
load_dotenv()

@st.cache_data(ttl=1800)
def get_weather_data(city="Manaus"):
    try:
        api_key = st.secret["weather_api_key"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        return response.json()
    except:
        return None
    
st.header("Clima 🌤️")
weather = get_weather_data()

if weather and weather.get('cod') == 200:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Temperatura", f"{weather['main']['temp']:.1f}°C")
    with col2:
        st.metric("Sensação Térmica", f"{weather['main']['feels_like']:.1f}°C")
    with col3:
        st.metric("Umidade", f"{weather['main']['humidity']}%")
    
    st.write(f"Condição: {weather['weather'][0]['description'].title()}")

import plotly.graph_objects as go

st.header("Gráfico Demo")

dates = pd.date_range('2024-01-01', periods=30, freq='D')
values = [100 + i + 10 * np.sin(i / 3) for i in range(30)]

fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name='Exemplo'))
fig.update_layout(title="Evolução ao Longo do Tempo")


st.plotly_chart(fig, use_container_width=True)
