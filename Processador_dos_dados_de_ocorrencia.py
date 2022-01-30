
#Bibliotecas
import pandas as pd

#O caminho do arquivo gerado pelo Coletor vai aqui
banco_de_dados = pd.read_csv(r"C:\Users\User\Downloads\Banco_de_Dados_Criminalidade.csv", sep = ';')

#Calculando as 3 regiões com mais HOMICÍDIOS DOLOSOS
regioes = banco_de_dados['Regiões'].unique()
homicidios_dolosos = pd.DataFrame(0.0, columns = ['Ocorrências'], index = regioes)
homicidios_dolosos.index.name = 'Regiões'

for i in range(len(banco_de_dados)):
    if banco_de_dados.loc[i]['Natureza'] == 'HOMICÍDIO DOLOSO (2)':
        regiao = banco_de_dados.loc[i]['Regiões']
        ocorrencia = banco_de_dados.loc[i]['Ocorrência']
        homicidios_dolosos.loc[regiao, 'Ocorrências'] = homicidios_dolosos.loc[regiao, 'Ocorrências'] + ocorrencia
homicidios_dolosos = homicidios_dolosos.sort_values(by = 'Ocorrências', ascending = False)
print('As regiões com mais homicídios dolosos nos últimos dois anos foram:')
print(homicidios_dolosos.head(n=3))

#Calculando as 3 regiões com maior AUMENTO DE HOMICÍDIOS DOLOSOS
homicidios_dolosos_2020 = pd.DataFrame(0.0, columns = ['Ocorrências'], index = regioes)
homicidios_dolosos_2020.index.name = 'Regiões'
homicidios_dolosos_2021 = pd.DataFrame(0.0, columns = ['Ocorrências'], index = regioes)
homicidios_dolosos_2021.index.name = 'Regiões'

for i in range(len(banco_de_dados)):
    if banco_de_dados.loc[i]['Natureza'] == 'HOMICÍDIO DOLOSO (2)':
        regiao = banco_de_dados.loc[i]['Regiões']
        ocorrencia = banco_de_dados.loc[i]['Ocorrência']
        if banco_de_dados.loc[i]['Ano'] == 2020:
            homicidios_dolosos_2020.loc[regiao, 'Ocorrências'] = homicidios_dolosos_2020.loc[regiao, 'Ocorrências'] + ocorrencia
        if banco_de_dados.loc[i]['Ano'] == 2021:
            homicidios_dolosos_2021.loc[regiao, 'Ocorrências'] = homicidios_dolosos_2021.loc[regiao, 'Ocorrências'] + ocorrencia

variacao_de_ocorrencias = pd.DataFrame(0.0, columns = ['Ocorrências'], index = regioes)
variacao_de_ocorrencias.index.name = 'Regiões'
for regiao in regioes:
    variacao_de_ocorrencias.loc[regiao, 'Ocorrências'] = homicidios_dolosos_2021.loc[regiao, 'Ocorrências'] - homicidios_dolosos_2020.loc[regiao, 'Ocorrências']
variacao_de_ocorrencias = variacao_de_ocorrencias.sort_values(by = 'Ocorrências', ascending = False)
print('As regiões com maior aumento de homicídios dolosos nos últimos dois anos foram:')
print(variacao_de_ocorrencias.head(n=3))