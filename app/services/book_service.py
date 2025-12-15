
from models.models import Book, Loan

class BookService:
    @staticmethod
    def add_book(title, author_id_str):
        """Thêm sách mới"""
        title = title.strip()
        author_id_str = author_id_str.strip()

        # 1. Validate Title
        if not title:
            return False, "Tiêu đề sách không được để trống."

        # 2. Validate Author (Nếu có nhập ID)
        author_id = None
        if author_id_str:
            if not author_id_str.isdigit():
                return False, "ID Tác giả phải là số."
            
            author_id = int(author_id_str)
        
        # 3. Gọi Model
        if Book.add(title, author_id_str):
            return True, "Thêm sách thành công."
        return False, "Lỗi Database."

    @staticmethod
    def update_book(book_id, title, author_id_str):
        """Cập nhật thông tin sách"""
        if not book_id: return False, "Thiếu ID sách."
        title = title.strip()
        
        if not title:
            return False, "Tiêu đề không được để trống."

        if Book.update(book_id, title, author_id_str):
            return True, "Cập nhật thành công."
        return False, "Lỗi cập nhật."

    @staticmethod
    def delete_book(book_id):
        """Xóa sách"""
        if not book_id: return False, "Chưa chọn sách."

        # RULE: Sách đang được mượn thì không được xóa khỏi kho
        if Loan.check_book_is_borrowed(book_id):
            return False, "Sách này đang được mượn, không thể xóa!"

        if Book.delete(book_id):
            return True, "Đã xóa sách khỏi kho."
        return False, "Lỗi Database."