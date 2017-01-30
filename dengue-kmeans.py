#!/usr/bin/python

from numpy import *
from pandas import *
from pandasql import *
from scipy.cluster.vq import kmeans

csv = 'dados/dados-fixed.csv'
nCentroides = 2

# ler csv imputado
dfDengue = read_csv(csv)

# selecionar anos com todas as colunas disponiveis: 94 a 2013
q = """
	SELECT * FROM dfDengue
		WHERE ano >= 1994 AND
			ano <= 2013
	"""

x = sqldf(q, globals())
xObs = x[['medicos_mil_hab', 'leitos_mil_hab',\
	'dengue_cem_mil_hab', 'taxa_obito_hemorragica']]

# clusterizar com kmeans
c, d = kmeans(asarray(xObs), nCentroides)

print(c)
