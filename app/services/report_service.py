# services/report_service.py
import csv
from models.models import Report

class ReportService:
    @staticmethod
    def export_report(report_type, file_path):
        """
        Lấy dữ liệu từ Model và ghi ra file CSV tại đường dẫn file_path
        """
        if not file_path:
            return False, "Chưa chọn đường dẫn lưu file."

        # 1. Lấy dữ liệu từ Database
        headers, rows = Report.execute_custom_query(report_type)
        
        if not rows:
            return False, "Không có dữ liệu để xuất báo cáo."

        # 2. Ghi file CSV (Logic xử lý file nằm ở Service)
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if headers: 
                    writer.writerow(headers) # Ghi tiêu đề cột
                writer.writerows(rows)       # Ghi dữ liệu
            return True, f"Đã xuất file thành công: {file_path}"
        except Exception as e:
            return False, f"Lỗi khi ghi file: {str(e)}"
# services/report_service.py
import csv
from models.models import Report

class ReportService:
    @staticmethod
    def export_report(report_type, file_path):
        """
        Lấy dữ liệu từ Model và ghi ra file CSV tại đường dẫn file_path
        """
        if not file_path:
            return False, "Chưa chọn đường dẫn lưu file."

        # 1. Lấy dữ liệu từ Database
        headers, rows = Report.execute_custom_query(report_type)
        
        if not rows:
            return False, "Không có dữ liệu để xuất báo cáo."

        # 2. Ghi file CSV (Logic xử lý file nằm ở Service, ko phải UI)
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if headers: 
                    writer.writerow(headers) # Ghi tiêu đề cột
                writer.writerows(rows)       # Ghi dữ liệu
            return True, f"Đã xuất file thành công: {file_path}"
        except Exception as e:
            return False, f"Lỗi khi ghi file: {str(e)}"