from flask import Flask
import pyodbc
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Database connection
def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={app.config["SQL_DRIVER"]};'
        f'SERVER={app.config["SQL_SERVER"]};'
        f'DATABASE={app.config["SQL_DATABASE"]};'
        f'UID={app.config["SQL_USER"]};'
        f'PWD={app.config["SQL_PASSWORD"]}'
    )
    return conn

# Initialize database with products table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create products table if it doesn't exist
    cursor.execute('''
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
    conn.commit()
    conn.close()

# Initialize database at startup
with app.app_context():
    init_db()

# Import routes after app creation to avoid circular imports
from app import routes