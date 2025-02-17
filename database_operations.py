import sqlite3

DATABASE_NAME = "computers.db"

# Hàm thêm thiết bị
def add_computer(device_name, specifications, brand, location, status):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO computers (device_name, specifications, brand, location, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (device_name, specifications, brand, location, status))
    conn.commit()
    conn.close()
    print("Đã thêm thiết bị mới!")

# Hàm sửa thông tin thiết bị
def update_computer(id, device_name, specifications, brand, location, status):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE computers 
        SET device_name=?, specifications=?, brand=?, location=?, status=?
        WHERE id=?
    ''', (device_name, specifications, brand, location, status, id))
    conn.commit()
    conn.close()
    print("Đã cập nhật thông tin thiết bị!")

# Hàm xóa thiết bị
def delete_computer(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM computers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    print("Đã xóa thiết bị!")

# Hàm truy vấn danh sách thiết bị
def get_computers():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM computers")
    computers = cursor.fetchall()
    conn.close()
    return computers

# Chạy thử chức năng truy vấn
if __name__ == "__main__":
    print(get_computers())
