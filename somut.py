#!/usr/bin/python

from numpy import *
from random import shuffle
from os import *

# atualiza valor de s
def novos(so, epoca, ts):
	return so * exp(- epoca / ts)

# atualiza valor de n
def novon(no, epoca, tn):
	return no * exp(- epoca / tn)

# retorna a vizinhanca topologica baseada na matriz de
# distancias d e no desvio padrao da gaussiana
def viztopologica(d, s, l, dim):
	h = zeros((l, l, dim))
	for i in range(0, l):
		for j in range(0, l):
			h[i, j] = exp(- d[i, j]**2 /\
				(2 * s**2) )

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


# retorna indices do neuronio vencedor (menor argmin)
def vencedor(x, w, l):
	sqrDif = square(x - w)
	v = zeros((l, l))
	for i in range(0, l):
		for j in range(0, l):
			v[i, j] = sqrt(sqrDif[i, j].sum())
	
	return unravel_index(v.argmin(), v.shape)

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
			iMin, jMin = vencedor(x[ex], w, l)

			# cooperacao
			d = distancias(iMin, jMin, l, dim)
			h = viztopologica(d, s, l, dim)

			# adaptacao
			w = w + n * h * (x[ex] - w)

			# atualiza parametros da som
			s = novos(so, epoca, ts)
			n = novon(no, epoca, tn)

		epoca = epoca + 1

	return w
