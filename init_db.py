import clickhouse_connect
from datetime import date

client = clickhouse_connect.get_client(host='localhost', port=8123)

client.command("""
CREATE TABLE IF NOT EXISTS sales (
    id UInt32,
    product String,
    amount Float32,
    sale_date Date
) ENGINE = MergeTree()
ORDER BY id
""")

client.insert("sales", [
    (1, 'Laptop', 1200.50, date(2025, 1, 15)),
    (2, 'Monitor', 350.00, date(2025, 1, 16)),
    (3, 'Keyboard', 45.99, date(2025, 1, 17)),
    (4, 'Mouse', 25.50, date(2025, 1, 18)),
    (5, 'Headphones', 89.99, date(2025, 1, 19)),
])
print("✅ Таблица 'sales' создана, добавлено 5 записей.")