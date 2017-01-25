#!/usr/bin/python

from numpy import *

# correlacao R entre as series x e y
def correlr(x, y):
	n = float(len(x))
	sx = std(x, ddof=1)
	sy = std(y, ddof=1)
	ux = mean(x)
	uy = mean(y)

	r = (1/(n-1)) * (((x - ux) * (y - uy)) / (sx * sy)).sum()

	return r

# retorna os parametros da linha de regressao das series
def linreg(x, y):
	r = correlr(x,y)

	m = r * std(y, ddof=1)/std(x, ddof=1)
	b = mean(y) - m * mean(x)

	return (m, b)
