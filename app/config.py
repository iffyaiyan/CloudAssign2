import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Azure SQL Database configuration
    SQL_SERVER = os.environ.get('SQL_SERVER')
    SQL_DATABASE = os.environ.get('SQL_DATABASE')
    SQL_USER = os.environ.get('SQL_USER')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD')
    SQL_DRIVER = os.environ.get('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')
    
    # Azure Blob Storage configuration
    STORAGE_ACCOUNT_NAME = os.environ.get('STORAGE_ACCOUNT_NAME')
    STORAGE_ACCOUNT_KEY = os.environ.get('STORAGE_ACCOUNT_KEY')
    STORAGE_CONTAINER_NAME = os.environ.get('STORAGE_CONTAINER_NAME', 'product-images')
    
    # Database connection string
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'mssql+pyodbc://{self.SQL_USER}:{self.SQL_PASSWORD}@{self.SQL_SERVER}/{self.SQL_DATABASE}?driver={self.SQL_DRIVER}'