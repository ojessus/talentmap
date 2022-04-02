import streamlit as st
import pandas as pd
import numpy as np


def make_clickable(text, url):
    return f'<a href="{url}{text}">{text}</a>'


pd.set_option('display.max_colwidth', -1)
st.set_page_config(layout="wide")
dfraw = pd.read_csv("models/dataraw.csv")
dfindex = pd.read_csv("models/italentotodos.csv")
df = dfraw.set_index('ID').join(dfindex.set_index('ID')).reset_index()[
    ['ID', 'Function', 'indice']].drop_duplicates()

puesto = st.selectbox('Selecionar Function', df.Function.drop_duplicates().to_list(), key=1)
dft = df[df.Function == puesto]
dft['ID'] = dft['ID'].apply(make_clickable, args=(
    'https://talentmap.mattertalent.com/simulador/',))
st.write('<center>'+dft.sort_values(by='indice', ascending=False).head(50).to_html(escape=False,
         index=False)+'</center>', unsafe_allow_html=True)
# st.table(dft.assign(hack='').set_index('hack'))
