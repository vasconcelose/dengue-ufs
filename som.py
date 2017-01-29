#!/usr/bin/python

from somut import *
from pandas import *
from pandasql import *
from numpy import *


""" preparacao dos dados de entrada da rede """

# caminho para os dados ja imputados
csvDengue = 'dados/dados-fixed.csv'

# selecao de dados de entrada da som (x)
dfDengue = read_csv(csvDengue)

# anos com dados 100% disponiveis: 94 a 2013
q = """
	SELECT * FROM dfDengue
		WHERE
			ano >= 1994 AND
			ano <= 2013
	"""

# dados de entrada da som
dfDengueCompletos = sqldf(q, globals())
x = dfDengueCompletos[['medicos_mil_hab', 'leitos_mil_hab',\
	'dengue_cem_mil_hab', 'taxa_obito_hemorragica']]
x = asarray(x)

# vou usar as seguintes dimensoes na rede:
# 	- medicos_mil_hab
# 	- leitos_mil_hab
# 	- dengue_cem_mil_hab
# 	- taxa_obito_hemorragica
# para cada par (uf, ano), portanto 4 dimensoes

""""""


""" configuracao dos parametros da rede """

s = 1.0 # desvio da gaussiana
n = 0.02 # taxa de aprendizado
ts = 0.5 # cte de tempo do desvio
tn = 0.5 # cte de tempo da taxa de aprendizado
l = 10 # lado da rede
dim = 4 # numero de dimensoes das entradas
w = random.rand(l, l, dim) # pesos sinapticos
N = 1 # numero maximo de epocas de treinamento
m = 0.001 # minimo admissivel de alteracao nos pesos

""""""


""" treinamento """

w = treinar(x, s, n, ts, tn, l, dim, w, N, m)

""""""
