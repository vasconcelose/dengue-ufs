#!/usr/bin/python

from numpy import *

# retorna a vizinhanca topologica baseada na matriz de
# distancias d e no desvio padrao da gaussiana
def viztopologica(d, s, l):
	h = zeros((l, l))
	for i in range(0, l):
		for j in range(0, l):
			h[i, j] = exp(- d[i, j]**2 /\
				(2 * s**2) )

	return h

# retorna a distancia euclidiana entre o vencedor e
# os demais neuronios do reticulo
def distancias(iMin, jMin, l):
	d = zeros((l, l))
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
def treinar(x, s, n, ts, tn, l, dim, w, N, m):
	nEx = len(x)
	epoca = 1
	while(epoca <= N):
		for ex in range(0, nEx):
			# competicao
			iMin, jMin = vencedor(x[ex], w, l)

			# cooperacao
			d = distancias(iMin, jMin, l)
			h = viztopologica(d, s, l)

			# adaptacao
			
