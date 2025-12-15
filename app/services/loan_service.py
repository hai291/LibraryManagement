from datetime import datetime
from models.models import Loan, Borrower, Book

class LoanService:
    @staticmethod
    def create_loan(borrower_id, book_id, bdate_str, ddate_str, status):
        """
        Xử lý logic mượn sách.
        Trả về: (Success: bool, Message: str)
        """
        # 1. Kiểm tra định dạng dữ liệu (Data Validation)
        if not borrower_id or not book_id:
            return False, "Vui lòng nhập ID Bạn đọc và ID Sách."
        
        try:
            d_borrow = datetime.strptime(bdate_str, "%Y-%m-%d")
            d_due = datetime.strptime(ddate_str, "%Y-%m-%d")
        except ValueError:
            return False, "Ngày tháng phải đúng định dạng YYYY-MM-DD."

        # 2. Kiểm tra Logic nghiệp vụ (Business Rules)
        
        # Rule 1: Ngày trả không được nhỏ hơn ngày mượn
        if d_borrow > d_due:
            return False, "Ngày hẹn trả không được nhỏ hơn ngày mượn."

        # Rule 2: Kiểm tra sự tồn tại (Reference Integrity)
        if not Borrower.exists(borrower_id):
            return False, f"Bạn đọc ID {borrower_id} không tồn tại."
        
        if not Book.exists(book_id):
            return False, f"Sách ID {book_id} không tồn tại."

        # Rule 3: Kiểm tra nợ xấu (Business Policy)
        # "Không cho mượn nếu đang giữ sách quá hạn"
        if Loan.check_borrower_has_overdue(borrower_id):
            return False, "Bạn đọc này đang có sách quá hạn chưa trả!"
        
        # Rule 4: Kiểm tra sách bận (Availability)
        # "Không cho mượn nếu sách đó chưa được trả kho"
        if Loan.check_book_is_borrowed(book_id):
            return False, "Cuốn sách này đang được người khác mượn."

        # 3. Nếu mọi thứ OK -> Gọi xuống Model để lưu (Persistence)
        if Loan.add(borrower_id, book_id, bdate_str, ddate_str, status):
            return True, "Mượn sách thành công!"
        else:
            return False, "Lỗi hệ thống cơ sở dữ liệu."

    @staticmethod
    def update_loan(loan_id, borrower_id, book_id, bdate_str, ddate_str, status):
        """Logic cập nhật phiếu mượn"""
        
        if Loan.check_book_is_borrowed(book_id, exclude_loan_id=loan_id):
             return False, "Sách này đang dính líu đến phiếu mượn khác."

        if Loan.update(loan_id, borrower_id, book_id, bdate_str, ddate_str, status):
            return True, "Cập nhật thành công."
        return False, "Lỗi khi cập nhật."