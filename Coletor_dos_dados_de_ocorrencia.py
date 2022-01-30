#Requisitos:
# - Instalar o pip (https://bootstrap.pypa.io/get-pip.py)
# - Instalar o Selenium (pip install selenium)
# - Baixar o chromedriver para executar pelo Google Chrome
# - Inserir o caminho do chromedriver.exe em #1

#Bibliotecas
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

#Seleção do .exe do webdriver
driver = webdriver.Chrome(service = Service(r"C:\Users\User\Downloads\chromedriver.exe")) #1

#Acesso ao site e busca pelos dados
driver.get('http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx')

ocorrencia_registrada_por_mes = driver.find_element(By.LINK_TEXT, 'Ocorrências Registradas por Mês')

ocorrencia_registrada_por_mes.click()

regioes = driver.find_element(By.ID, 'conteudo_ddlRegioes')

select = Select(regioes)

regioes_lista = [rl.text for rl in select.options]

banco_de_dados = pd.DataFrame(columns = ['Regiões', 'Ano', 'Mês', 'Natureza', 'Ocorrência'])

regioes.click()

#Busca pelos dados entre as colunas j e linhas i de cada ano de cada região k
for k in range (1, len(regioes_lista)):
    
    select.select_by_visible_text(regioes_lista[k])
    
    num_linhas_20 = len (driver.find_elements(By.XPATH, '//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr'))
    num_colunas_20 = len (driver.find_elements(By.XPATH, '//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr/th'))
    
    for j in range(1, num_colunas_20-1):
        
        caminho_mes = '//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr/th[' + str(j+1) + ']'
        mes = driver.find_element(By.XPATH, caminho_mes).text
        
        for i in range(1, num_linhas_20):
            
            caminho_natureza = '//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr[' + str(i+1) + ']/td[1]'
            natureza = driver.find_element(By.XPATH, caminho_natureza).text
            
            caminho_valor = '//*[@id="conteudo_repAnos_gridDados_2"]/tbody/tr[' + str(i+1) + ']/td[' + str(j+1) + ']'
            valor = driver.find_element(By.XPATH, caminho_valor).text
            
            dados_series = pd.Series([regioes_lista[k], '2020', mes, natureza, valor], index = banco_de_dados.columns)
            banco_de_dados = banco_de_dados.append(dados_series, ignore_index= True)
      
    num_linhas_21 = len (driver.find_elements(By.XPATH, '//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr'))
    num_colunas_21 = len (driver.find_elements(By.XPATH, '//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr/th'))
    
    for j in range(1, num_colunas_20-1):
        
        caminho_mes = '//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr/th[' + str(j+1) + ']'
        mes = driver.find_element(By.XPATH, caminho_mes).text
        
        for i in range(1, num_linhas_20):
            
            caminho_natureza = '//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr[' + str(i+1) + ']/td[1]'
            natureza = driver.find_element(By.XPATH, caminho_natureza).text
            
            caminho_valor = '//*[@id="conteudo_repAnos_gridDados_1"]/tbody/tr[' + str(i+1) + ']/td[' + str(j+1) + ']'
            valor = driver.find_element(By.XPATH, caminho_valor).text
            
            dados_series = pd.Series([regioes_lista[k], '2021', mes, natureza, valor], index = banco_de_dados.columns)
            banco_de_dados = banco_de_dados.append(dados_series, ignore_index= True)
            
    regioes = driver.find_element(By.ID, 'conteudo_ddlRegioes')
    select = Select(regioes)
    regioes.click()
    
driver.quit()

#Correção dos dados numéricos
banco_de_dados['Ocorrência'] = banco_de_dados['Ocorrência'].str.replace('.','', regex = False)

#O caminho de download vai aqui
banco_de_dados.to_csv(r"C:\Users\User\Downloads\Banco_de_Dados_Criminalidade.csv", sep = ';', index = False)
