#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import panel as pn
import holoviews as hv
import panel.widgets as pnw
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter
from holoviews import opts
pn.extension()
hv.extension('matplotlib')


# In[2]:


df = pd.read_csv('casos_obitos_doencas_preexistentes.csv.zip', delimiter=';')
dados_dc = df.loc[df['nome_munic']=='Dois Córregos']


# In[3]:


def graf_obitos():
    plt.hist(dados_dc['obito'], bins=10)
    counts, edges = np.histogram(dados_dc['obito'], bins=10)
    obitos_hist = hv.Histogram((edges,counts), kdims=['obito'])
    return obitos_hist


# In[4]:


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


# In[5]:


def graf_riscos():
    counts, edges = np.histogram(dados_final, bins=10)
    hv.output(backend='matplotlib')
    riscos_hist = hv.Histogram((edges,counts))
    return riscos_hist


# In[6]:


dropdown = pnw.Select(
    name='Selecione o grafico',
    options={'Obitos': graf_obitos, 'Riscos': graf_riscos}
)
dashboard = pn.Column(
    '# Dashboard', dropdown, pn.panel(None)
)
def update_plot(event):
    selected_graph = dropdown.value
    dashboard[-1] = pn.panel(selected_graph())
dropdown.param.watch(update_plot, 'value')
dashboard.servable()


# In[ ]:




