import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np


def make_clickable(text, url):
    return f'<a href="{url}{text}">{text}</a>'


pd.set_option('display.max_colwidth', -1)
st.set_page_config(layout="wide")
dflideres = pd.read_csv("models/datarawl.csv")
dftodos = pd.read_csv("models/dataraw.csv")
idsl = [int(i) for i in dflideres.ID.drop_duplicates().values]
idst = [int(i) for i in dftodos.ID.drop_duplicates().values]
numemp = st.selectbox('Selecionar Numero de Empleado', idsl+idst, key=1)
if int(numemp) in idst:
    components.iframe("https://talentmap.mattertalent.com/simulador/" +
                      str(numemp), height=1000, scrolling=True)
elif int(numemp) in idsl:
    components.iframe("https://talentmap.mattertalent.com/simuladorl/" +
                      str(numemp), height=1000, scrolling=True)
else:
    st.write('ID no dosponible')
