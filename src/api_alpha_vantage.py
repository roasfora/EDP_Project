import os
import requests
import pandas as pd

def fetch_monthly_adjusted_data(symbol="EDP.LS"):
    """
    Coleta dados mensais ajustados de ações usando a API Alpha Vantage.
    A API Key é lida de uma variável de ambiente chamada 'API_KEY'.
    
    :param symbol: O símbolo da ação (ex.: "EDP.LS" para EDP Portugal).
    :return: DataFrame contendo os dados históricos mensais ajustados.
    """
    # Obter a API Key do ambiente
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("A API Key não está definida. Configure a variável de ambiente 'API_KEY'.")

    # Endpoint da API
    url = "https://www.alphavantage.co/query"
    
    # Parâmetros da solicitação
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": symbol,
        "apikey": api_key,
        "datatype": "json",  # JSON ou CSV
    }
    
    # Fazendo a solicitação à API
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Garante que erros HTTP sejam tratados
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
    
    # Verificar a resposta da API
    data = response.json()
    if "Monthly Adjusted Time Series" not in data:
        print("Erro: Não foram encontrados dados para o símbolo fornecido.")
        return None

    # Processar os dados
    time_series = data["Monthly Adjusted Time Series"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)  # Converte o índice para datetime
    df.columns = [
        "open", "high", "low", "close", 
        "adjusted_close", "volume", "dividend_amount"
    ]
    df = df.sort_index()  # Ordena por data
    
    # Caminho para salvar o CSV
    output_path = r"C:\Users\isabe\Desktop\EDIT\EDIT\Data Ops\Company_Project\data\monthly_adjusted_data.csv"
    try:
        df.to_csv(output_path)
        print(f"Dados mensais ajustados salvos em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        return None

    return df

if __name__ == "__main__":
    # Certifique-se de que a variável de ambiente 'API_KEY' está configurada antes de rodar o código
    try:
        edp_data = fetch_monthly_adjusted_data()
        if edp_data is not None:
            print(edp_data.head())
    except Exception as e:
        print(f"Erro no programa principal: {e}")
