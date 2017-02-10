# dengue-ufs
Arquivos utilizados para escrever as postagens "Brasil vs. dengue: estamos ganhando ou perdendo a briga?" e "Revelando os perfis da dengue nos estados com k-means clustering" no blog Edudatalab.

https://edudatalab.wordpress.com/

Arquivos:
* dados/dados.csv: base de dados antes da imputação
* dados/dados-fixed.csv: base de dados depois da imputação
* dados/dados.ods: planilha contendo a base de dados antes da imputação
* dados/to-kmeans.csv: dados de entrada para executar o k-means (gerados por wrangle.py)
* dados/after-kmeans.csv: dados de ufs com os grupos gerados pelo k-means
* graficos/*: visualizacoes
* dengue-brasil-imputar.py: arquivo Python para imputação e gráficos de modelos
* dengue-kmeans.py: arquivo chamando k-Means para a base
* m_dengue_e_m_hemorragica.txt: resultados de coeficientes angulares para a doença
* m_medicos_e_m_leitos.txt: resultados de coeficientes angulares para a saúde brasileira
* centroides.txt: resultados de clustering do k-means
* utilidades.py e utilidades.pyc: minha implementação de regressão linear
* wrangle.py: análise exploratória, prepara entrada para o k-means

> Eduardo Vasconcelos<br>
> eduardovasconcelos@usp.br
