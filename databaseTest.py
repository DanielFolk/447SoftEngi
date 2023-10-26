import sqlite3
import json


class DatabaseManager:
    def __init__(self, db_name='stocks.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create the 'stocks' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY,
                user_name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume INTEGER NOT NULL
            )
        ''')

        # Create the 'stock_metrics' table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_metrics (
                id INTEGER PRIMARY KEY,
                stock_id INTEGER,
                metrics_json TEXT NOT NULL,
                FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
        ''')
        self.conn.commit()

    def add_profile(self, user_name, user_email, threshold, symbol, price, volume):
        self.cursor.execute('''
            INSERT INTO stocks (user_name, symbol, price, volume) VALUES (?, ?, ?, ?)
        ''', (user_name, symbol, price, volume))
        stock_id = self.cursor.lastrowid  # Get the ID of the last inserted stock
        self.conn.commit()
        return stock_id

    def add_stock_metrics(self, stock_id, metrics_json):
        self.cursor.execute('''
            INSERT INTO stock_metrics (stock_id, metrics_json) VALUES (?, ?)
        ''', (stock_id, metrics_json))
        self.conn.commit()

    def get_stocks(self, user_name):
        self.cursor.execute(
            'SELECT * FROM stocks WHERE user_name = ?', (user_name,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


db_manager = DatabaseManager()

# Add a stock profile
stock_id = db_manager.add_profile('John Doe', 'joe_doe@gmail.com', '10.0', 'AAPL', 150.0, 1000)

# Add metrics for the stock
metrics_data = {'metric1': 20, 'metric2': 30}
metrics_json = json.dumps(metrics_data)
db_manager.add_stock_metrics(stock_id, metrics_json)

user_stocks = db_manager.get_stocks('John Doe')
print(f"Stocks for John Doe: {user_stocks}")

db_manager.close()
