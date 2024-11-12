import sqlite3
from datetime import datetime
 
# Hàm chuyển đổi ngày từ chuỗi sang định dạng yyyy-mm-dd
def to_date(date_str, format_str='%d-%m-%Y'):
    """
    Chuyển đổi chuỗi ngày tháng thành ngày hợp lệ trong SQLite (định dạng yyyy-mm-dd).
    
    :param date_str: Chuỗi ngày tháng cần chuyển đổi.
    :param format_str: Định dạng chuỗi ngày tháng (mặc định là '%d-%m-%Y').
    :return: Ngày tháng đã chuyển đổi hoặc None nếu không hợp lệ.
    """
    try:
        # Chuyển chuỗi ngày tháng theo định dạng đã cho
        date_obj = datetime.strptime(date_str, format_str)
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None  # Trả về None nếu chuỗi không hợp lệ