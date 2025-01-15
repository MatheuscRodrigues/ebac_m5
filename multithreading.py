# Este script automatiza a extração de detalhes de filmes populares do site IMDb.
# Utilizando bibliotecas como requests para requisições HTTP e BeautifulSoup para parsing HTML,
# ele obtém informações como título, data de lançamento, classificação e sinopse.
# Os dados extraídos são salvos em um arquivo CSV para facilitar a análise posterior.

# Algoritmo (explicando a lógica):
# 1. Define um cabeçalho HTTP para simular um navegador e evitar bloqueios.
# 2. Faz uma requisição à página inicial do IMDb para buscar os 100 filmes mais populares.
# 3. Analisa o HTML usando BeautifulSoup para localizar a tabela de filmes.
# 4. Extrai os links para as páginas individuais de cada filme.
# 5. Usa o máximo de threads permitidas para processar as páginas em paralelo.
# 6. Para cada filme, faz uma requisição, extrai detalhes como título, data, classificação e sinopse.
# 7. Grava os dados em um arquivo CSV, se todas as informações forem encontradas.
# 8. Mede e exibe o tempo total de execução para monitorar o desempenho.
# As informações foram obtidas analisando o HTML da página selecionada.

import requests  # Biblioteca para fazer requisições HTTP e obter conteúdo da web.
import time  # Usada para introduzir atrasos nas requisições, evitando sobrecarregar servidores.
import csv  # Permite gravar dados em formato CSV para armazenar informações extraídas.
import random  # Fornece números aleatórios para simular pausas naturais entre requisições.
import concurrent.futures  # Garante execução de tarefas simultâneas usando threads.
from bs4 import BeautifulSoup  # Biblioteca para analisar e manipular HTML e XML.

# Define um cabeçalho HTTP para simular um navegador e evitar bloqueios
########################## Algoritmo: Passo 1 - Define o cabeçalho
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

# Define o número máximo de threads para execução paralela
MAX_THREADS = 100

# Função para extrair detalhes de um filme a partir de seu link
# O uso de sleep com um atraso aleatório ajuda a evitar ser bloqueado pelo servidor

def extract_movie_details(movie_link):
    ########################## Algoritmo: Passo 6 - Faz requisição e extrai detalhes
    time.sleep(random.uniform(0, 0.2))
    response = requests.get(movie_link, headers=headers)  # Faz uma requisição GET para obter o conteúdo da página do filme
    movie_soup = BeautifulSoup(response.content, 'html.parser')  # Faz o parsing do conteúdo HTML

    if movie_soup is not None:
        title = None
        date = None
        
        # Procura a seção principal da página onde os detalhes do filme estão
        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})
        
        if page_section is not None:
            divs = page_section.find_all('div', recursive=False)  # Obtém divs diretamente contidas na seção
            
            if len(divs) > 1:
                target_div = divs[1]  # A segunda div contém os detalhes relevantes

                # Procura o título do filme
                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()

                # Procura a data de lançamento
                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()

                # Procura a classificação do filme
                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                rating = rating_tag.get_text() if rating_tag else None

                # Procura a sinopse do filme
                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                plot_text = plot_tag.get_text().strip() if plot_tag else None

                # Salva os dados no arquivo CSV
                with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                    movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    ########################## Algoritmo: Passo 7 - Grava os dados no CSV
                    if all([title, date, rating, plot_text]):  # Salva apenas se todos os dados forem válidos
                        print(title, date, rating, plot_text)
                        movie_writer.writerow([title, date, rating, plot_text])

# Função para extrair links de filmes a partir da página principal de filmes populares
# Usa paralelismo para acelerar a extração detalhada de cada filme

def extract_movies(soup):
    ########################## Algoritmo: Passo 3 - Analisa o HTML para localizar a tabela de filmes
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')  # Identifica a tabela de filmes
    movies_table_rows = movies_table.find_all('li')  # Coleta todos os itens da lista (filmes)
    
    ########################## Algoritmo: Passo 4 - Extrai os links dos filmes
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    ########################## Algoritmo: Passo 5 - Usa o máximo de threads para processar os links
    threads = min(MAX_THREADS, len(movie_links))  # Define o número de threads baseado no menor valor entre MAX_THREADS e a quantidade de filmes
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)  # Executa a extração de detalhes em paralelo

# Função principal que coordena o processo de scraping

def main():
    start_time = time.time()  # Marca o tempo de início

    ########################## Algoritmo: Passo 2 - Faz requisição à página inicial para obter a lista de filmes
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)  # Faz uma requisição para obter o HTML da página
    soup = BeautifulSoup(response.content, 'html.parser')  # Cria o objeto BeautifulSoup para parsing

    ########################## Algoritmo: Passo 3 - Extrai os filmes listados na página principal
    extract_movies(soup)

    end_time = time.time()  # Marca o tempo final
    ########################## Algoritmo: Passo 8 - Exibe o tempo total de execução
    print('Total time taken: ', end_time - start_time)  # Exibe o tempo total de execução

# Garante que o script seja executado apenas quando chamado diretamente
if __name__ == '__main__':
    main()