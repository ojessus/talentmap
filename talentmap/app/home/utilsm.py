import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import shap
import io
import os
from flask import url_for
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
path = os.path.join(SITE_ROOT, "models")+"/"

bd = pd.read_csv(path+"dataraw.csv")
lgbm = pd.read_csv(path+"lgbm_data.csv")
evaluacion = pd.read_csv(path+"Evaluacion.csv")
italentotodos = pd.read_csv(path+"italentotodos.csv")
trayectoria = pd.read_csv(path+"trayectoria.csv")

bdl = pd.read_csv(path+"datarawl.csv")
lgbml = pd.read_csv(path+"lgbm_datal.csv")
evaluacionl = pd.read_csv(path+"Evaluacionl.csv")
italenlider = pd.read_csv(path+"italentolideres.csv")
nombres = pd.read_csv(path+"namescol.csv")
evaluacionTt = pd.read_csv(path+"EvaluacionTt.csv")
evaluacionTl = pd.read_csv(path+"EvaluacionTl.csv")

comercial = pd.read_csv(path+"comercial.csv")
rh = pd.read_csv(path+"recursoshumanos.csv")

rlideres = pd.read_csv(path+"Radareslideres.csv")
rtodos = pd.read_csv(path+"Radarestodos.csv")


shapvp = []
shapvd = []

shapvpl = []
shapvdl = []

base = np.loadtxt(path+"base.csv")
basep = np.loadtxt(path+"basep.csv")

basel = np.loadtxt(path+"basel.csv")
basepl = np.loadtxt(path+"basepl.csv")

shapvd.append(np.loadtxt(path+"shapv0.csv"))
shapvd.append(np.loadtxt(path+"shapv1.csv"))
shapvd.append(np.loadtxt(path+"shapv2.csv"))

shapvdl.append(np.loadtxt(path+"shapv0l.csv"))
shapvdl.append(np.loadtxt(path+"shapv1l.csv"))
shapvdl.append(np.loadtxt(path+"shapv2l.csv"))

shapvp.append(np.loadtxt(path+"shapv0p.csv"))
shapvp.append(np.loadtxt(path+"shapv1p.csv"))
shapvp.append(np.loadtxt(path+"shapv2p.csv"))

shapvpl.append(np.loadtxt(path+"shapv0pl.csv"))
shapvpl.append(np.loadtxt(path+"shapv1pl.csv"))
shapvpl.append(np.loadtxt(path+"shapv2pl.csv"))
varsno = ['Age', 'Position', 'Function', 'Global Pay Grade', 'Technical Entry Date (date format)']


def get_force(ID, eval):
    i = bd.query("ID=="+str(ID)).index[0]
    ev = evaluacion.iloc[i, :]
    evalue = ev[eval]-1
    string_out = io.StringIO()
    print(eval, ID, i)
    if eval == 'Desempeño':
        print(len(shapvd[evalue][i]), len(lgbm.iloc[evalue, :]))
        s = shap.force_plot(base[evalue], shapvd[evalue][i], lgbm.iloc[evalue, :])
    elif eval == 'Potencial':
        print(len(shapvp[evalue][i]), len(lgbm.iloc[evalue, :]))
        s = shap.force_plot(basep[evalue], shapvp[evalue][i], lgbm.iloc[evalue, :])
    shap.save_html(string_out, s)
    return string_out.getvalue()


def get_radar(ID, eval):
    string_out = io.StringIO()
    if eval == 'lideres':
        print(rlideres.columns)
        i = rlideres[rlideres['No. Empleado '] == int(ID)].drop(columns=['No. Empleado '])
    elif eval == 'todos':
        print(rtodos.columns)
        i = rtodos[rtodos['Numero de Empleado '] == int(ID)].drop(columns=['Numero de Empleado '])
    df = pd.DataFrame({'Dimensión': i.columns, 'Evaluación': i.values[0]})
    fig = px.line_polar(df, r='Evaluación', theta='Dimensión', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )
    fig.write_html(string_out)
    return string_out.getvalue()


