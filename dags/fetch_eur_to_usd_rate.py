from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Diretório da DAG
DAG_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_eur_to_usd_rate():
    """Scrape EUR to USD exchange rate and return the data."""
    try:
        # URL para scraping
        url = "https://www.x-rates.com/calculator/?from=EUR&to=USD&amount=1"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extrair a taxa de câmbio
            rate_element = soup.find("span", class_="ccOutputRslt")
            if rate_element:
                rate = float(rate_element.text.split()[0])

                # Preparar os dados
                data = {
                    "timestamp": datetime.utcnow().isoformat(),  # UTC para consistência
                    "eur_to_usd_rate": rate
                }
                return data
            else:
                raise Exception("Could not find the exchange rate on the webpage.")
        else:
            raise Exception(f"Failed to fetch the webpage: {response.status_code}")
    except Exception as e:
        raise RuntimeError(f"Error scraping EUR to USD exchange rate: {e}")

def save_to_csv(**kwargs):
    """Save EUR to USD exchange rate data to a CSV file."""
    # Caminho absoluto para salvar o CSV
    data_dir = os.path.join(DAG_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)  # Criar a pasta, se necessário
    filepath = os.path.join(data_dir, "eur_to_usd_rates.csv")

    # Buscar os dados do XCom (retornados pela tarefa anterior)
    data = kwargs['ti'].xcom_pull(task_ids='fetch_rate')

    # Carregar dados existentes, se o arquivo existir
    if os.path.isfile(filepath):
        df = pd.read_csv(filepath)
    else:
        df = pd.DataFrame(columns=["timestamp", "eur_to_usd_rate"])

    # Adicionar os novos dados
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)

    # Salvar o CSV atualizado
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

# Definição da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    'fetch_and_save_eur_to_usd_rate',
    default_args=default_args,
    description='Fetch EUR to USD exchange rate and save to CSV',
    schedule='@daily',  # Frequência de execução
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    fetch_rate = PythonOperator(
        task_id='fetch_rate',
        python_callable=fetch_eur_to_usd_rate,
    )

    save_rate = PythonOperator(
        task_id='save_rate',
        python_callable=save_to_csv,
    )

    fetch_rate >> save_rate
