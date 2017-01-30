#!/usr/bin/python

from somut import *
from pandas import *
from pandasql import *
from numpy import *
from matplotlib.pyplot import *


""" preparacao dos dados de entrada da rede """

# caminho para os dados ja imputados
csvDengue = 'dados/dados-fixed.csv'

# selecao de dados de entrada da som (x)
dfDengue = read_csv(csvDengue)

# transformacao de dados para possibilitar separacao
dfDengue.medicos_mil_hab = dfDengue.medicos_mil_hab**3
dfDengue.leitos_mil_hab = exp(dfDengue.leitos_mil_hab)
dfDengue.taxa_obito_hemorragica = exp(\
	dfDengue.taxa_obito_hemorragica)
dfDengue.dengue_cem_mil_hab =\
	exp(dfDengue.dengue_cem_mil_hab / 100)

# anos com dados 100% disponiveis: 94 a 2013
q = """
	SELECT * FROM dfDengue
		WHERE ano = 2013
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

so = 15.0 # desvio inicial da gaussiana
no = 2.0 # taxa de aprendizado inicial
ts = 1.2 # cte de tempo do desvio
tn = 1.2 # cte de tempo da taxa de aprendizado
l = 20 # lado da rede
dim = 4 # numero de dimensoes das entradas
w = random.rand(l, l, dim) # pesos sinapticos
N = 2 # numero maximo de epocas de treinamento

""""""


""" treinamento """
# x = [ [-1, -1], [1, 1], [-2.5, -2.5], [3.0, 3.0] ]
# dim = 2
# w = random.rand(l, l, dim)
w = treinar(x, so, no, ts, tn, l, dim, w, N)

img = zeros((l, l))

for k in range(0, len(x)):
	i, j = saida(x[k], w, l)
	img[i, j] = img[i, j] + 1

imshow(img)
show()
clf()

""""""
