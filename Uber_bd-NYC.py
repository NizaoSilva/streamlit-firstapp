# """
# To run your code you can use:
# python -m streamlit run your_script.py
# or just :
# py -m streamlit run c:\Users\Skidrow-NT\Desktop\Python\streamlit\Uber_bd-NYC.py
# To create venv:
# https://www.youtube.com/watch?v=yG9kmBQAtW4
# """

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber: dados público de NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Carregando dados...')
data = load_data(20000)
data_load_state.text("Prontinho!")

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

st.subheader('Número de coletas por hora')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('Hora', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Mapa de todas as coletas as %s:00' % hour_to_filter)
st.map(filtered_data)