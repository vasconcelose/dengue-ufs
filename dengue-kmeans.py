#!/usr/bin/python

from numpy import *
from pandas import *
from pandasql import *
from scipy.cluster.vq import kmeans
from matplotlib.pyplot import *
from random import *
import seaborn as sns

# melhorar visual dos graficos
sns.set(style='whitegrid')

# configuracoes
csv = 'dados/to-kmeans.csv'
nMaxCentroides = 9 # numero maximo de centroides da analise (2 ... x)

# ver se alguem esta fazendo besteira
if nMaxCentroides < 2:
	exit('impossivel clusterizar com menos de 2 centroides')

# ler csv imputado
dfDengue = read_csv(csv)

x = dfDengue[['media_medicos', 'std_medicos',\
	'media_leitos', 'std_leitos', 'media_dengue_cem_mil_hab', 'std_dengue_cem_mil_hab',\
	'media_obitos_hemorragica', 'std_obitos_hemorragica']]

# calcular grupo de cada estado
for nCentroide in range(2, nMaxCentroides + 1):

	# clusterizar com kmeans
	c, w = kmeans(asarray(x), nCentroide)

	# centroids
	print('Centroides:\n{}\n'.format(c))

	# para guardar o grupo de cada estado
	dfDengue['grupo_' + str(nCentroide)] = 0

	for estado in dfDengue.uf:
		y = dfDengue[(dfDengue.uf == estado)][['media_medicos', 'std_medicos',\
		'media_leitos', 'std_leitos', 'media_dengue_cem_mil_hab', 'std_dengue_cem_mil_hab',\
		'media_obitos_hemorragica', 'std_obitos_hemorragica']]
		y = asarray(y)
		d = zeros(nCentroide)
		for i in range(0, nCentroide):
			d[i] = sqrt(pow((c[i] - y), 2).sum())
		dfDengue.loc[dfDengue.uf == estado, 'grupo_' + str(nCentroide)] = argmin(d)

dfDengue.to_csv('dados/after-kmeans.csv')

# construir visualizacao
for nCentroide in range(2, nMaxCentroides + 1):
	g = 'grupo_' + str(nCentroide)
	dfDengue = dfDengue.sort([g])
	x = range(0, len(dfDengue.uf))
	plot(x, dfDengue[g], color='#CEA6E0', linestyle='none',\
		marker='o', markeredgecolor='black', markeredgewidth=1,\
		markersize=25, alpha=0.6)
	margins(0.05)
	xticks(x, asarray(dfDengue.uf))
	yticks(range(0, nCentroide))
	xlabel('estado')
	ylabel('grupo')
	title('agrupamento {}-means das ufs'.format(nCentroide))
	savefig('graficos/{}-means.png'.format(nCentroide))
	clf()