def get_it(ID):
    i = italentotodos.query("ID=="+str(ID)).values[0][1]
    return str(round(i, 2))

def get_name(ID):
    try:
        i = nombres.query("ID=="+str(ID)).Name.to_list()
        return i[0]
    except:
        return 'Nombre no disponible'


def get_ev(ID, eval):
    i = bd.query("ID=="+str(ID)).index[0]
    ev = evaluacion.iloc[i, :]
    evalue = ev[eval]
    return evalue


def get_evTt(ID, eval):
    try:
        i = evaluacionTt.query("ID=="+str(ID))
        ev = i[eval].values[0]
    except:
        ev = 'S/E'
    return ev


def get_evTl(ID, eval):
    try:
        i = evaluacionTl.query("ID=="+str(ID))
        ev = i[eval].values[0]
    except:
        ev = 'S/E'
    return ev


def get_forcel(ID, eval):
    i = bdl.query("ID=="+str(ID)).index[0]
    ev = evaluacionl.iloc[i, :]
    evalue = ev[eval]-1
    string_out = io.StringIO()
    print(eval, ID, i)
    if eval == 'Desempeño':
        print(len(shapvdl[evalue][i]), len(lgbml.iloc[evalue, :]))
        s = shap.force_plot(basel[evalue], shapvdl[evalue][i], lgbml.iloc[evalue, :])
    elif eval == 'Potencial':
        print(len(shapvpl[evalue][i]), len(lgbml.iloc[evalue, :]))
        s = shap.force_plot(basepl[evalue], shapvpl[evalue][i], lgbml.iloc[evalue, :])
    shap.save_html(string_out, s)
    return string_out.getvalue()


def get_itl(ID):
    v = italenlider.query("ID=="+str(ID)).values[0][1]
    return str(round(v, 2))


def get_evl(ID, eval):
    i = bdl.query("ID=="+str(ID)).index[0]
    ev = evaluacionl.iloc[i, :]
    evalue = ev[eval]
    return evalue


def get_trayect(ID):
    t = trayectoria[trayectoria['Employee Personnel Number'] == int(ID)].dropna().sort_values(by='inicio', ascending=False).groupby(
        ['Employee Personnel Number', 'Position', 'Function']).agg({'inicio': min, 'fin': max}).reset_index().sort_values(by='inicio', ascending=False)
    return t.to_html(index=False).replace('<table border="1" class="dataframe">', '<table class="table">')


def get_comercial():
    urlc = 'http://ec2-3-15-228-102.us-east-2.compute.amazonaws.com/simulador/'
    t = comercial.to_html(index=False, formatters={
                          'ID': lambda x: '<a href="' + urlc + f'{x}">{x}</a>'}, escape=False)
    return t.replace('<table border="1" class="dataframe">', '<table class="table">')


def get_rh():
    urlc = 'http://ec2-3-15-228-102.us-east-2.compute.amazonaws.com/simulador/'
    t = rh.to_html(index=False, formatters={
                   'ID': lambda x: '<a href="' + urlc + f'{x}">{x}</a>'}, escape=False)
    return t.replace('<table border="1" class="dataframe">', '<table class="table">')





def get_isn(ID, eval):
    #string_out = io.StringIO()
    if eval == 'lideres':
        it = get_itl(ID)
        ev = get_evl(ID, 'Potencial')+get_evl(ID, 'Desempeño')
        i = rlideres[rlideres['No. Empleado '] == int(ID)].drop(columns=['No. Empleado '])
    elif eval == 'todos':
        it = get_it(ID)
        ev = get_ev(ID, 'Potencial')+get_ev(ID, 'Desempeño')
        i = rtodos[rtodos['Numero de Empleado '] == int(ID)].drop(columns=['Numero de Empleado '])
    df = pd.DataFrame({'Dimensión': i.columns, 'Evaluación': i.values[0]})
    s1 = float(df['Evaluación'].sum())
    s2 = float(it)
    s3 = float(ev)
    s4 = len(trayectoria[trayectoria['Employee Personnel Number'] == int(ID)].dropna().sort_values(by='inicio', ascending=False).groupby(
        ['Employee Personnel Number', 'Position', 'Function']).agg({'inicio': min, 'fin': max}).reset_index().sort_values(by='inicio', ascending=False))
    g = int(round((22*s1+26*s2+26*s3+26*s4)/10, 0))
    return g



