
from models.models import Borrower, Loan
class BorrowerService:
    @staticmethod
    def add_borrower(name):
        """Thêm bạn đọc mới"""
        name = name.strip()
        if not name:
            return False, "Tên bạn đọc không được để trống."
        
        
        if Borrower.add(name):
            return True, "Thêm bạn đọc thành công."
        return False, "Lỗi cơ sở dữ liệu."

    @staticmethod
    def delete_borrower(borrower_id):
        """Xóa bạn đọc"""
        if not borrower_id:
            return False, "Chưa chọn bạn đọc để xóa."

        if Loan.check_borrower_has_active_loan(borrower_id): 
            return False, "Bạn đọc này đang giữ sách (hoặc nợ quá hạn), không thể xóa!"

        if Borrower.delete(borrower_id):
            return True, "Đã xóa hồ sơ bạn đọc."
        return False, "Lỗi khi xóa (Có thể do ràng buộc dữ liệu)."