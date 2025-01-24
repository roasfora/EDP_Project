from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os

def scrape_lusa_with_selenium():
    """
    Faz scraping no site da Lusa.pt usando Selenium para buscar notícias sobre EDP.
    """
    url = "https://www.lusa.pt/search-results?kw=EDP"

    # Configurando o driver do Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Comente esta linha para depuração visual
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        print("Acessando a página...")
        driver.get(url)
        time.sleep(10)  # Tempo de espera para o carregamento da página
        print("Página carregada. Buscando notícias...")

        # XPath generalizado para capturar todas as manchetes
        articles = driver.find_elements(By.XPATH, '//*[@id="MIDDLE"]//h3/a')

        news_list = []

        for article in articles:
            title = article.text.strip()  # Obtém o texto do título
            link = article.get_attribute("href")  # Obtém o link
            if title and link:
                news_list.append({"title": title, "link": link})

        # Verifica se encontrou notícias
        if not news_list:
            print("Nenhuma notícia encontrada na Lusa.pt.")
            return

        # Salvando os resultados em CSV
        csv_dir = r"C:\Users\isabe\Desktop\EDIT\EDIT\Data Ops\Company_Project\data"
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, "lusa_edp_news.csv")

        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["title", "link"])
            writer.writeheader()
            writer.writerows(news_list)

        print(f"Notícias salvas em: {csv_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_lusa_with_selenium()
