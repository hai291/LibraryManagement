import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# =========================================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN
# =========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
app_dir = os.path.join(project_root, 'app')

sys.path.append(project_root) 
sys.path.append(app_dir)      

# Import Service
from app.services.borrower_service import BorrowerService
from app.services.book_service import BookService
from app.services.loan_service import LoanService
from app.services.author_service import AuthorService
from app.services.report_service import ReportService
from app.services.dashboard_service import DashboardService
from app.db.connection import create_connection

class TestLibraryFullSuite(unittest.TestCase):
    
    # =========================================================================
    # GIAI ĐOẠN 1: TEST CẤU HÌNH & KẾT NỐI
    # =========================================================================
    @patch('mysql.connector.connect')
    def test_phase_1_connection_fail(self, mock_connect):
        from mysql.connector import Error
        mock_connect.side_effect = Error("Access denied")
        conn = create_connection()
        self.assertIsNone(conn)
        print("\n[PASS] Giai đoạn 1: Xử lý lỗi kết nối DB thành công.")

    # =========================================================================
    # GIAI ĐOẠN 2: QUẢN LÝ BẠN ĐỌC
    # =========================================================================
    def test_phase_2_borrower_empty_input(self):
        success, msg = BorrowerService.add_borrower("")
        self.assertFalse(success)
        self.assertEqual(msg, "Tên bạn đọc không được để trống.")
        print("[PASS] Giai đoạn 2: Chặn nhập tên rỗng.")

    @patch('models.models.Borrower.add')
    def test_phase_2_borrower_special_char(self, mock_add):
        mock_add.return_value = True
        name = "Nguyễn Văn A @#$%^&*()"
        success, msg = BorrowerService.add_borrower(name)
        
        self.assertTrue(success)
        mock_add.assert_called_with(name)
        print("[PASS] Giai đoạn 2: Chấp nhận ký tự đặc biệt.")

    @patch('models.models.Loan.check_borrower_has_active_loan')
    @patch('models.models.Borrower.delete')
    def test_phase_2_delete_clean_borrower(self, mock_delete, mock_check_loan):
        mock_check_loan.return_value = False 
        mock_delete.return_value = True      
        
        success, msg = BorrowerService.delete_borrower(1)
        self.assertTrue(success)
        self.assertEqual(msg, "Đã xóa hồ sơ bạn đọc.")
        print("[PASS] Giai đoạn 2: Xóa bạn đọc sạch thành công.")

    # =========================================================================
    # GIAI ĐOẠN 3: QUẢN LÝ SÁCH
    # =========================================================================
    @patch('models.models.Book.add')
    def test_phase_3_add_book_no_author(self, mock_add):
        mock_add.return_value = True
        success, msg = BookService.add_book("Dế Mèn", "")
        self.assertTrue(success)
        mock_add.assert_called() 
        print("[PASS] Giai đoạn 3: Thêm sách không tác giả thành công.")

    @patch('models.models.Book.update')
    def test_phase_3_update_book(self, mock_update):
        mock_update.return_value = True
        success, msg = BookService.update_book(1, "Tên Mới", "2")
        self.assertTrue(success)
        print("[PASS] Giai đoạn 3: Cập nhật sách thành công.")

    # =========================================================================
    # GIAI ĐOẠN 4: TEST MƯỢN TRẢ
    # =========================================================================
    def test_phase_4_validate_dates(self):
        success, msg = LoanService.create_loan("1", "1", "2023-10-30", "2023-10-01", "Borrowed")
        self.assertFalse(success)
        self.assertEqual(msg, "Ngày hẹn trả không được nhỏ hơn ngày mượn.")
        print("[PASS] Giai đoạn 4: Validate ngày tháng OK.")

    @patch('models.models.Borrower.exists')
    def test_phase_4_validate_id_fake(self, mock_b_exist):
        mock_b_exist.return_value = False 
        success, msg = LoanService.create_loan("9999", "1", "2023-01-01", "2023-01-05", "Borrowed")
        self.assertFalse(success)
        self.assertIn("không tồn tại", msg)
        print("[PASS] Giai đoạn 4: Chặn ID ảo thành công.")

    # [ĐÃ SỬA] Test Mượn Thành Công
    # Sửa: Patch check_borrower_has_overdue thay vì active_loan
    @patch('models.models.Loan.check_book_is_borrowed')
    @patch('models.models.Loan.check_borrower_has_overdue') 
    @patch('models.models.Book.exists')
    @patch('models.models.Borrower.exists')
    @patch('models.models.Loan.add')
    def test_phase_4_borrow_success(self, mock_add, mock_b_exist, mock_bk_exist, mock_check_overdue, mock_check_book):
        # Thiết lập "Đèn xanh" toàn bộ
        mock_b_exist.return_value = True         # User Tồn tại
        mock_bk_exist.return_value = True        # Sách Tồn tại
        mock_check_overdue.return_value = False  # KHÔNG Nợ xấu (Quan trọng)
        mock_check_book.return_value = False     # Sách KHÔNG bận
        mock_add.return_value = True             # DB Insert OK

        success, msg = LoanService.create_loan("1", "1", "2023-01-01", "2023-01-15", "Borrowed")
        
        self.assertTrue(success, f"Failed msg: {msg}")
        self.assertEqual(msg, "Mượn sách thành công!")
        print("[PASS] Giai đoạn 4: Quy trình mượn chuẩn OK.")

    # [ĐÃ SỬA] Test Sách Bận
    # Sửa: Patch check_borrower_has_overdue thay vì active_loan
    @patch('models.models.Loan.check_book_is_borrowed')
    @patch('models.models.Loan.check_borrower_has_overdue')
    @patch('models.models.Book.exists')
    @patch('models.models.Borrower.exists')
    def test_phase_4_book_busy(self, mock_b_exist, mock_bk_exist, mock_check_overdue, mock_check_book):
        """Test Business Rule: Sách đang bận"""
        mock_b_exist.return_value = True
        mock_bk_exist.return_value = True
        
        # QUAN TRỌNG: User phải sạch nợ thì code mới chạy tiếp xuống dòng check sách bận
        mock_check_overdue.return_value = False 
        
        # SÁCH ĐANG BẬN -> True -> Gây lỗi
        mock_check_book.return_value = True 
        
        success, msg = LoanService.create_loan("1", "1", "2023-01-01", "2023-01-05", "Borrowed")
        self.assertFalse(success)
        self.assertEqual(msg, "Cuốn sách này đang được người khác mượn.")
        print("[PASS] Giai đoạn 4: Chặn mượn sách đang bận OK.")

    @patch('models.models.Book.exists')
    @patch('models.models.Borrower.exists')
    @patch('models.models.Loan.check_borrower_has_overdue')
    def test_phase_4_bad_debt(self, mock_check_overdue, mock_b_exist, mock_bk_exist):
        mock_b_exist.return_value = True
        mock_bk_exist.return_value = True
        mock_check_overdue.return_value = True # User đang nợ xấu
        
        success, msg = LoanService.create_loan("1", "2", "2023-01-01", "2023-01-05", "Borrowed")
        self.assertFalse(success)
        self.assertIn("quá hạn", msg.lower()) 
        print("[PASS] Giai đoạn 4: Chặn nợ xấu OK.")

    @patch('models.models.Loan.check_book_is_borrowed')
    @patch('models.models.Loan.update')
    def test_phase_4_return_book(self, mock_update, mock_check_book):
        mock_check_book.return_value = False 
        mock_update.return_value = True
        
        success, msg = LoanService.update_loan(1, "1", "1", "2023-01-01", "2023-01-05", "Returned")
        self.assertTrue(success)
        print("[PASS] Giai đoạn 4: Trả sách thành công.")

    # =========================================================================
    # GIAI ĐOẠN 5: RÀNG BUỘC DỮ LIỆU
    # =========================================================================
    @patch('models.models.Loan.check_book_is_borrowed')
    def test_phase_5_delete_busy_book(self, mock_check_book):
        mock_check_book.return_value = True 
        success, msg = BookService.delete_book(1)
        self.assertFalse(success)
        self.assertEqual(msg, "Sách này đang được mượn, không thể xóa!")
        print("[PASS] Giai đoạn 5: Chặn xóa sách đang mượn OK.")

    @patch('models.models.Loan.check_borrower_has_active_loan')
    def test_phase_5_delete_busy_borrower(self, mock_check_user):
        mock_check_user.return_value = True 
        success, msg = BorrowerService.delete_borrower(1)
        self.assertFalse(success)
        self.assertIn("không thể xóa", msg) 
        print("[PASS] Giai đoạn 5: Chặn xóa bạn đọc đang giữ sách OK.")

    # =========================================================================
    # GIAI ĐOẠN 6: BÁO CÁO
    # =========================================================================
    @patch('models.models.Report.execute_custom_query')
    def test_phase_6_export_csv(self, mock_query):
        mock_query.return_value = (["Name", "Book"], [("An", "Book A")])
        with patch("builtins.open", mock_open()) as mock_file:
            success, msg = ReportService.export_report("INNER", "dummy_path.csv")
            self.assertTrue(success)
            print("[PASS] Giai đoạn 6: Xuất CSV (Mock File) thành công.")

    # =========================================================================
    # GIAI ĐOẠN 7: DASHBOARD
    # =========================================================================
    @patch('models.models.Loan.get_status_counts')
    @patch('models.models.DashboardStats.get_kpis')
    def test_phase_7_dashboard_update(self, mock_kpi, mock_chart):
        mock_kpi.return_value = (10, 20, 5, 1)
        mock_chart.return_value = [("Borrowed", 5), ("Overdue", 1)]

        nb, nbook, nloan, nov = DashboardService.get_summary_stats()
        self.assertEqual(nb, 10)
        self.assertEqual(nbook, 20)
        
        statuses, counts = DashboardService.get_chart_data()
        self.assertEqual(statuses, ["Borrowed", "Overdue"])
        print("[PASS] Giai đoạn 7: Dashboard lấy số liệu chuẩn.")

if __name__ == '__main__':
    unittest.main(verbosity=2)