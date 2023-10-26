import sqlite3
import bcrypt

class DatabaseManager:
    def __init__(self, db_name='stocks.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create the 'users' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                hashed_password TEXT NOT NULL
            )
        ''')

        # Create the 'stocks' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute('''
            INSERT INTO users (username, hashed_password) VALUES (?, ?)
        ''', (username, hashed_password))
        self.conn.commit()

    def authenticate_user(self, username, password):
        self.cursor.execute('SELECT hashed_password FROM users WHERE username = ?', (username,))
        row = self.cursor.fetchone()
        if row:
            stored_hash = row[0]
            # Check if the provided password matches the stored hash
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False

    def add_stock(self, user_id, symbol, price, volume):
        self.cursor.execute('''
            INSERT INTO stocks (user_id, symbol, price, volume) VALUES (?, ?, ?, ?)
        ''', (user_id, symbol, price, volume))
        self.conn.commit()

    def get_user_stocks(self, user_id):
        self.cursor.execute(
            'SELECT * FROM stocks WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# Example usage:
db_manager = DatabaseManager()

# Adding a user
db_manager.add_user('john_doe', 'password123')

# # Authenticating a user
# is_authenticated = db_manager.authenticate_user('john_doe', 'password123')
# print(f"Is John authenticated? {is_authenticated}")

# Adding a stock for the authenticated user
user_id = 1  # Assuming user_id for 'john_doe'
db_manager.add_stock(user_id, 'AAPL', 150.0, 1000)

# Retrieving stocks for the user
user_stocks = db_manager.get_user_stocks(user_id)
print(f"Stocks for John Doe: {user_stocks}")

db_manager.close()
