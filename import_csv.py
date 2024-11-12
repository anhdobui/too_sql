import csv
import sqlite3
 
# Tạo kết nối đến SQLite và sử dụng file để lưu dữ liệu
conn = sqlite3.connect("a.db")  # Kết nối đến file SQLite (nếu file chưa tồn tại, SQLite sẽ tự tạo)
cursor = conn.cursor()
 
# Khai báo tên bảng và tên file CSV
table_name = 'trans_minh'  # Tên bảng bạn muốn kiểm tra
csv_file = 'trans_minh.csv'  # Đường dẫn tới file CSV
 
# Tạo bảng theo cấu trúc đã nêu (chỉ tạo bảng nếu chưa có bảng nào)
# Kiểm tra xem bảng đã tồn tại chưa, nếu chưa tạo bảng và thêm dữ liệu
cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
table_exists = cursor.fetchone()
 
if not table_exists:
    # Nếu bảng trống, đọc file CSV và insert vào SQLite
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        headers = next(csv_reader)  # Lấy dòng đầu tiên làm tên cột
         # Làm sạch tiêu đề để đảm bảo hợp lệ với SQLite (chuyển đổi các ký tự không hợp lệ thành '_')
        headers = [header.replace(' ', '_').replace('-', '_').replace('#', '_').replace('.', '_') for header in headers]
        # Tạo câu lệnh CREATE TABLE với tên cột được làm sạch và bao quanh tên cột bằng dấu nháy kép
        create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'\"{header}\" TEXT' for header in headers])})"
        cursor.execute(create_table_query)
 
        # Thêm dữ liệu vào bảng
        for row in csv_reader:
            insert_query = f"INSERT INTO {table_name} ({', '.join([f'\"{header}\"' for header in headers])}) VALUES ({', '.join(['?' for _ in headers])})"
            cursor.execute(insert_query, row)
    # Lưu lại thay đổi (commit)
    conn.commit()
    print("Dữ liệu đã được thêm vào cơ sở dữ liệu.")
else:
    print(f"Bảng '{table_name}' đã tồn tại, không thực hiện thêm dữ liệu.")
 
# Thực hiện một truy vấn mẫu để kiểm tra dữ liệu (lấy 5 dòng đầu tiên)
cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
rows = cursor.fetchall()
 
# Hiển thị kết quả dưới dạng bảng với tiêu đề cột
 
 
for row in rows:
    print(row)
 
# Đóng kết nối
conn.close()
 