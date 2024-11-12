import sqlite3
import sys
from datetime import datetime
from utils import to_date
global file_run 
if 'dl' in [arg.strip() for arg in sys.argv[1:]]:
    file_run = 'ddl.sql'
else:
    file_run = 'query.sql'
print(f"File run: {file_run}")
# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('a.db')  # Thay bằng đường dẫn file SQLite của bạn
 
# Đăng ký hàm to_date vào SQLite
conn.create_function("to_date", 2, to_date)
#. . .
###########
cursor = conn.cursor()
 
# Thực hiện truy vấn SQL
with open(file_run, 'r', encoding='utf-8') as file:
    sql_query = file.read()
 
try:
    # Thực thi câu lệnh SQL (có thể là DDL hoặc DML)
    cursor.execute(sql_query)
 
    # Kiểm tra xem câu lệnh có trả về dữ liệu (SELECT) hay không
    if cursor.description:  # Chỉ có cursor.description nếu có kết quả trả về (SELECT)
        headers = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        # Lấy tên cột
        headers = [description[0] for description in cursor.description]
 
        # Tính toán độ dài cột dài nhất (để căn chỉnh)
        max_lengths = [len(header) for header in headers]  # Chiều dài tiêu đề
        for row in rows:
            for i, value in enumerate(row):
                max_lengths[i] = max(max_lengths[i], len(str(value)))  # Tính chiều dài tối đa
 
        # Ghi vào file .md dưới dạng bảng Markdown
        with open('query_result.md', 'w', encoding='utf-8') as file:
            # Viết tiêu đề bảng
            file.write("| " + " | ".join([f"{header:{max_lengths[i]}}" for i, header in enumerate(headers)]) + " |\n")
            # Viết đường kẻ phân cách giữa tiêu đề và dữ liệu
            separator = "| " + " | ".join(["-" * length for length in max_lengths]) + " |"
            file.write(separator + "\n")
            
            # Ghi dữ liệu vào bảng
            for row in rows:
                file.write("| " + " | ".join([f"{str(value):{max_lengths[i]}}" for i, value in enumerate(row)]) + " |\n")
    else:
        # Nếu là DDL (không có dữ liệu trả về), chỉ in thông báo
        print("Câu lệnh DDL đã được thực thi thành công.")
        # conn.commit()
 
# Đóng kết nối
except sqlite3.Error as e:
 
     # Lấy thời gian hiện tại
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Định dạng thời gian
 
    # Tạo thông báo lỗi
    error_message = f"{current_time} - Error: {e}\n\n"
    error_message += "------------------------RESULT OLD---------------------------------------------\n\n"
 
    try:
        # Đọc nội dung cũ của file
        with open('query_result.md', 'r', encoding='utf-8') as file:
            old_content = file.read()
 
        # Mở lại file để ghi lỗi vào đầu file và giữ lại nội dung cũ
        with open('query_result.md', 'w', encoding='utf-8') as file:
            file.write(error_message)  # Ghi lỗi vào đầu file
            file.write(old_content)    # Ghi lại nội dung cũ của file vào sau lỗi   
 
    except FileNotFoundError:
        # Nếu file không tồn tại, chỉ tạo file mới và ghi lỗi vào đó
        with open('query_result.md', 'w', encoding='utf-8') as file:
            file.write(error_message)
 
finally:
    # Đảm bảo rằng kết nối được đóng đúng cách
    conn.close()
    print("Kết nối đã được đóng.")
 