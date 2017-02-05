#!/usr/bin/python

from pandas import *
from pandasql import *
from numpy import *
from matplotlib.pyplot import *
from matplotlib.dates import *

import seaborn as sns

from utilidades import linreg

# melhorar visual dos graficos
sns.set(style='whitegrid')

# caminho para os dados
csvDengue = 'dados/dados.csv'

# ler dados do csv
dfDengue = read_csv(csvDengue)

# converter datas para inteiros (eh apenas ano)
dfDengue.ano =  to_datetime(dfDengue.ano)
dfDengue.ano = dfDengue.ano.map(lambda x: x.strftime('%Y')).astype(int)


""""""


# selecionar estados
q = 'SELECT uf FROM dfDengue GROUP BY uf'
estados = sqldf(q, globals())

# imputar para cada estado
for estado in estados.uf:

	# 1. imputar demografia medica (medicos_mil_hab)

	# anos com demografia medica indisponivel: 2010 e 2012
	q = """
		SELECT * FROM dfDengue
			WHERE uf = '{}'
			AND ano <> 2010
			AND ano <> 2012
		""".format(estado)

	# para tocantins faltam tambem 2000 e 2002
	if (estado == 'TO'):
		q = q + " AND ano <> 2000 AND ano <> 2002"

	dadosUf = sqldf(q, globals())

	# linha de regressao de medicos_mil_hab do estado
	m, b = linreg(dadosUf.ano, dadosUf.medicos_mil_hab)
	print('{}: m_medicos = {}'.format(estado, m))

	# nesse trecho, observar o jeito certo de fazer atribuicao em
	# dataframe no pandas, sem correr o risco de atribuir a uma copia

	# novamente, tratando o caso de tocantins
	if (estado == 'TO'):
		dfDengue.loc[(dfDengue.ano == 2000) & (dfDengue.uf == estado), 'medicos_mil_hab'] =\
			round_(m * 2000 + b, decimals=2)
		dfDengue.loc[(dfDengue.ano == 2002) & (dfDengue.uf == estado), 'medicos_mil_hab'] =\
			round_(m * 2002 + b, decimals=2)

	# imputacao de medicos_mil_hab para 2010 e 2012
	dfDengue.loc[(dfDengue.ano == 2010) & (dfDengue.uf == estado), 'medicos_mil_hab'] =\
		round_(m * 2010 + b, decimals=2)
	dfDengue.loc[(dfDengue.ano == 2012) & (dfDengue.uf == estado), 'medicos_mil_hab'] =\
		round_(m * 2012 + b, decimals=2)

	# gerar grafico mostrando a linha de regressao sobre os dados
	yReg = m * dadosUf.ano + b
	plot(dadosUf.ano, dadosUf.medicos_mil_hab, marker='o', markersize=10, color='#12FFA8', alpha=0.7)
	plot(dadosUf.ano, yReg, color='black', linestyle='--', alpha=0.7)
	title('{}: densidade de medicos'.format(estado))
	margins(0.05)
	xlabel('ano')
	ylabel('medico/mil hab.')
	savefig('graficos/{}-densidade-de-medicos.png'.format(estado))
	clf()

	# 2. taxa de obitos de dengue hemorragica

	dfDengue['taxa_obito_hemorragica'] = 0.0
	dfDengue.loc[(dfDengue.casos_hemorragica != 0), 'taxa_obito_hemorragica'] =\
		round_(dfDengue.obitos_hemorragica / dfDengue.casos_hemorragica, decimals=2)

	# 3. imputacao de leitos por mil habitantes

	# selecionar anos com taxa de leitos disponivel
	q = """
		SELECT * FROM dfDengue
			WHERE uf = '{}'
			AND (
				ano = 1990 OR
				ano = 1992 OR
				ano = 1999 OR
				ano = 2002 OR
				ano = 2005 OR
				ano = 2009
				)
		""".format(estado)

	dadosUf = sqldf(q, globals())

	m, b = linreg(dadosUf.ano, dadosUf.leitos_mil_hab)
	print('{}: m_leitos = {}'.format(estado, m))

	# imputacao de dados de leitos nos anos faltantes
	for a in [1991, 1993, 1994, 1995, 1996, 1997,\
		1998, 2000, 2001, 2003, 2004, 2006, 2007,\
		2008, 2009, 2010, 2011, 2012, 2013, 2014]:

		dfDengue.loc[(dfDengue.ano == a) & (dfDengue.uf == estado), 'leitos_mil_hab'] =\
			round_(m * a + b, decimals=2)

	# geracao de grafico
	yReg = m * dadosUf.ano + b
	plot(dadosUf.ano, dadosUf.leitos_mil_hab, marker='o', markersize=10, color='#FF12A8', alpha=0.7)
	plot(dadosUf.ano, yReg, color='black', linestyle='--', alpha=0.7)
	title('{}: densidade de leitos'.format(estado))
	margins(0.05)
	xlabel('ano')
	ylabel('leito/mil hab.')
	savefig('graficos/{}-densidade-de-leitos.png'.format(estado))
	clf()
	
dfDengue.to_csv('dados/dados-fixed.csv', index=False)
