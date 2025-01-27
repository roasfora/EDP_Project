import pandas as pd
import psycopg2

# Database configuration

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# File paths
MONTHLY_ADJUSTED_DATA_CSV = r"C:\Users\isabe\Desktop\EDIT\EDIT\Data Ops\Company_Project\data\monthly_adjusted_data.csv"
LUSA_EDP_NEWS_CSV = r"C:\Users\isabe\Desktop\EDIT\EDIT\Data Ops\Company_Project\data\lusa_edp_news.csv"

# Function to upload a CSV file to a PostgreSQL table
def upload_csv_to_db(csv_file, table_name, conn):
    try:
        # Load the CSV into a Pandas DataFrame
        df = pd.read_csv(csv_file)

        # Ensure column names match database schema
        if table_name == "monthly_adjusted_data":
            required_columns = ["date", "open", "high", "low", "close", "adjusted_close", "volume", "dividend_amount"]
        elif table_name == "lusa_edp_news":
            required_columns = ["title", "link"]
        else:
            raise ValueError(f"Unknown table: {table_name}")

        # Rename columns if necessary and validate
        if set(required_columns) != set(df.columns):
            print(f"Adjusting column names for {table_name}...")
            if table_name == "monthly_adjusted_data" and "Unnamed: 0" in df.columns:
                df = df.rename(columns={"Unnamed: 0": "date"})
            df = df[required_columns]

        print(f"Carregando {csv_file} com {len(df)} linhas.")

        # Convert all data to strings (for safety)
        df = df.astype(str)

        # Create a cursor
        cur = conn.cursor()

        # Create table if not exists
        columns = ", ".join([f'"{col}" TEXT' for col in required_columns])
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        cur.execute(create_table_query)
        conn.commit()

        # Insert data into the table
        for _, row in df.iterrows():
            columns = ", ".join([f'"{col}"' for col in required_columns])
            values = ", ".join(["%s"] * len(row))
            insert_query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values});'
            cur.execute(insert_query, tuple(row))
        conn.commit()

        print(f"Tabela '{table_name}' preenchida com sucesso.")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao carregar a tabela '{table_name}': {e}")
    finally:
        cur.close()

# Main function
def main():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        print("Conexão com o banco de dados estabelecida.")

        # Upload CSV files to their respective tables
        upload_csv_to_db(MONTHLY_ADJUSTED_DATA_CSV, "monthly_adjusted_data", conn)
        upload_csv_to_db(LUSA_EDP_NEWS_CSV, "lusa_edp_news", conn)

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    main()
