import requests
import pandas as pd

def fetch_monthly_adjusted_data(api_key, symbol="EDP.LS"):
    """
    Coleta dados mensais ajustados de ações usando a API Alpha Vantage.
    
    :param api_key: Sua chave de API da Alpha Vantage.
    :param symbol: O símbolo da ação (ex.: "EDP.LS" para EDP Portugal).
    :return: DataFrame contendo os dados históricos mensais ajustados.
    """
    # Endpoint da API
    url = "https://www.alphavantage.co/query"
    
    # Parâmetros da solicitação
    params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": symbol,
        "apikey": api_key,
        "datatype": "json",  # JSON ou CSV
    }
    
    # Fazendo a solicitação
    response = requests.get(url, params=params)
    
    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        
        # Obtendo os dados mensais ajustados
        if "Monthly Adjusted Time Series" in data:
            time_series = data["Monthly Adjusted Time Series"]
            
            # Convertendo para um DataFrame
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df.index = pd.to_datetime(df.index)  # Converte o índice para datetime
            df.columns = [
                "open", "high", "low", "close", 
                "adjusted_close", "volume", "dividend_amount"
            ]
            df = df.sort_index()  # Ordena por data
            
            # Caminho para salvar o CSV
            csv_filename = r"C:\Users\isabe\Desktop\EDIT\EDIT\Data Ops\Company_Project\data\monthly_adjusted_data.csv"
            df.to_csv(csv_filename)
            print(f"Dados mensais ajustados salvos em: {csv_filename}")
            
            return df
        else:
            print("Erro: Não foram encontrados dados para o símbolo fornecido.")
            return None
    else:
        print(f"Erro na solicitação: {response.status_code}")
        return None


if __name__ == "__main__":
    # Chave de API da Alpha Vantage
    API_KEY = "IITM7YMI9CMXL71J"
    
    # Coletar os dados da EDP Portugal
    edp_data = fetch_monthly_adjusted_data(API_KEY)
    
    # Exibe os 5 primeiros registros, se disponível
    if edp_data is not None:
        print(edp_data.head())
