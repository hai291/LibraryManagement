# services/author_service.py
from models.models import Author

class AuthorService:
    @staticmethod
    def add_author(name):
        name = name.strip()
        if not name:
            return False, "Tên tác giả không được để trống."
        
        if Author.add(name):
            return True, "Thêm tác giả thành công."
        return False, "Lỗi hệ thống."

    @staticmethod
    def delete_author(author_id):
        if not author_id:
            return False, "Chưa chọn tác giả."
    
        
        if Author.delete(author_id):
            return True, "Đã xóa tác giả."
        return False, "Lỗi hệ thống."