def get_is(ID, eval):
    string_out = io.StringIO()
    if eval == 'lideres':
        it = get_itl(ID)
        ev = get_evl(ID, 'Potencial')+get_evl(ID, 'Desempeño')
        i = rlideres[rlideres['No. Empleado '] == int(ID)].drop(columns=['No. Empleado '])
    elif eval == 'todos':
        it = get_it(ID)
        ev = get_ev(ID, 'Potencial')+get_ev(ID, 'Desempeño')
        i = rtodos[rtodos['Numero de Empleado '] == int(ID)].drop(columns=['Numero de Empleado '])
    df = pd.DataFrame({'Dimensión': i.columns, 'Evaluación': i.values[0]})
    s1 = float(df['Evaluación'].sum())
    s2 = float(it)
    s3 = float(ev)
    s4 = len(trayectoria[trayectoria['Employee Personnel Number'] == int(ID)].dropna().sort_values(by='inicio', ascending=False).groupby(
        ['Employee Personnel Number', 'Position', 'Function']).agg({'inicio': min, 'fin': max}).reset_index().sort_values(by='inicio', ascending=False))
    g = int(round((22*s1+26*s2+26*s3+26*s4)/10, 0))
    print(s1, s2, s3, s4)
    print(g)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=g,
        title={'text': "Índice de sucesión"},
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 40},
        gauge={'axis': {'range': [None, 100]},
               'steps': [
            {'range': [0, 20], 'color': "#E45756"},
            {'range': [20, 40], 'color': "#F58518"},
            {'range': [40, 60], 'color': "#EECA3B"},
            {'range': [60, 80], 'color': "#72B7B2"},
            {'range': [80, 100], 'color': "#54A24B"}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}
    ))
    fig.write_html(string_out)
    return string_out.getvalue()


def get_fortals(ID, eval):
    i = bd.query("ID=="+str(ID)).index[0]
    ev = evaluacion.iloc[i, :]
    evalue = ev[eval]-1
    print(eval, ID, i)
    if eval == 'Desempeño':
        sv = shapvd[evalue][i]
        bv = base[evalue]
        vev = lgbm.iloc[evalue, :]

    elif eval == 'Potencial':
        sv = shapvp[evalue][i]
        bv = base[evalue]
        vev = lgbm.iloc[evalue, :]

    dff = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia>0').sort_values(by='Influencia', ascending=False).head(10)
    dfo = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia<0').sort_values(by='Influencia').head(10)

    return {'fortalezas': dff.to_html(index=False).replace('<table border="1" class="dataframe">', '<table class="table">'),
            'oportunidades': dfo.to_html(index=False).replace('<table border="1" class="dataframe">', '<table class="table">')}


def get_fortalsl(ID, eval):
    i = bdl.query("ID=="+str(ID)).index[0]
    ev = evaluacionl.iloc[i, :]
    evalue = ev[eval]-1
    print(eval, ID, i)
    if eval == 'Desempeño':
        sv = shapvdl[evalue][i]
        bv = basel[evalue]
        vev = lgbml.iloc[evalue, :]

    elif eval == 'Potencial':
        sv = shapvpl[evalue][i]
        bv = basel[evalue]
        vev = lgbml.iloc[evalue, :]

    dff = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia>0').sort_values(by='Influencia', ascending=False).head(10)
    dfo = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia<0').sort_values(by='Influencia').head(10)

    return {'fortalezas': dff.to_html(index=False).replace('<table border="1" class="dataframe">', '<table class="table">'),
            'oportunidades': dfo.to_html(index=False).replace('<table border="1" class="dataframe">', '<table class="table">')}


