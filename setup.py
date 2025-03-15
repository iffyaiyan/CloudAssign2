import os
import pyodbc
import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

def setup_azure_resources():
    """
    Setup required Azure resources:
    1. Create Azure SQL Database if it doesn't exist
    2. Create Azure Blob Storage container if it doesn't exist
    """
    load_dotenv()
    
    # Setup SQL Database
    try:
        server = os.environ.get('SQL_SERVER')
        database = os.environ.get('SQL_DATABASE')
        username = os.environ.get('SQL_USER')
        password = os.environ.get('SQL_PASSWORD')
        driver = os.environ.get('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')
        
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE=master;UID={username};PWD={password}'
        
        # Connect to master database to create the app database
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{database}'")
        result = cursor.fetchone()
        
        if not result:
            print(f"Creating database {database}...")
            cursor.execute(f"CREATE DATABASE [{database}]")
            print(f"Database {database} created successfully!")
        else:
            print(f"Database {database} already exists.")
        
        conn.close()
        
        # Connect to the app database to create tables
        app_conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        app_conn = pyodbc.connect(app_conn_str)
        app_cursor = app_conn.cursor()
        
        # Create products table
        app_cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'products')
        BEGIN
            CREATE TABLE products (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                description NVARCHAR(MAX),
                price DECIMAL(10, 2) NOT NULL,
                image_url NVARCHAR(255),
                created_at DATETIME DEFAULT GETDATE()
            )
        END
        ''')
        app_conn.commit()
        app_conn.close()
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Database setup error: {str(e)}")
    
    # Setup Blob Storage
    try:
        account_name = os.environ.get('STORAGE_ACCOUNT_NAME')
        account_key = os.environ.get('STORAGE_ACCOUNT_KEY')
        container_name = os.environ.get('STORAGE_CONTAINER_NAME', 'product-images')
        
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Create container if it doesn't exist
        if not container_client.exists():
            container_client.create_container(public_access="blob")
            print(f"Blob container {container_name} created successfully!")
        else:
            print(f"Blob container {container_name} already exists.")
        
        print("Blob storage setup completed successfully!")
        
    except Exception as e:
        print(f"Blob storage setup error: {str(e)}")

if __name__ == "__main__":
    setup_azure_resources()