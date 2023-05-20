#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
import panel.widgets as pnw
from holoviews import opts
pn.extension()
hv.extension('bokeh', 'matplotlib')


# In[2]:


# Base de dados
df = pd.read_csv('casos_obitos_doencas_preexistentes.csv.zip', delimiter=';')
dados_dc = df.loc[df['nome_munic']=='Dois Córregos']


# In[3]:


dados_riscos = dados_dc.loc[:,['idade','obito','diabetes','obesidade','outros_fatores_de_risco']].copy()
dados_riscos['obesidade'] = dados_riscos['obesidade'].map({'IGNORADO':0, 'NÃO':1, 'SIM':2})
dados_riscos['outros_fatores_de_risco'] = dados_riscos['outros_fatores_de_risco'].map({'IGNORADO':0, 'NÃO':1, 'SIM':2})
dados_riscos['diabetes'] = dados_riscos['diabetes'].map({'IGNORADO':0, 'NÃO':1, 'SIM':2})
dados_riscos = dados_riscos.rename(columns={'outros_fatores_de_risco':'outros'})
#dados_dc = dados_dc[dados_dc['obesidade'] == 'SIM']
dados_riscos = dados_riscos[dados_riscos['obesidade'] > 0]
dados_riscos['risco'] = dados_riscos['obesidade'] + dados_riscos['outros'] + dados_riscos['diabetes']
dados_riscos = dados_riscos[dados_riscos['outros'] > 0]
dados_final = dados_riscos.loc[:,['obito', 'diabetes', 'obesidade', 'outros', 'risco']].copy()
#dados_final.interactive()


# In[8]:


# funções que geram os gráficos
def graf_obitos():
    counts, edges = np.histogram(dados_dc['obito'], bins=int(np.sqrt(len(dados_dc))))
    obitos_hist = hv.Histogram((edges,counts), kdims=['obito']).opts(fontscale=2, width=600, height=480)
    return obitos_hist
def graf_riscos():
    counts, edges = np.histogram(dados_final, bins=int(np.sqrt(len(dados_final))))
    riscos_hist = hv.Histogram((edges,counts), kdims='riscos').opts(fontscale=2, width=600, height=480)
    return riscos_hist
def graf_escala():
    edges, counts = np.histogram(dados_final['risco'], bins=int(np.sqrt(len(dados_final['risco']))))
    escala = hv.Histogram(data=(edges, counts), kdims='escala').opts(fontscale=2, width=600, height=480)
    return escala
def graf_obito():
    counts, edges = np.histogram(dados_final['obito'], bins=int(np.sqrt(len(dados_final['obito']))))
    obito = hv.Histogram(data=(edges, counts), kdims='obito').opts(fontscale=2, width=600, height=480)
    return obito
def graf_outros():
    counts, edges = np.histogram(dados_final['outros'], bins=int(np.sqrt(len(dados_final['outros']))))
    outros = hv.Histogram(data=(edges, counts), kdims='outros').opts(fontscale=2, width=600, height=480)
    return outros
def graf_obesidade():
    counts, edges = np.histogram(dados_final['obesidade'], bins=int(np.sqrt(len(dados_final['obesidade']))))
    obesidade = hv.Histogram(data=(edges, counts), kdims='obesidade').opts(fontscale=2, width=600, height=480)
    return obesidade
def graf_diabetes():
    counts, edges = np.histogram(dados_final['diabetes'], bins=int(np.sqrt(len(dados_final['diabetes']))))
    diabetes = hv.Histogram(data=(edges, counts), kdims='diabetes').opts(fontscale=2, width=600, height=480)
    return diabetes


# In[9]:


dropdown = pnw.Select(
    name='Selecione o grafico',
    options={'Obitos': graf_obitos, 'Riscos': graf_riscos, 'Escala de Risco': graf_escala, 'Obito': graf_obito,
             'Outros': graf_outros, 'Obesidade': graf_obesidade, 'Diabetes': graf_diabetes},
    value=graf_obitos
)

dashboard = pn.Column(
    '# Informações sobre o COVID', dropdown, pn.panel(None))

def update_plot(event):
    selected_graph = dropdown.value
    dashboard[-1] = pn.panel(selected_graph())
    
dropdown.param.watch(update_plot, 'value')
update_plot(None)
dashboard.servable()


# In[ ]:




