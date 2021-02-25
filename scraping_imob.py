### DESCRIÇÃO
# Este código irá coletar os dados de apartamentos que estão sendo vendidos na cidade de São Paulo.
# Ele retornará um arquivo csv e excel com as informações.

### FUNÇÕES

# wait_page: verifica o carregamento das páginas
def wait_page(drv):
    status = 0
    for t in range(5):
        timeout = 3
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(drv, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            time.sleep(1)
            status = 1
            break
      
    if (status == 0):
        print("Falha")
    
    return status

### BIBLIOTECAS

from selenium import webdriver
import pandas as pd
import time

### CÓDIGO

# Criação do DF
df = pd.DataFrame()   
df = pd.DataFrame(columns = ['PREÇO', 'ÁREA', 'QUARTOS', 'BANHEIROS', 'VAGA GARAGEM'])

# Paginação

URL_1 = 'https://www.lopes.com.br/busca/venda/br/sp/sao-paulo/tipo/apartamento'
URL_2 = '?estagio=real_estate&exp=pfcc:a&tipo=APARTMENT'
PG_ATUAL = 1
PG_ANTERIOR = 0
count = 0

driver = webdriver.Chrome()
    
while PG_ATUAL != PG_ANTERIOR:
    page = URL_1 + '/pagina/' + str(PG_ATUAL) + URL_2
    driver.get(page)

    # Aguarda carregar a página
    time.sleep(1)
    if(wait_page(driver) == 0):
        print("ERRO")
        
    print('Página {}'.format(PG_ATUAL))
    
    dados = driver.find_elements_by_xpath('/html/body/lps-root/lps-search/div/div/div[1]/lps-search-grid/lps-search-content/div/perfect-scrollbar/div/div[1]/div[2]/lps-card-grid/div[1]/ul/li/lps-card-product/lps-link-product/div/a')

    for dado in dados:
        aux_dado = dado.get_attribute('text')
        vetor_dado = aux_dado.split(' ')
        
        # Preço
        preco = vetor_dado[1].strip('R$')
        preco = preco.replace('.', '')
        preco = float(preco)
        
        aux_area = aux_dado.split('São Paulo')
        aux_area2 = aux_area[1].split(' ')
        
        # Área
        area = aux_area2[1]
        area = area.replace('m²', '')
        area = float(area)
        
        # Quartos
        quartos = aux_area2[3]
        quartos = int(quartos)

        # Banheiros
        banheiros = aux_area2[5]
        banheiros = int(banheiros)
        
        # Garagem
        if len(aux_area2) > 7:
            garagem = aux_area2[7]
            garagem = int(garagem)
        else:
            garagem = 0
        
        # Salvando no df
        df.loc[count] = [preco, area, quartos, banheiros, garagem]
        count += 1

    # Coleta os dados do apartamento
    paginas = driver.find_elements_by_xpath('/html/body/lps-root/lps-search/div/div/div[1]/lps-search-grid/lps-search-content/div/perfect-scrollbar/div/div[1]/div/div[1]/nz-pagination/ul/li/a')
    
    for pagina in paginas:
        pg = pagina.get_attribute('text')
        if pg != '•••' and pg != '':
            if int(pg) == (int(PG_ATUAL) + 1):
                PG_AUX = int(pg)
    
    print('Apartamentos registrados: {}'.format((count)))
    PG_ATUAL = PG_AUX
    PG_ANTERIOR += 1

# Salvando o df no pc
df.to_csv('df_apartamentos.csv', index = False)
df.to_excel('df_apartamentos.xlsx', index = False)

print('Terminou. {} apartamentos salvos.'.format(count))

driver.quit()