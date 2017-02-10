#!/usr/bin/python

from pandas import *
from numpy import *
from pandasql import *
from matplotlib.pyplot import *

from utilidades import linreg

import seaborn as sns

# melhorar visual dos graficos
sns.set(style='whitegrid')

# importar dados
csv = 'dados/dados-fixed.csv'

dfDengue = read_csv(csv)

# lista de estados
q = """
	SELECT uf FROM dfDengue
		WHERE
			ano >= 1994 AND
			ano <= 2013
		GROUP BY uf
	"""

estados = sqldf(q, globals())

# medias e desvios para graficos
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

	# casos de dengue
	estados.loc[(estados.uf == estado), 'media_dengue_cem_mil_hab'] =\
		mean(dfDengue[dfDengue.uf == estado].dengue_cem_mil_hab)
	estados.loc[(estados.uf == estado), 'std_dengue_cem_mil_hab'] =\
		std(dfDengue[dfDengue.uf == estado].dengue_cem_mil_hab, ddof=1)

	# casos de hemorragica
	estados.loc[(estados.uf == estado), 'media_casos_hemorragica'] =\
		mean(dfDengue[dfDengue.uf == estado].casos_hemorragica)
	estados.loc[(estados.uf == estado), 'std_casos_hemorragica'] =\
		std(dfDengue[dfDengue.uf == estado].casos_hemorragica, ddof=1)

	# obitos hemorragica
	estados.loc[(estados.uf == estado), 'media_obitos_hemorragica'] =\
		mean(dfDengue[dfDengue.uf == estado].taxa_obito_hemorragica)
	estados.loc[(estados.uf == estado), 'std_obitos_hemorragica'] =\
		std(dfDengue[dfDengue.uf == estado].taxa_obito_hemorragica, ddof=1)

# plots
x = asarray(range(0, len(estados.uf))) * 1.5

# errorbar para a densidade de medicos
errorbar(x, estados.media_medicos, yerr=estados.std_medicos,\
	fmt='s', markersize=10, color='#347DEB', alpha=0.7)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de densidade de medicos')
xlabel('estado')
ylabel('medico/mil hab.')
savefig('graficos/@error-bar-media-medicos.png')
clf()

# errorbar para a densidade de leitos
errorbar(x, estados.media_leitos, yerr=estados.std_leitos,\
	fmt='s', markersize=10, color='#124FEB', alpha=0.7)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de densidade de leitos')
xlabel('estado')
ylabel('leito/mil hab.')
savefig('graficos/@error-bar-media-leitos.png')
clf()

# errorbar para casos de dengue
errorbar(x, estados.media_dengue_cem_mil_hab, yerr=estados.std_dengue_cem_mil_hab,\
	fmt='s', markersize=10, color='#1156EB', alpha=0.7)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de taxa de casos de dengue')
xlabel('estado')
ylabel('casos de dengue/cem mil hab.')
savefig('graficos/@error-bar-media-dengue.png')
clf()

# errorbar para casos de hemorragica
errorbar(x, estados.media_casos_hemorragica, yerr=estados.std_casos_hemorragica,\
	fmt='s', markersize=10, color='#A052EF', alpha=0.7)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de casos de dengue hemorragica')
xlabel('estado')
ylabel('numero de casos de dengue hemorragica')
savefig('graficos/@error-bar-casos-hemorragica.png')
clf()

# errorbar para obitos hemorragica
errorbar(x, estados.media_obitos_hemorragica, yerr=estados.std_obitos_hemorragica,\
	fmt='s', markersize=10, color='black', alpha=0.7)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de taxa de obito devido a dengue hemorragica')
xlabel('estado')
ylabel('taxa de obito devido a dengue hemorragica')
savefig('graficos/@error-bar-obitos-hemorragica.png')
clf()

# lista de anos
q = """
	SELECT ano, uf FROM dfDengue
		WHERE ano >= 1994 AND ano <= 2013
		GROUP BY ano
	"""

anos = sqldf(q, globals())

# verificar tendencia de subida da taxa de casos de dengue
for estado in estados.uf:
	x = anos.ano
	y = dfDengue[(dfDengue.ano >= 1994) &\
		(dfDengue.ano <= 2013) &\
		(dfDengue.uf == estado)].dengue_cem_mil_hab
	x = asarray(x)
	y = asarray(y)
	m, b = linreg(x, y)
	print('{}: m_dengue = {}'.format(estado, m))

	y = dfDengue[(dfDengue.ano >= 1994) &\
		(dfDengue.ano <= 2013) &\
		(dfDengue.uf == estado)].taxa_obito_hemorragica
	y = asarray(y)
	m, b = linreg(x, y)
	print('{}: m_hemorragica = {}'.format(estado, m))

# escrever dataframe para depois agrupar
estadosToCsv = estados[['uf', 'media_medicos', 'std_medicos',\
	'media_leitos', 'std_leitos', 'media_dengue_cem_mil_hab', 'std_dengue_cem_mil_hab',\
	'media_obitos_hemorragica', 'std_obitos_hemorragica']]
estadosToCsv.to_csv('dados/to-kmeans.csv', index=False)
