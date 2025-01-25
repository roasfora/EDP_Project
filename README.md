# **EDP Project**

Este projeto tem como objetivo coletar e processar dados relacionados à **EDP Portugal (EDP.LS)**, utilizando APIs, web scraping e ferramentas de manipulação de dados. Ele combina dados financeiros e notícias relevantes para análises e insights.

---

## ⚙️ **Funcionalidades**

### **1. Coleta de Dados Históricos da Ação**
- Conexão com a **API Alpha Vantage**.
- Coleta de dados ajustados mensais da ação **EDP Portugal**.
- Armazenamento dos dados em um arquivo CSV para análise futura.

### **2. Web Scraping**
#### **a. Taxa de Câmbio EUR para USD**
- Utiliza **Beautiful Soup** para obter a taxa de câmbio EUR para USD do site **x-rates.com**.
- Salva os dados em um arquivo CSV, incluindo o timestamp e o valor da taxa.

#### **b. Notícias sobre EDP no site Lusa**
- Utiliza **Selenium** para acessar e extrair títulos e links de notícias sobre a EDP no site **Lusa.pt**.
- Salva os resultados em um arquivo CSV organizado para análise.

---

## 📦 **Estrutura do Projeto**

```plaintext
EDP_Project/
│
├── src/
│   ├── alpha_vantage_api.py    # Coleta dados históricos de ações via API Alpha Vantage
│   ├── web_scraping.py         # Scripts de web scraping para taxa de câmbio e notícias
│
├── data/                       # Armazena os arquivos CSV gerados
│   ├── monthly_adjusted_data.csv   # Dados da API Alpha Vantage
│   ├── eur_to_usd_rates.csv        # Taxa de câmbio EUR para USD
│   ├── lusa_edp_news.csv           # Notícias sobre a EDP
│
├── dags/                       # DAGs para o Apache Airflow
│   ├── fetch_eur_to_usd_rate.py    # DAG para scraping da taxa de câmbio
│
├── requirements.txt            # Bibliotecas e dependências do projeto
└── README.md                   # Documentação do projeto
