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
		WHERE
			ano >= 1994 AND
			ano <= 2013
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

# errorbar para casos de dengue
errorbar(x, estados.media_dengue_cem_mil_hab, yerr=estados.std_dengue_cem_mil_hab,\
	fmt='o', markersize=10, color='#3AEF12', alpha=0.75)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de taxa de casos de dengue com barras de erro')
xlabel('estado')
ylabel('casos de dengue/cem mil hab.')
savefig('graficos/@error-bar-media-de-casos-de-dengue-por-estado.png')
clf()

# errorbar para casos de hemorragica
errorbar(x, estados.media_casos_hemorragica, yerr=estados.std_casos_hemorragica,\
	fmt='o', markersize=10, color='#3A12EF', alpha=0.75)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de casos de dengue hemorragica por estado com barras de erro')
xlabel('estado')
ylabel('numero de casos de dengue hemorragica')
savefig('graficos/@error-bar-casos-de-hemorragica-por-estado.png')
clf()

# errorbar para obitos hemorragica
errorbar(x, estados.media_obitos_hemorragica, yerr=estados.std_obitos_hemorragica,\
	fmt='o', markersize=10, color='black', alpha=0.75)
xticks(x, asarray(estados.uf))
margins(0.05)
title('media anual de taxa de obito devido a dengue hemorragica por estado com barras de erro')
xlabel('estado')
ylabel('taxa de obito devido a dengue hemorragica')
savefig('graficos/@error-bar-obitos-hemorragica-por-estado.png')
clf()