def get_fortalsb(ID, eval):
    string_out1 = io.StringIO()
    string_out2 = io.StringIO()
    i = bd.query("ID=="+str(ID)).index[0]
    ev = evaluacion.iloc[i, :]
    evalue = ev[eval]-1
    print(eval, ID, i)
    if eval == 'Desempeño':
        sv = shapvd[evalue][i]
        bv = base[evalue]
        vev = lgbm.iloc[evalue, :]
        evaluet = ev['Potencial']-1
        svt = shapvp[evaluet][i]
        bvt = base[evaluet]
        vevt = lgbm.iloc[evaluet, :]
        dfft = pd.DataFrame({'Variable': vevt.index, 'Valor': vevt.to_list(), 'Influencia': svt}).query(
            'Influencia>0').sort_values(by='Influencia').tail(20)
        dfft = dfft[~dfft.Variable.isin(varsno)].tail(10)
        noao = dfft.Variable.to_list()

    elif eval == 'Potencial':
        sv = shapvp[evalue][i]
        bv = base[evalue]
        vev = lgbm.iloc[evalue, :]
        noao = ['tururu']
    # print(noao)
    dff = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia>0')
    dff = dff[~dff.Variable.isin(varsno)].sort_values(by='Influencia').tail(10)
    dfo = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia<0').sort_values(by='Influencia', ascending=False).tail(25)
    dfo = dfo[~dfo.Variable.isin(varsno)]
    dfo = dfo[~dfo.Variable.isin(noao)].tail(10)

    fig1 = go.Figure(go.Bar(
        x=dff.Influencia.to_list(),
        y=dff.Variable.to_list(),
        orientation='h'))
    fig2 = go.Figure(go.Bar(
        x=dfo.Influencia.to_list(),
        y=dfo.Variable.to_list(),
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        ),
        orientation='h'))

    fig1.write_html(string_out1)
    fig2.write_html(string_out2)

    return {'fortalezas': string_out1.getvalue(),
            'oportunidades': string_out2.getvalue()}


def get_fortalslb(ID, eval):
    string_out1 = io.StringIO()
    string_out2 = io.StringIO()
    i = bdl.query("ID=="+str(ID)).index[0]
    ev = evaluacionl.iloc[i, :]
    evalue = ev[eval]-1
    print(eval, ID, i)
    if eval == 'Desempeño':
        sv = shapvdl[evalue][i]
        bv = basel[evalue]
        vev = lgbml.iloc[evalue, :]
        evaluet = ev['Potencial']-1
        svt = shapvpl[evaluet][i]
        bvt = basel[evaluet]
        vevt = lgbml.iloc[evaluet, :]
        dfft = pd.DataFrame({'Variable': vevt.index, 'Valor': vevt.to_list(), 'Influencia': svt}).query(
            'Influencia>0').sort_values(by='Influencia').tail(20)
        dfft = dfft[~dfft.Variable.isin(varsno)].tail(10)
        noao = dfft.Variable.to_list()

    elif eval == 'Potencial':
        sv = shapvpl[evalue][i]
        bv = basel[evalue]
        vev = lgbml.iloc[evalue, :]
        noao = ['tururu']

    dff = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia>0')
    dff = dff[~dff.Variable.isin(varsno)].sort_values(by='Influencia').tail(10)
    dfo = pd.DataFrame({'Variable': vev.index, 'Valor': vev.to_list(), 'Influencia': sv}).query(
        'Influencia<0').sort_values(by='Influencia', ascending=False).tail(25)
    dfo = dfo[~dfo.Variable.isin(varsno)]
    dfo = dfo[~dfo.Variable.isin(noao)].tail(10)
    fig1 = go.Figure(go.Bar(
        x=dff.Influencia.to_list(),
        y=dff.Variable.to_list(),
        orientation='h'))
    fig2 = go.Figure(go.Bar(
        x=dfo.Influencia.to_list(),
        y=dfo.Variable.to_list(),
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        ),
        orientation='h'))

    fig1.write_html(string_out1)
    fig2.write_html(string_out2)

    return {'fortalezas': string_out1.getvalue(),
            'oportunidades': string_out2.getvalue()}
