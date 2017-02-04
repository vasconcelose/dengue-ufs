#!/usr/bin/python

from pandas import *
from numpy import *
from pandasql import *
from matplotlib.pyplot import *
import seaborn as sns

# melhorar visual dos graficos
sns.set(style='whitegrid')

# importar dados
csv = 'dados/dados-fixed.csv'

dfDengue = read_csv(csv)

# todos os estados
q = """
	SELECT uf FROM dfDengue
		GROUP BY uf
	"""

estados = sqldf(q, globals())
estados['media_medicos'] = 0
estados['std_medicos'] = 0

# calculo de estatisticas
for estado in estados.uf:

	# medicos
	estados.loc[(estados.uf == estado), 'media_medicos'] =\
		mean(dfDengue[dfDengue.uf == estado].medicos_mil_hab)
	estados.loc[(estados.uf == estado), 'std_medicos'] =\
		std(dfDengue[dfDengue.uf == estado].medicos_mil_hab, ddof=1)

	# leitos
	estados.loc[(estados.uf == estado), 'media_leitos'] =\
		mean(dfDengue[dfDengue.uf == estado].leitos_mil_hab)
	estados.loc[(estados.uf == estado), 'std_leitos'] =\
		std(dfDengue[dfDengue.uf == estado].leitos_mil_hab, ddof=1)

# plots
x = asarray(range(0, len(estados.uf))) * 1.5

# errorbar para a densidade de medicos
errorbar(x, estados.media_medicos, yerr=estados.std_medicos,\
	fmt='o', markersize=10, color='#EB9F3B', alpha=0.75)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de densidade de medicos por estado com barras de erro')
xlabel('estado')
ylabel('medico/mil hab.')
savefig('graficos/@error-bar-media-de-medicos-por-estado.png')
clf()

# errorbar para a densidade de leitos
errorbar(x, estados.media_leitos, yerr=estados.std_leitos,\
	fmt='o', markersize=10, color='#3B9FEB', alpha=0.75)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de densidade de leitos por estado com barras de erro')
xlabel('estado')
ylabel('leito/mil hab.')
savefig('graficos/@error-bar-media-de-leitos-por-estado.png')
clf()
