import sys
import os
import pytest
from pandas import DataFrame

# Adicionar o diretório src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from api_alpha_vantage_pydantic import fetch_monthly_adjusted_data

@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Fixture para configurar a chave de API como variável de ambiente."""
    monkeypatch.setenv("API_KEY", "mocked_api_key")

@pytest.fixture
def mock_requests_get(monkeypatch):
    """Fixture para substituir requests.get por um mock."""
    def mock_get(url, params):
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.data = {
                    "Monthly Adjusted Time Series": {
                        "2022-01-31": {
                            "1. open": "2.0",
                            "2. high": "3.0",
                            "3. low": "1.5",
                            "4. close": "2.5",
                            "5. adjusted close": "2.5",
                            "6. volume": "1000",
                            "7. dividend amount": "0.0"
                        }
                    }
                }

            def json(self):
                return self.data

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

def test_fetch_monthly_adjusted_data_returns_dataframe(mock_env_api_key, mock_requests_get):
    """
    Testa se a função fetch_monthly_adjusted_data retorna um DataFrame válido
    ao usar parâmetros mockados.
    """
    # Chamar a função com parâmetros mockados
    result = fetch_monthly_adjusted_data("EDP.LS")

    # Verificar se o resultado é um DataFrame
    assert isinstance(result, DataFrame), "O retorno deveria ser um pandas.DataFrame"
    assert not result.empty, "O DataFrame retornado não deveria estar vazio."
    assert "open" in result.columns, "O DataFrame deveria conter a coluna 'open'."
