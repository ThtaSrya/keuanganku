import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bulan TEXT UNIQUE,
    nominal INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_barang TEXT,
    harga INTEGER,
    tanggal TEXT,
    bulan TEXT
)
""")

conn.commit()
conn.close()

print("Database berhasil dibuat!")