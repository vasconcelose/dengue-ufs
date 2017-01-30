#!/usr/bin/python

from numpy import *
from random import shuffle
from os import *

# calcula saida da rede
def saida(x, w, l):
	d = zeros((l, l))
	for i in range(0, l):
		for j in range(0, l):
			d[i, j] = sqrt(sum(pow(x - w[i, j], 2)))
	
	i, j = unravel_index(d.argmin(), d.shape)

	return (i, j)

# atualiza valor de s
def novos(so, epoca, ts):
	return so * exp(- epoca / ts)

# atualiza valor de n
def novon(no, epoca, tn):
	return no * exp(- epoca / tn)

# retorna a vizinhanca topologica baseada na matriz de
# distancias d e no desvio padrao da gaussiana
def viztopologica(d, s):
	h = exp(- d**2 / (2 * s**2) )

	return h

# retorna a distancia euclidiana entre o vencedor e
# os demais neuronios do reticulo
def distancias(iMin, jMin, l, dim):
	d = zeros((l, l, dim))
	for i in range(0, l):
		for j in range(0, l):
			d[i, j] = sqrt(pow(i - iMin, 2) +\
				pow(j - jMin, 2))

	return d

# coordena treinamento da som
def treinar(x, so, no, ts, tn, l, dim, w, N):
	nEx = len(x)
	epoca = 1
	s = so
	n = no

	while(epoca <= N):

		shuffle(x)

		for ex in range(0, nEx):

			# atualizar console
			system('clear')
			print('Epoca {}\nExemplar {}/{}'.format(epoca,\
				ex, nEx))

			# competicao
			iMin, jMin = saida(x[ex], w, l)

			# cooperacao
			d = distancias(iMin, jMin, l, dim)
			h = viztopologica(d, s)

			# adaptacao
			w = w + n * h * (x[ex] - w)

			# atualiza parametros da som
			s = novos(so, epoca, ts)
			n = novon(no, epoca, tn)

		epoca = epoca + 1

	return w
