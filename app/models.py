from app import get_db_connection

class Product:
    def __init__(self, id=None, name=None, description=None, price=None, image_url=None, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.created_at = created_at
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description, price, image_url, created_at FROM products ORDER BY created_at DESC')
        
        products = []
        for row in cursor.fetchall():
            products.append(Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                image_url=row[4],
                created_at=row[5]
            ))
        
        conn.close()
        return products
    
    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description, price, image_url, created_at FROM products WHERE id = ?', product_id)
        
        row = cursor.fetchone()
        if row:
            product = Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                image_url=row[4],
                created_at=row[5]
            )
        else:
            product = None
        
        conn.close()
        return product
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id:
            # Update existing product
            cursor.execute(
                'UPDATE products SET name = ?, description = ?, price = ?, image_url = ? WHERE id = ?',
                self.name, self.description, self.price, self.image_url, self.id
            )
        else:
            # Insert new product
            cursor.execute(
                'INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)',
                self.name, self.description, self.price, self.image_url
            )
            
            # Get the ID of the newly inserted product
            cursor.execute('SELECT @@IDENTITY')
            self.id = int(cursor.fetchone()[0])
        
        conn.commit()
        conn.close()
        return self.id