import sqlite3

# Kết nối đến database (nếu chưa có file thì SQLite sẽ tự động tạo)
conn = sqlite3.connect("computers.db")

# Tạo con trỏ để thao tác với database
cursor = conn.cursor()

# Tạo bảng computers
cursor.execute('''
CREATE TABLE IF NOT EXISTS computers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT NOT NULL,
    specifications TEXT NOT NULL,
    brand TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    image TEXT DEFAULT NULL
)
''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Database đã được cập nhật với cột 'image'!")
