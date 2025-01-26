from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Diretório base da DAG
DAG_DIR = os.path.dirname(os.path.abspath(__file__))

# Função para coletar dados da API Alpha Vantage
def fetch_monthly_adjusted_data():
    """Coleta dados mensais ajustados da API Alpha Vantage."""
    from airflow.models import Variable  # Importar Variable para obter a API Key
    
    # Obter a API Key usando Airflow Variables
    api_key = Variable.get("API_KEY")
    if not api_key:
        raise ValueError("A API Key não está definida no Airflow Variables.")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": "EDP.LS",
        "apikey": api_key,
        "datatype": "json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    if "Monthly Adjusted Time Series" not in data:
        raise ValueError("Erro: Dados não encontrados para o símbolo fornecido.")

    time_series = data["Monthly Adjusted Time Series"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)
    df.columns = [
        "open", "high", "low", "close", 
        "adjusted_close", "volume", "dividend_amount"
    ]
    df = df.sort_index()

    # Caminho para salvar os dados
    data_dir = os.path.join(DAG_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "monthly_adjusted_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Dados mensais ajustados salvos em: {output_path}")


# Função para fazer scraping no site Lusa
def scrape_lusa_with_selenium():
    """Faz scraping de notícias no site Lusa sobre EDP."""
    url = "https://www.lusa.pt/search-results?kw=EDP"
    
    # Configurando o Selenium Manager para gerenciar o WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Modo headless para rodar em ambientes sem GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())  # Selenium Manager para instalar o ChromeDriver

    try:
        print("Inicializando o driver do Chrome...")
        driver = webdriver.Chrome(service=service, options=options)

        print("Acessando a página...")
        driver.get(url)
        time.sleep(10)  # Tempo de espera para o carregamento da página
        print("Página carregada. Buscando notícias...")

        articles = driver.find_elements(By.XPATH, '//*[@id="MIDDLE"]//h3/a')
        news_list = [{"title": article.text.strip(), "link": article.get_attribute("href")} for article in articles if article.text.strip()]

        if not news_list:
            print("Nenhuma notícia encontrada.")
            return

        # Caminho para salvar os dados
        data_dir = os.path.join(DAG_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, "lusa_edp_news.csv")
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["title", "link"])
            writer.writeheader()
            writer.writerows(news_list)

        print(f"Notícias salvas em: {csv_path}")
    except Exception as e:
        print(f"Erro durante o scraping: {e}")
        raise  # Relevanta o erro para que o Airflow registre
    finally:
        if 'driver' in locals():
            driver.quit()


# Definição da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    'collect_edp_data_and_news',
    default_args=default_args,
    description='Coleta dados da API Alpha Vantage e faz scraping de notícias no site Lusa.',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    fetch_api_data = PythonOperator(
        task_id='fetch_api_data',
        python_callable=fetch_monthly_adjusted_data,
    )

    scrape_news = PythonOperator(
        task_id='scrape_news',
        python_callable=scrape_lusa_with_selenium,
    )

    fetch_api_data >> scrape_news
